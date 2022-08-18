"""Views For Company App"""
import re
from urllib import parse
from django.conf import settings
from django.shortcuts import render, reverse
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.views import View
import geocoder
import cloudinary
import cloudinary.uploader
from cloudinary import CloudinaryImage
from baseapp.models import Booking, Company
from core.models import CustomUser
from .forms import CompanyForm, CompanyEditForm

# Regex code made with https://regexr.com/ accessible at https://regexr.com/6rr71
ILLIGAL_CHARS = re.compile(r"(^[^\S])|(?:[^a-z\s]|\d\s)")
SPACE_PLUS = re.compile(r"([\s]\{2,})")

GOOGLE_API = settings.GOOGLE_API_KEY

def get_geocode(addr):
    g = geocoder.google(key=GOOGLE_API, location=str(addr))
    return [g.latlng[0], g.latlng[1]]

def retrieve_brand_image(image):
    """Function to retrieve optimal
       image i.e avif / webp etc. and
       with specified dimensions"""
    return CloudinaryImage(
        str(image)) \
        .image(
            transformation=[
                {'width': 48, 'aspect_ratio': "1.0", 'crop': "scale"},
                {'radius': "max"},
                {'fetch_format': "auto"}
                ]
            )

def edit_not_valid_view(request, errors):
    """Function to redirect user to
       index if not logged in and if not
       has already a company"""
    if request.user.is_authenticated:
        try:
            company = Company.objects.get(user_id=request.user.id)
            if company:
                if (
                    parse.urlparse(
                        request.META.get('HTTP_REFERER')
                        ).path in [
                            "/company/add/",
                            "/company/edit/"
                            ]
                    ):

                    num = 0
                    error_dict = {}
                    for error in errors:
                        for err in errors[error][num]:
                            error_dict.update({error: err})
                        num =+ 1

                    return render(
                        request,
                        'company/form_company_not_valid.html',
                        { "error_dict": error_dict }
                        )
                return HttpResponseRedirect(
                    reverse('company_account')
                    )
        except ObjectDoesNotExist:
            return HttpResponseRedirect(
                reverse('company_account')
                )
    return HttpResponseRedirect(
            reverse('home')
            )


class CompanyAccountView(View):
    """Company view to be directed
       to just after login, from there
       user can add, edit and delete
       their account"""
    def get(self, request):
        if request.user.is_authenticated:
            try:
                company = Company.objects \
                    .select_related('user') \
                    .select_related('category') \
                    .get(user_id=request.user.id)

                brand_image = company.brand_image

                if company:
                    if str(company.brand_image) != 'placeholder':
                        brand_image = retrieve_brand_image(str(company.brand_image))

                    context = {
                        "slug": company.slug,
                        "company_id": company.id,
                        "brand_image": brand_image,
                        "previous_brand_image": company.previous_brand_image,
                        "company_name": company.company_name,
                        "company_address": company.address,
                        "company_phone": company.phone,
                        "company_description": company.description,
                        "company_spots": company.spots,
                        "company_registered_on": company.registered_on,
                        "company_status": company.registration_status,
                        "company_user_id": company.user_id,
                        "company_website": company.website,
                        "user_first_name": company.user.first_name,
                        "user_last_name": company.user.last_name,
                        "user": company.user,
                    }

                    if company.registration_status == 'Approved':
                        p = Paginator(Booking.objects.filter(company_id=company.id), 10)

                        page = request.GET.get('page')
                        account = p.get_page(page)

                        return render(
                            request,
                            'company/account.html',
                            { "page": account, "context": context }
                            )
                    elif company.registration_status == 'Disapproved':
                        return render(
                            request,
                            'company/inactive_company.html',
                            context
                            )
                    return render(
                        request,
                        'company/pending_company.html',
                        context
                        )
            except ObjectDoesNotExist:
                return HttpResponseRedirect(
                        reverse('company_add')
                    )
            return render(
                request,
                'company/add_company.html',
                {
                    "user": company.user,
                    "company_form": CompanyForm(),
                    "google_api_key": GOOGLE_API,
                }
                )
        return HttpResponseRedirect(
            reverse('home')
            )


class CompanyCreateView(View):
    """Company create view to be
       directed to the company form
       for adding company info"""
    def get(self, request):
        """GET company form"""
        if request.user.is_authenticated:
            try:
                company = Company.objects.get(user_id=request.user.id)

                if company:
                    return HttpResponseRedirect(
                        reverse('company_account')
                    )
            except ObjectDoesNotExist:
                return render(
                    request,
                    'company/add_company.html',
                    {
                        "company_form": CompanyForm(),
                        "google_api_key": GOOGLE_API,
                    }
                )
        return HttpResponseRedirect(
            reverse('home')
            )


    def post(self, request):
        """POST new company info
           to the database"""
        if request.user.is_authenticated:
            form_company = CompanyForm(request.POST, request.FILES)

            if form_company.is_valid():
                previous_brand_image = str(form_company['brand_image'].data)
                company_name = form_company['company_name'].data.lower()
                phone = form_company['phone'].data

                form_company.company_name = re \
                    .sub(ILLIGAL_CHARS, '', company_name) \
                    .strip()

                full_address = form_company['address'].data
                latlng = get_geocode(full_address)
                latitude = latlng[0]
                longitude = latlng[0]

                Company.objects.create(
                    user_id=request.user.id,
                    previous_brand_image=previous_brand_image,
                    entered_phone=phone,
                    latitude=latitude,
                    longitude=longitude,
                    **form_company.cleaned_data
                    )

                return HttpResponseRedirect(
                        reverse('company_account')
                    )

            errors = form_company.errors.as_data()
            return edit_not_valid_view(request, errors)

        return HttpResponseRedirect(
            reverse('home')
            )


class CompanyUpdateView(View):
    """Company update view to be
       directed to the company edit form
       for updating company info"""
    def get(self, request):
        """GET company database Details"""
        if request.user.is_authenticated:
            try:
                company = Company.objects.get(user_id=request.user.id)

                brand_image = company.previous_brand_image

                if company:
                    if str(company.brand_image) != 'placeholder':
                        brand_image = retrieve_brand_image(str(company.brand_image))

                    initial_data_company = {
                        "previous_brand_image": company.previous_brand_image,
                        "company_name": company.company_name,
                        "address": company.address,
                        "phone": company.entered_phone,
                        "description": company.description,
                        "website": company.website,
                        "spots": company.spots,
                        "category": company.category,
                        "company_id": company.id,
                    }

                    d_brand_image = { "brand_image": brand_image }

                    company_form = CompanyEditForm(initial=initial_data_company)

                    return render(
                        request,
                        'company/edit_company.html',
                        {
                            "data": initial_data_company,
                            "dbm": d_brand_image,
                            "company_form": company_form,
                            "google_api_key": GOOGLE_API,
                        }
                        )
                return HttpResponseRedirect(
                    reverse('home')
                    )
            except ObjectDoesNotExist:
                return HttpResponseRedirect(
                        reverse('company_add')
                    )
        return HttpResponseRedirect(
            reverse('home')
            )

    def post(self, request):
        """POST updated company info
           to the database"""
        if request.user.is_authenticated:
            company = Company.objects.get(user_id=request.user.id)

            form_company = CompanyEditForm(request.POST, request.FILES)

            if form_company.is_valid():

                company.address = form_company['address'].data
                company.phone = form_company['phone'].data
                old_phone = company.entered_phone
                company.entered_phone = form_company['phone'].data
                company.description = form_company['description'].data
                company.spots = form_company['spots'].data
                company.website = form_company['website'].data

                brand_image = form_company['brand_image'].data
                if brand_image is not None:
                    cloudinary.uploader.destroy(
                        company.brand_image.public_id,
                        invalidate=True
                        )
                    company.brand_image = form_company['brand_image'].data
                    company.previous_brand_image = str(request.FILES.get('brand_image'))

                if company.entered_phone is old_phone:
                    company.entered_phone = old_phone

                if not company.latitude:
                    full_address = company.address
                    latlng = get_geocode(full_address)
                    company.latitude = latlng[0]
                    company.longitude = latlng[1]

                company.save()
                return HttpResponseRedirect(
                            reverse('company_account')
                        )

            errors = form_company.errors.as_data()
            return edit_not_valid_view(request, errors)

        return HttpResponseRedirect(
                        reverse('company_account')
                    )


class CompanyDeleteView(View):
    """Edit Company View"""
    def get(self, request):
        """GET delete company page"""
        if request.user.is_authenticated:
            user = CustomUser.objects.select_related('company').get(id=request.user.id)

            try:
                context = {
                    "company": user.company
                }

                if context['company']:
                    return render(
                        request,
                        'company/delete_company.html',
                        context
                        )
            except ObjectDoesNotExist:
                return HttpResponseRedirect(
                    reverse('company_account')
                    )
        return HttpResponseRedirect(
            reverse('home')
            )

    def post(self, request):
        """POST delete request to database"""
        if request.user.is_authenticated:
            user = CustomUser.objects.get(id=request.user.id)

            user.delete()

            return HttpResponseRedirect(
                        reverse('home')
                    )
        return HttpResponseRedirect(
            reverse('home')
            )


class CompanyExistView(View):
    """Exist Company View"""
    def get(self, request):
        """GET exists company page"""
        if request.user.is_authenticated:
            return render(
                request,
                'company/exists.html'
                )
        return HttpResponseRedirect(
            reverse('home')
            )

"""Views For Company App"""
import re
from django.conf import settings
from django.shortcuts import render, reverse
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.views import View
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

def retrieve_brand_image(image):
    return CloudinaryImage(
        str(image)) \
        .image(
            transformation=[
                {'width': 48, 'aspect_ratio': "1.0", 'crop': "scale"},
                {'radius': "max"},
                {'fetch_format': "auto"}
                ]
            )

class CompanyAccountView(View):
    """Company View"""
    def get(self, request):
        if request.user.is_authenticated:
            try:
                company = Company.objects \
                    .select_related('user') \
                    .select_related('category') \
                    .get(user_id=request.user.id)

                if company:
                    cloudinary_brand_image = retrieve_brand_image(str(company.brand_image))
                    context = {
                        "slug": company.slug,
                        "company_id": company.id,
                        "brand_image": cloudinary_brand_image,
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
                    "google_api_key": GOOGLE_API
                }
                )
        return HttpResponseRedirect(
            reverse('home')
            )


class CompanyCreateView(View):
    """Add New Company View"""
    def get(self, request):
        """Get New Company Form"""
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
                        "google_api_key": GOOGLE_API
                    }
                )
        return HttpResponseRedirect(
            reverse('home')
            )


    def post(self, request):
        """Post New Company Details"""
        if request.user.is_authenticated:
            form_company = CompanyForm(request.POST, request.FILES)

            if form_company.is_valid():
                # previous_brand_image = str(request.FILES.get('brand_image'))
                previous_brand_image = str(form_company['brand_image'].data)
                company_name = form_company['company_name'].data.lower()
                # company_name = request.POST.get('company_name').lower()

                form_company.company_name = re \
                    .sub(ILLIGAL_CHARS, '', company_name) \
                    .strip()

                Company.objects.create(
                    user_id=request.user.id,
                    previous_brand_image=previous_brand_image,
                    **form_company.cleaned_data
                    )

                return HttpResponseRedirect(
                        reverse('company_account')
                    )
            return HttpResponseRedirect(
                reverse('company_exists')
            )
        return HttpResponseRedirect(
            reverse('home')
            )


class CompanyUpdateView(View):
    """Edit Company View"""
    def get(self, request):
        if request.user.is_authenticated:
            try:
                company = Company.objects.get(user_id=request.user.id)

                if company:
                    cloudinary_brand_image = retrieve_brand_image(str(company.brand_image))

                    initial_data_company = {
                        "previous_brand_image": company.previous_brand_image,
                        "company_name": company.company_name,
                        "address": company.address,
                        "phone": company.phone,
                        "description": company.description,
                        "website": company.website,
                        "spots": company.spots,
                        "category": company.category,
                        "user_id": company.user_id,
                    }

                    d_brand_image = { "brand_image": cloudinary_brand_image }

                    company_form = CompanyEditForm(initial=initial_data_company)

                    return render(
                        request,
                        'company/edit_company.html',
                        {
                            "data": initial_data_company,
                            "dbm": d_brand_image,
                            "company_form": company_form,
                            "google_api_key": GOOGLE_API
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
        if request.user.is_authenticated:
            company = Company.objects.get(user_id=request.user.id)

            form_company = CompanyEditForm(request.POST, request.FILES)

            if form_company.is_valid():

                company.address = form_company['address'].data
                company.phone = form_company['phone'].data
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

                company.save()

                return HttpResponseRedirect(
                            reverse('company_account')
                        )
            if company:
                return HttpResponseRedirect(
                                reverse('company_edit_not_valid')
                            )
            return HttpResponseRedirect(
                            reverse('company_account')
                        )
        return HttpResponseRedirect(
            reverse('home')
            )


class CompanyDeleteView(View):
    """Edit Company View"""
    def get(self, request):
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
        if request.user.is_authenticated:
            return render(
                request,
                'company/exists.html'
                )
        return HttpResponseRedirect(
            reverse('home')
            )


def edit_not_valid_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        try:
            company = Company.objects.get(user_id=request.user.id)
            if company:
                pass

        except ObjectDoesNotExist:
            return HttpResponseRedirect(
                reverse('company_account')
            )
    return HttpResponseRedirect(
            reverse('home')
            )

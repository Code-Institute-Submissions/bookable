import re
from django.shortcuts import render, get_object_or_404, reverse
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.views import View
import cloudinary
import cloudinary.uploader
from baseapp.models import Booking, Company, Address
from core.models import CustomUser
from .forms import CompanyForm, CompanyEditForm, CompanyAddressForm

# Regex code made with https://regexr.com/ accessible at https://regexr.com/6rr71
ILLIGAL_CHARS = re.compile(r"(^[^\S])|(?:[^a-z\s]|\d\s)")
SPACE_PLUS = re.compile(r"([\s]\{2,})")

class CompanyAccountView(View):
    """Company View"""
    def get(self, request):
        if request.user.is_authenticated:
            try:
                queryset = Company.objects.select_related('user').get(user_id=request.user.id)

                if queryset:
                    context = {
                        "brand_image": queryset.brand_image,
                        "company": queryset.company_name,
                        "slug": queryset.slug,
                        "status": queryset.registration_status,
                        "user": queryset.user,
                    }

                    if queryset.registration_status == 'Approved':
                        p = Paginator(Booking.objects.filter(company_id=queryset.id), 10)

                        page = request.GET.get('page')
                        account = p.get_page(page)

                        return render(
                            request,
                            'company/account.html',
                            { "page": account, "context": context }
                            )
                    elif queryset.registration_status == 'Disapproved':
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
                    "user": queryset.user,
                    "company_form": CompanyForm(),
                    "address_form": CompanyAddressForm(),
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
                queryset = Company.objects.get(user_id=request.user.id)

                if queryset:
                    return HttpResponseRedirect(
                        reverse('company_account')
                    )
            except ObjectDoesNotExist:
                return render(
                    request,
                    'company/add_company.html',
                    {
                        "company_form": CompanyForm(),
                        "address_form": CompanyAddressForm(),
                    }
                )
        return HttpResponseRedirect(
            reverse('home')
            )


    def post(self, request):
        """Post New Company Details"""
        user = get_object_or_404(CustomUser, pk=request.user.id)
        if request.user.is_authenticated:
            form_company = CompanyForm(request.POST, request.FILES)
            form_company_address = CompanyAddressForm(request.POST)

            if form_company.is_valid() and form_company_address.is_valid():
                previous_brand_image = str(request.FILES.get('brand_image'))
                company_name = request.POST.get('company_name').lower()

                company_name = re \
                    .sub(ILLIGAL_CHARS, '', company_name) \
                    .strip()

                form = Company.objects.create(
                    user_id=user.id,
                    previous_brand_image=previous_brand_image,
                    **form_company.cleaned_data
                    )

                created_company = Company.objects.get(
                    company_name=form.company_name
                    )
                Address.objects.create(
                    pk=created_company.id,
                    **form_company_address.cleaned_data
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
            company = Company.objects.get(user_id=request.user.id)
            address = Address.objects.get(company_id=company)

            initial_data_company = {
                "current_brand_image": company.previous_brand_image,
                "company_name": company.company_name,
                "phone": company.phone,
                "street": address.street,
                "city": address.city,
                "google_map": company.google_map,
                "description": company.description,
                "website": company.website,
                "spots": company.spots,
                "category": company.category,
                "user_id": company.user.id,
            }

            d_brand_image = { "brand_image": company.brand_image }

            company_form = CompanyEditForm(initial=initial_data_company)

            return render(
                request,
                'company/edit_company.html',
                {
                    "data": initial_data_company,
                    "dbm": d_brand_image,
                    "company_form": company_form
                }
                )
        return HttpResponseRedirect(
            reverse('home')
            )

    def post(self, request):
        if request.user.is_authenticated:
            company = Company.objects.get(user_id=request.user.id)
            address = Address.objects.get(company_id=company)

            form_company = CompanyEditForm(request.POST, request.FILES)
            form_company_address = CompanyAddressForm(request.POST)

            if form_company.is_valid() and form_company_address.is_valid():

                company.phone = form_company['phone'].data
                company.description = form_company['description'].data
                company.spots = form_company['spots'].data
                company.google_map = form_company['google_map'].data
                company.website = form_company['website'].data
                address.street = form_company['street'].data
                address.city = form_company['city'].data

                brand_image = form_company['brand_image'].data
                if brand_image is not None:
                    cloudinary.uploader.destroy(
                        company.brand_image.public_id,
                        invalidate=True
                        )
                    company.brand_image = form_company['brand_image'].data
                    company.previous_brand_image = str(request.FILES.get('brand_image'))

                company.save()
                address.save()

                return HttpResponseRedirect(
                            reverse('company_account')
                        )
            return HttpResponseRedirect(
                            reverse('company_edit_not_valid')
                        )
        return HttpResponseRedirect(
            reverse('home')
            )


class CompanyDeleteView(View):
    """Edit Company View"""
    def get(self, request):
        if request.user.is_authenticated:
            user = CustomUser.objects.select_related('company').get(id=request.user.id)

            context = {
                "company": user.company
            }

            return render(
                request,
                'company/delete_company.html',
                context
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

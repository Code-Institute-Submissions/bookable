import re
from django.shortcuts import render, get_object_or_404, reverse
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.views import View
from baseapp.models import Booking, Company, Address
from core.models import CustomUser
from .forms import CompanyForm, CompanyAddressForm

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
                        "company": queryset.company_name,
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
            is_company_form_valid = form_company.is_valid()
            form_company_address = CompanyAddressForm(request.POST)
            if form_company.is_valid() and form_company_address.is_valid():
                company_name = request.POST.get('company_name').lower()
                re_illigal_chars = re \
                    .sub(ILLIGAL_CHARS, '', company_name) \
                    .replace('è', 'e') \
                    .strip()
                slug = re.sub(SPACE_PLUS, '', re_illigal_chars) \
                    .replace(' ', '-')
                form = Company.objects.create(
                    user_id=user.id,
                    slug=slug,
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
            else:
                if not is_company_form_valid:
                    return HttpResponseRedirect(
                        reverse('company_exists')
                    )
            return render(
                request,
                'company/account.html',
                )


class CompanyUpdateView(View):
    """Edit Company View"""
    def get(self, request):
        if request.user.is_authenticated:
            company = Company.objects.get(user_id=request.user.id)
            address = Address.objects.get(company_id=company)
            return render(
                request,
                'company/edit_company.html',
                {
                    "company": company,
                    "user": company.user,
                    "company_form": CompanyForm(instance=company),
                    "address_form": CompanyAddressForm(instance=address),
                }
                )
        return HttpResponseRedirect(
            reverse('home')
            )

    def post(self, request):
        if request.user.is_authenticated:
            company = Company.objects.get(user_id=request.user.id)
            address = Address.objects.get(company_id=company)
            form_company = CompanyForm(request.POST, instance=company)
            form_company_address = CompanyAddressForm(request.POST, instance=address)
            if form_company.is_valid() and form_company_address.is_valid():
                form_company.save()
                form_company_address.save()
            return HttpResponseRedirect(
                        reverse('company_account')
                    )


class CompanyDeleteView(View):
    """Edit Company View"""
    def get(self, request):
        if request.user.is_authenticated:
            user = CustomUser.objects.select_related('company').get(id=request.user.id)
            context = {
                "user": user,
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

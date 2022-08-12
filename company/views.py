from django.shortcuts import render, get_object_or_404, reverse
from django.core.exceptions import ObjectDoesNotExist
from django.views import View
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from core.models import CustomUser
from baseapp.models import Booking, Company, Address
from .forms import CompanyForm, CompanyAddressForm




class CompanyAccountView(View):
    """Company View"""
    def get(self, request):
        if request.user.is_authenticated:
            try:
                queryset = Company.objects.get(user_id=request.user.id)
                if queryset:
                    p = Paginator(Booking.objects.filter(company_id=queryset.id), 10)
                    page = request.GET.get('page')
                    account = p.get_page(page)
                    return render(
                        request,
                        'company/account.html',
                        { 'page': account }
                        )
            except ObjectDoesNotExist:
                return HttpResponseRedirect(
                        reverse('company_add')
                    )
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


class CompanyAddView(View):
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
                    'company/add_company.html'
                )

    def post(self, request):
        """Post New Company Details"""
        user = get_object_or_404(CustomUser, pk=request.user.id)
        if request.user.is_authenticated:
            form_company = CompanyForm(request.POST)
            form_company_address = CompanyAddressForm(request.POST)
            if form_company.is_valid() and form_company_address.is_valid():
                slug = request.POST.get('company_name').replace(' ', '-').replace("'", '').lower()
                form = Company.objects.create(
                    user_id=user.id,
                    slug=slug,
                    **form_company.cleaned_data
                    )
                created_company = Company.objects.get(company_name=form.company_name)
                Address.objects.create(
                    pk=created_company.id,
                    **form_company_address.cleaned_data
                    )
                return HttpResponseRedirect(
                        reverse('company_account')
                    )
            return render(
                request,
                'company/account.html',
                {
                    "form_company": form_company,
                    "form_address": form_company_address,
                }
                )


class CompanyEditView(View):
    """Edit Company View"""
    def get(self, request):
        if request.user.is_authenticated:
            company = Company.objects.get(user_id=request.user.id)
            address = Address.objects.get(company_id=company)
            return render(
                request,
                'company/edit_company.html',
                {
                    "company_form": CompanyForm(instance=company),
                    "address_form": CompanyAddressForm(instance=address),
                }
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

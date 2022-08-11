from django.shortcuts import render, get_object_or_404, reverse
from django.core.exceptions import ObjectDoesNotExist
from django.views import View
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from core.models import CustomUser
from baseapp.models import Booking, Company, Address
from .forms import NewCompanyForm, CompanyAddressForm


class CompanyAddView(View):
    """Add New Company View"""
    def get(self, request):
        """Get New Company Form"""
        if request.user.is_authenticated:
            return render(
                request,
                'company/add_company.html',
                {
                    "company_form": NewCompanyForm(),
                    "address_form": CompanyAddressForm(),
                }
            )

    def post(self, request, *args, **kwargs):
        """Post New Company Details"""
        user = get_object_or_404(CustomUser, pk=request.user.id)
        if request.user.is_authenticated:
            form_company = NewCompanyForm(request.POST)
            form_company_address = CompanyAddressForm(request.POST)
            if form_company.is_valid() and form_company_address.is_valid():
                slug = request.POST.get('company_name').replace(' ', '-').replace("'", '').lower()
                form = Company.objects.create(
                    user_id=user.id,
                    slug=slug,
                    **form_company.cleaned_data
                    )
                new_company = Company.objects.get(company_name=form.company_name)
                print(new_company.id)
                Address.objects.create(
                    pk=new_company.id,
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


class CompanyAccountView(View):
    """Company View"""
    def get(self, request):
        if request.user.is_authenticated:
            try:
                queryset = Company.objects.get(user_id=request.user.id)
                if queryset:
                    p = Paginator(Booking.objects.filter(company_id=queryset.id), 10)
                    page = request.GET.get('page')
                    index = p.get_page(page)
                    return render(
                        request,
                        'company/index.html',
                        { 'index': index }
                        )
            except ObjectDoesNotExist:
                return HttpResponseRedirect(
                        reverse('company_add')
                    )
            return render(
                request,
                'company/add_company.html',
                {
                    "company_form": NewCompanyForm(),
                    "address_form": CompanyAddressForm(),
                }
            )

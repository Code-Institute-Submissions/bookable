from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.views import View
from core.models import CustomUser
from baseapp.models import Booking, Company, Address
from .forms import NewCompanyForm, CompanyAddressForm


class CompanyView(View):
    """Company View"""
    def get(self, request):
        if request.user.is_authenticated:
            try:
                if Company.objects.filter(user_id=request.user.id):
                    return render(
                        request,
                        'company/index.html'
                        )
            except ObjectDoesNotExist:
                return render(
                    request,
                    'company/new_company.html',
                    {
                      "company_form": NewCompanyForm(),
                      "address_form": CompanyAddressForm()
                    }
                )

    def post(self, request, **kwargs):
        """Post New Company Details"""
        user = get_object_or_404(CustomUser, pk=request.user.id)
        if request.user.is_authenticated:
            form_company = NewCompanyForm(request.POST)
            form_company_address = CompanyAddressForm(request.POST)
            if form_company.is_valid() and form_company_address.is_valid():
                form = Company.objects.create(
                    user_id=user.id,
                    **form_company.cleaned_data
                    )
                new_company = Company.objects.get(company_name=form.company_name)
                print(new_company.id)
                Address.objects.create(
                    pk=new_company.id,
                    **form_company_address.cleaned_data
                    )
                context = {
                    "form_company": form_company,
                    "form_address": form_company_address,
                }
                return render(
                  request,
                  'company/index.html',
                  context
                )

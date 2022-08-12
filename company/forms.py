from django import forms
from baseapp.models import Address, Company


class CompanyForm(forms.ModelForm):
    """New Company Form"""
    class Meta:
        model = Company
        fields = (
            'brand_image',
            'company_name',
            'phone',
            'google_map',
            'description',
            'website',
            'spots',
            'category',
            )


class CompanyAddressForm(forms.ModelForm):
    """New Company Form"""
    class Meta:
        model = Address
        fields = (
            'street',
            'city',
            )

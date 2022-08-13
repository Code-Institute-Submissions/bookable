from django import forms
from cloudinary.forms import CloudinaryJsFileField
from baseapp.models import Address, Company


class CompanyForm(forms.ModelForm):
    """New Company Form"""
    class Meta:
        model = Company
        brand_image = CloudinaryJsFileField()
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

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


class CompanyEditForm(forms.ModelForm):
    """Edit Company Form"""
    user_id = forms.CharField()
    street = forms.CharField()
    city = forms.CharField()

    class Meta:
        model = Company
        fields = (
            'brand_image',
            'company_name',
            'phone',
            'street',
            'city',
            'google_map',
            'description',
            'website',
            'spots',
            'category',
            'user_id',
            )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["company_name"].disabled = True
        self.fields["company_name"].required = False
        self.fields["user_id"].disabled = True
        self.fields["user_id"].required = False


class CompanyAddressForm(forms.ModelForm):
    """New Company Form"""
    class Meta:
        model = Address
        fields = (
            'street',
            'city',
            )

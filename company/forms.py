"""Company Forms"""
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from baseapp.models import Company


class CompanyForm(forms.ModelForm):
    """New Company Form"""
    brand_image = forms.FileField(
        label='Brand Image',
        help_text='Please use a width of 480px or 240px and a ratio of 1:1',
        required=False
    )
    address = forms.CharField(
        label='Address',
        help_text='format: 103 Greenwich Avenue, New York, NY, USA'
    )
    phone = PhoneNumberField(
        help_text='format: country code ie. +1 followed by 123-123-1234'
    )

    class Meta:
        model = Company
        fields = (
            'brand_image',
            'company_name',
            'address',
            'phone',
            'description',
            'website',
            'spots',
            'category',
            )


class CompanyEditForm(forms.ModelForm):
    """Edit Company Form"""
    brand_image = forms.FileField(
        label='Brand Image',
        help_text='Please use a width of 480px or 240px and a ratio of 1:1',
        required=False
        )
    previous_brand_image = forms.CharField(
        label='File name'
    )
    address = forms.CharField(
        label='Address',
        help_text='format: 103 Greenwich Avenue, New York, NY, USA'
    )
    phone = forms.CharField(
        label='Phone',
        help_text='format: country code ie. +1 followed by 123-123-1234'
    )
    company_id = forms.CharField()

    class Meta:
        model = Company
        fields = (
            'previous_brand_image',
            'brand_image',
            'company_name',
            'address',
            'phone',
            'description',
            'website',
            'spots',
            'category',
            'company_id',
            )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["company_name"].disabled = True
        self.fields["company_name"].required = False
        self.fields["company_id"].disabled = True
        self.fields["company_id"].required = False
        self.fields["previous_brand_image"].disabled = True
        self.fields["previous_brand_image"].required = False

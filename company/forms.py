from django import forms
from baseapp.models import Company


class CompanyForm(forms.ModelForm):
    """New Company Form"""
    brand_image = forms.FileField(
        label='Brand Image',
        help_text='Please use a width of 480px or 240px and a ratio of 1:1'
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
    user_id = forms.CharField()

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
            'user_id',
            )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["company_name"].disabled = True
        self.fields["company_name"].required = False
        self.fields["user_id"].disabled = True
        self.fields["user_id"].required = False
        self.fields["previous_brand_image"].disabled = True
        self.fields["previous_brand_image"].required = False

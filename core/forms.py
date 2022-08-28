"""Signup Form"""
from allauth.account.forms import SignupForm
from django import forms


class CompanySignupForm(SignupForm):
    """Extend Allauth Signup Form"""
    username = forms.CharField(
        help_text='No spaces is allowed, they are removed'
    )
    first_name = forms.CharField(
        max_length=30,
        label = 'First Name',
        widget=forms.TextInput(attrs={'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=30,
        label = 'Last Name',
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'})
    )

    def save(self, request):
        user = super(CompanySignupForm, self).save(request)
        user.username = self.cleaned_data['username']\
            .strip().lower().replace(' ', '')
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user

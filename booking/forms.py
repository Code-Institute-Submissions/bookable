from django import forms
from baseapp.models import Booking


class BookingForm(forms.ModelForm):
    """Booking Form"""
    spots = forms.CharField(
        label='Guests',
        widget=forms.TextInput(
            attrs={
                "placeholder": "How many people?"
            }
        ),
    )
    date_time = forms.CharField(
        label='Date & Time',
        widget=forms.TextInput(
            attrs={
                "placeholder": "Pick a time"
            }
        ),
    )
    first_name = forms.CharField(max_length=255, required=True)
    last_name = forms.CharField(max_length=255,required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(
        label='Phone',
        help_text='format: country code ie. +1 followed by 123-123-1234'
    )

    class Meta:
        model = Booking
        fields = (
            'spots',
            'date_time',
            'first_name',
            'last_name',
            'email',
            'phone',
            )


class BookingCustomerDeleteForm(forms.ModelForm):
    """Booking Customer Delete Form"""
    email = forms.CharField(
        label='Your Email',
        widget=forms.TextInput(
            attrs={
                "placeholder": "Your booking email"
            }
        ),
        help_text='Please use the email you used when you made your booking.'
    )

    class Meta:
        model = Booking
        fields = (
            'email',
            )

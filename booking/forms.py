from django import forms
from baseapp.models import Booking


class BookingForm(forms.ModelForm):
    """Booking Form"""

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

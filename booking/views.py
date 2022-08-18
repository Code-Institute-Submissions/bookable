import urllib.parse
from django.conf import settings
from django.shortcuts import render, reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.views import View
from cloudinary import CloudinaryImage
from baseapp.models import Booking, Company
from .forms import BookingForm


GOOGLE_API = settings.GOOGLE_API_KEY


def booking_form_not_valid_view(request, errors):
    """Function to redirect user to
       index if not logged in and if not
       has already a company"""
    return


class BookingView(View):
    """Booking view"""
    def get(self, request):
        """GET request will redirect
           the user to home"""
        return HttpResponseRedirect(
            reverse('home')
            )


class BookingCreateView(View):
    """Company create view to be
       directed to the company form
       for adding company info"""
    def get(self, request, **kwargs):
        """GET company form"""
        path = request.path
        try:
            company = Company.objects.get(slug=kwargs['slug'])

            brand_image = company.brand_image

            if str(company.brand_image) != 'placeholder':
                brand_image = CloudinaryImage(
                    str(company.brand_image))\
                    .image(width=96,transformation=[
                        {'width': 96, 'aspect_ratio': "1.0", 'crop': "scale"},
                        {'fetch_format': "auto"}, {'radius': 'max'},
                        ]
                    )

            full_address = company.address

            split = full_address.split(',')
            street = split[-4]
            city = split[-3]
            state = split[-2]

            quote_company_name = urllib.parse.quote_plus(company.company_name).lower()
            google_map_search = 'https://www.google.com/maps/search/'
            get_directions = google_map_search+quote_company_name

            context = {
                "booking_path": path,
                "company_name": company.company_name,
                "company_directions": get_directions,
                "company_brand_image": brand_image,
                "full_address": full_address,
                "company_street": street,
                "company_city": city,
                "company_state": state,
                "company_phone": company.phone,
                "company_entered_phone": company.entered_phone,
                "company_description": company.description,
                "company_website": company.website,
                "booking_form": BookingForm(),
                "google_api_key": GOOGLE_API,
                "latitude": company.latitude,
                "longitude": company.longitude,
            }

            return render(
                request,
                'booking/book_company.html',
                { 'context': context }
            )
        except ObjectDoesNotExist:
            return render(
                request,
                'booking/book_company_error.html',
                { "does_not_exist": "Company does not exist!" }
            )


    def post(self, request, **kwargs):
        """POST new booking info
           to the database"""
        form_booking = BookingForm(request.POST)

        if form_booking.is_valid():
            Booking.objects.create(
                **form_booking.cleaned_data
                )

        errors = form_booking.errors.as_data()
        return booking_form_not_valid_view(request, errors)

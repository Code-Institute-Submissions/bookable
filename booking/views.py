"""Booking Model Views"""
import re
from django.conf import settings
from django.shortcuts import render, reverse, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.views import View
from cloudinary import CloudinaryImage
from baseapp.models import Booking, Company, Customer
from .forms import BookingForm, BookingCustomerDeleteForm


GOOGLE_API = settings.GOOGLE_API_KEY


def company_not_valid_view(request, **kwargs):
    """Function to run company does not
       exist page"""
    company = kwargs['slug'].replace('-', ' ')

    return render(
        request,
        'booking/book_company_does_not_exist.html',
        {"company": company}
        )


def not_valid_view(request, **kwargs):
    """Function to run booking does not
       exist page"""
    context = {
        "obj": kwargs,
    }

    return render(
        request,
        'booking/book_does_not_exist.html',
        context
        )


def get_direction(obj):
    """Make a company google map direction link"""
    address = obj.address.replace(',', '').replace(' ', '+')
    slug = obj.slug.replace('-', '+')
    return 'https://www.google.com/maps/search/'\
        + slug + '+' + address


def form_not_valid_view(request, errors):
    """Function to redirect user to
       not valid form page displaying the errors"""
    num = 0
    error_dict = {}
    for error in errors:
        for err in errors[error][num]:
            error_dict.update({error: err})
        num += 1

    return render(
        request,
        'booking/book_form_not_valid.html',
        {"error_dict": error_dict}
        )


class BookingView(View):
    """Booking view"""
    def get(self, request):
        """GET request will redirect
           the user to home"""
        return HttpResponseRedirect(
            reverse('home')
            )


class BookingCreateView(View):
    """Booking create view to be
       directed to the booking form"""
    def get(self, request, **kwargs):
        """GET company booking form"""
        path = request.path
        not_valid = re.search(r'\/not-valid\/', path)
        if not_valid:
            return company_not_valid_view(request, **kwargs)

        try:
            company = Company.objects.get(slug=kwargs['slug'])

            brand_image = company.brand_image

            if str(company.brand_image) != 'placeholder':
                brand_image = CloudinaryImage(
                    str(company.brand_image))\
                    .image(width=96, transformation=[
                        {'width': 96, 'aspect_ratio': "1.0", 'crop': "scale"},
                        {'fetch_format': "auto"}, {'radius': 'max'},
                        ]
                    )

            full_address = company.address

            split = full_address.split(',')

            street = split[0].strip()
            city = split[1].strip()
            state = split[2].strip()



            context = {
                "booking_path": path,
                "company_name": company.company_name,
                "company_direction": get_direction(company),
                "company_brand_image": brand_image,
                "full_address": full_address,
                "company_street": street,
                "company_city": city,
                "company_state": state,
                "company_phone": company.phone.replace(' ', ''),
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
                {'context': context}
            )
        except ObjectDoesNotExist:
            return company_not_valid_view(request, **kwargs)

    def post(self, request, **kwargs):
        """POST new booking info
           to the database"""

        company = Company.objects.get(slug=kwargs['slug'])

        form_booking = BookingForm(request.POST)

        if form_booking.is_valid():
            try:
                customer = Customer.objects.get(
                    email=form_booking['email'].data
                    )

            except ObjectDoesNotExist:
                customer = Customer.objects.create(
                    first_name=form_booking['first_name'].data,
                    last_name=form_booking['last_name'].data,
                    email=form_booking['email'].data,
                    phone=form_booking['phone'].data
                    )

            queryset = Booking.objects.filter(
                date_time=form_booking['date_time'].data)
            company_spots = Company.objects.get(
                slug=kwargs['slug']).spots

            if len(queryset.filter(
                    customer_id=customer.id)) >= 1:
                request.session['temp_duplicate_date_time'] = \
                    form_booking['date_time'].data

                return redirect('already-booked/')

            if len(queryset) >= company_spots:
                request.session['temp_spots_filled_date_time'] = \
                    form_booking['date_time'].data

                return redirect('spots-filled/')

            booking = Booking.objects.create(
                date_time=form_booking['date_time'].data,
                spots=form_booking['spots'].data,
                customer_id=customer.id,
                company_id=company.id
                )

            redirection = 'thank-you/' + str(booking.id) + '/'

            return redirect(redirection)

        errors = form_booking.errors.as_data()
        return form_not_valid_view(request, errors)


class BookingDetailView(View):
    """Booking detail view to redirect
       a customer to the thank you page"""
    def get(self, request, **kwargs):
        """GET Thank You Page"""
        try:
            obj = Booking.objects\
                .select_related('company')\
                .select_related('customer')\
                .get(id=kwargs['id'])

            return render(
                request,
                'booking/book_thankyou.html',
                {"obj": obj, "direction": get_direction(obj.company)}
            )

        except ObjectDoesNotExist:
            try:
                if (
                    request.path != '/booking/' + kwargs['slug'] + '/' and
                    Company.objects.get(slug=kwargs['slug'])
                ):

                    return not_valid_view(request, **kwargs)

            except Exception:
                try:
                    if Company.objects.get(slug=kwargs['slug']):
                        return not_valid_view(request, **kwargs)

                except ObjectDoesNotExist:
                    return redirect('../../not-valid/')


class BookingAlreadyBookedView(View):
    """Already Booked Booking View"""
    def get(self, request, **kwargs):
        """GET spots filled on date page"""
        date_time = request.session['temp_duplicate_date_time']
        booked = Booking.objects.select_related('company')\
            .get(date_time=date_time)

        return render(
            request,
            'booking/book_duplicate.html',
            {
                "date_time": date_time, "id": booked.id,
                "slug": booked.company.slug
            }
            )


class BookingSpotsFilledView(View):
    """Spots Filled Booking View"""
    def get(self, request, **kwargs):
        """GET spots filled on date page"""
        filled_date_time = request.session['temp_spots_filled_date_time']

        return render(
            request,
            'booking/book_spots_filled.html',
            {"date_time": filled_date_time}
            )


class BookingDeleteView(View):
    """Delete Booking View"""
    def get(self, request, **kwargs):
        """GET delete customer page"""
        try:
            obj = Booking.objects.select_related('customer')\
                .get(id=kwargs['id'])

            context = {
                "obj": obj,
                "kwargs": kwargs,
                "BookingCustomerDeleteForm": BookingCustomerDeleteForm()
            }

            return render(
                request,
                'booking/book_delete.html',
                context
                )

        except ObjectDoesNotExist:
            return redirect('not-valid/')

    def post(self, request, **kwargs):
        """POST delete request to database"""
        try:
            obj = Booking.objects.select_related('customer')\
                .get(id=kwargs['id'])

            form_del_booking = BookingCustomerDeleteForm(request.POST)
            form_email = form_del_booking['email'].data

            context = {
                "obj": obj,
                "kwargs": kwargs,
                "error_user_not_same": (
                    """<div class="alert alert-danger" role="alert">
                        <p class="my-0">Error: """ + form_email + """</p>
                        <p class="my-0">Email isn't as the email used to
                        make the booking!</p>
                    </div>"""
                ),
                "BookingCustomerDeleteForm": BookingCustomerDeleteForm()
            }

            if form_del_booking.is_valid():

                if form_email == obj.customer.email:
                    obj.delete()

                    return render(
                        request,
                        'booking/book_deleted.html',
                        context
                        )
                return render(
                    request,
                    'booking/book_delete.html',
                    context
                    )

        except ObjectDoesNotExist:
            return redirect('not-valid/')


class BookingDoesNotExistView(View):
    """Delete Booking Does Not Exist View"""
    def get(self, request, **kwargs):
        """GET delete booking object
           customer page if object exists"""
        try:
            Booking.objects.get(id=kwargs['id'])
            return redirect('../../')

        except ObjectDoesNotExist:
            return not_valid_view(request, **kwargs)

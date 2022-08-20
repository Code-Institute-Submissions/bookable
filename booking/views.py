from django.conf import settings
from django.shortcuts import render, reverse, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse
from django.views import View
from cloudinary import CloudinaryImage
from baseapp.models import Booking, Company, Customer
from .forms import BookingForm, BookingCustomerDeleteForm


GOOGLE_API = settings.GOOGLE_API_KEY

def get_direction(obj):
    """Make a company google map direction link"""
    address = obj.address.replace(',', '').replace(' ', '+')
    slug = obj.slug.replace('-', '+')
    return 'https://www.google.com/maps/search/'\
         + slug + '+' + address

def booking_form_not_valid_view(request, errors):
    """Function to redirect user to
       not valid form page displaying the errors"""
    return HttpResponse('OK')


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

            context = {
                "booking_path": path,
                "company_name": company.company_name,
                "company_direction": get_direction(company),
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
        return booking_form_not_valid_view(request, errors)


class BookingDetailView(View):
    """Company create view to be
       directed to the company form
       for adding company info"""
    def get(self, request, **kwargs):
        """GET company form"""
        try:
            obj = Booking.objects\
                .select_related('company')\
                .select_related('customer')\
                .get(id=kwargs['id'])

            return render(
                request,
                'booking/book_thankyou.html',
                { "obj": obj, "direction": get_direction(obj.company) }
            )

        except ObjectDoesNotExist:
            if request.path != '/booking/' + kwargs['slug'] + '/':
                context = {
                    "obj": kwargs,
                }

                return render(
                    request,
                    'booking/book_does_not_exist.html',
                    context
                    )
            return render(
                request,
                'booking/book_company_error.html',
                { "does_not_exist": "Company does not exist!" }
            )


class BookingAlreadyBookedView(View):
    """Already Booked Booking View"""
    pass


class BookingSpotsFilledView(View):
    """Spots Filled Booking View"""
    def get(self, request, **kwargs):
        """GET spots filled on date page"""
        filled_date_time = request.session['temp_spots_filled_date_time']

        return render(
            request,
            'booking/book_spots_filled.html',
            { "date_time": filled_date_time }
            )


class BookingDeleteView(View):
    """Delete Booking View"""
    def get(self, request, **kwargs):
        """GET delete customer page"""

        print(request)
        print(kwargs)

        try:
            obj = Booking.objects.select_related('customer').get(id=kwargs['id'])
            print(obj)

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
            obj = Booking.objects.select_related('customer').get(id=kwargs['id'])

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
            context = {
                "obj": kwargs,
            }

            return render(
                request,
                'booking/book_does_not_exist.html',
                context
                )

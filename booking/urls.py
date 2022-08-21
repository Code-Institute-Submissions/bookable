from django.urls import path
from .views import *


urlpatterns = [
    path(
        '',
        BookingView.as_view(),
        name='booking_view'
    ),
    path(
        '<slug:slug>/',
        BookingCreateView.as_view(),
        name='book_company'
    ),
    path(
        '<slug:slug>/not-valid/',
        BookingCreateView.as_view(),
        name='book_company_not_valid'
    ),
    path(
        '<slug:slug>/already-booked/',
        BookingAlreadyBookedView.as_view(),
        name='book_already_booked'
    ),
    path(
        '<slug:slug>/spots-filled/',
        BookingSpotsFilledView.as_view(),
        name='book_spots_filled'
    ),
    path(
        '<slug:slug>/thank-you/<int:id>/',
        BookingDetailView.as_view(),
        name='book_thankyou'
    ),
    path(
        '<slug:slug>/thank-you/<int:id>/delete/',
        BookingDeleteView.as_view(),
        name='book_delete'
    ),
    path(
        '<slug:slug>/thank-you/<int:id>/delete/not-valid/',
        BookingDoesNotExistView.as_view(),
        name='book_does_not_exist'
    ),
]

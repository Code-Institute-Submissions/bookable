from django.urls import path
from django.views.generic import TemplateView
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
]

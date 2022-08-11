from django.urls import path
from django.views.generic import TemplateView
from .views import *


urlpatterns = [
    path(
        '',
        CompanyView.as_view(),
        name='company_index'
    ),
    path(
        'add/',
        CompanyAddView.as_view(),
        name='company_add'
    ),
]

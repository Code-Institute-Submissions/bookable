from django.urls import path
from django.views.generic import TemplateView
from .views import *


urlpatterns = [
    path(
        '',
        CompanyAccountView.as_view(),
        name='company_account'
    ),
    path(
        'add/',
        CompanyAddView.as_view(),
        name='company_add'
    ),
]

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
        CompanyCreateView.as_view(),
        name='company_add'
    ),
    path(
        'exists/',
        CompanyExistView.as_view(),
        name='company_exists'
    ),
    path(
        'edit/',
        CompanyUpdateView.as_view(),
        name='company_edit'
    ),
    path(
        'form-not-valid/',
        edit_not_valid_view,
        name='form_company_not_valid'
    ),
    path(
        'delete/',
        CompanyDeleteView.as_view(),
        name='company_delete'
    ),
]

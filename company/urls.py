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
        'edit-not-valid/',
        TemplateView.as_view(
            template_name='company/edit_company_not_valid.html'),
        name='company_edit_not_valid'
    ),
    path(
        'delete/',
        CompanyDeleteView.as_view(),
        name='company_delete'
    ),
]

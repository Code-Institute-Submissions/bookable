from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode
from . import models

# Register your models here.
@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'companys_count']
    list_per_page = 10

    @admin.display(ordering='companys_count')
    def companys_count(self, category):
        url = (
            reverse('admin:baseapp_company_changelist')
            + '?'
            + urlencode({
                'category__id': str(category.id)
            }))
        return format_html(
                '<a href="{}">{}</a>',
                url,
                category.companys_count
                )

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            companys_count=Count('company')
        )


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'user_id', 'registered_on', 'registration_status']
    list_per_page = 10

    def user_id(self, company):
        url = (
            reverse('admin:auth_user_changelist')
            + '?'
            + urlencode({
                'company__id': str(company.id)
            }))
        return format_html(
            '<a href="{}">{}</a>',
            url,
            company.user_id
            )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name']
    ordering = ['first_name', 'last_name']
    list_per_page = 10

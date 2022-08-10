from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.sites.models import Site
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode
from allauth.socialaccount.models import (
    EmailAddress, SocialToken, SocialAccount, SocialApp
    )
from core.models import CustomUser
from . import models


@admin.register(CustomUser)
class UserAdmin(BaseUserAdmin):
    list_per_page = 10
    search_fields = ['username']
    add_fieldsets = (
        (None, {
                "classes": ("wide",),
                "fields": (
                    "first_name", "last_name",
                    "username", "email",
                    "password1", "password2",
                    ),
            },),
    )


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'companys_count']
    list_per_page = 10
    search_fields = ['title']
    fields = ['title']

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
    autocomplete_fields = ['category', 'user']
    prepopulated_fields = {
        'slug': ['company_name']
    }
    list_display = ['company_name', 'user_id', 'registered_on', 'registration_status', 'category']
    list_editable = ['registration_status']
    list_filter = ['registration_status']
    list_per_page = 10
    search_fields = ['company_name__istartswith']

    def user_id(self, company):
        url = (
            reverse('admin:core_customuser_changelist')
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


admin.site.unregister(EmailAddress)
admin.site.unregister(Site)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialToken)
admin.site.unregister(SocialApp)

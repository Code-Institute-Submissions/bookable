from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html, urlencode
from . import models

# Register your models here.
@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_per_page = 10


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'user_id', 'registered_on', 'registration_status']
    list_per_page = 10

    def user_id(self, company):
        url = (
            reverse('admin:auth_user_changelist')
            + '?'
            + urlencode({
                'q': str(company.company_name)
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

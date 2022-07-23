from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_per_page = 10


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'company_name', 'registered_on', 'registration_status']
    list_per_page = 10


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name']
    ordering = ['first_name', 'last_name']
    list_per_page = 10

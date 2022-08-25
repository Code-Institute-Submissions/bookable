"""Bookable Models"""
from django.conf import settings
from django.core.validators import URLValidator
from django.utils.text import slugify
from django.db import models
from cloudinary.models import CloudinaryField
from phonenumber_field.modelfields import PhoneNumberField


class Category(models.Model):
    """Category Model Class"""
    title = models.CharField(max_length=255)
    company_in_category = models.ForeignKey(
        'Company',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='+'
        )

    def __str__(self) -> str:
        return self.title

    class Meta:
        """Meta class for ordering by title"""
        ordering = ['title']

class Company(models.Model):
    """Company Model Class"""
    REGISTRATION_STATUS_PENDING = 'Pending'
    REGISTRATION_STATUS_APPROVED = 'Approved'
    REGISTRATION_STATUS_DISAPPROVED = 'Disapproved'
    REGISTRATION_STATUS_CHOICES = [
      (REGISTRATION_STATUS_PENDING, 'Pending'),
      (REGISTRATION_STATUS_APPROVED, 'Approved'),
      (REGISTRATION_STATUS_DISAPPROVED, 'Disapproved')
    ]

    brand_image = CloudinaryField('image', default='placeholder')
    previous_brand_image = models.CharField(max_length=255, null=True, blank=True)
    company_name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255, null=True, blank=True)
    longitude = models.CharField(max_length=255, null=True, blank=True)
    phone = PhoneNumberField()
    entered_phone = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    website = models.CharField(max_length=255, validators=[URLValidator()])
    spots = models.PositiveIntegerField('How many spots or seats?')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True)
    registered_on = models.DateTimeField(auto_now_add=True)
    registration_status = models.CharField(
        max_length=11,
        choices=REGISTRATION_STATUS_CHOICES,
        default=REGISTRATION_STATUS_PENDING
        )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        """Meta class for ordering by company name"""
        ordering = ['company_name']

    def __str__(self) -> str:
        return self.company_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.company_name)
        super(Company, self).save(*args, **kwargs)


class Customer(models.Model):
    """Customer Model Class"""
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = PhoneNumberField()

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'


class Booking(models.Model):
    """Booking Model Class"""
    spots = models.PositiveSmallIntegerField()
    date_time = models.DateTimeField()

    placed_at = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        """Meta class to for booking control"""
        ordering = ['-placed_at']

    def __str__(self) -> str:
        return f'Booking Number {self.id}'

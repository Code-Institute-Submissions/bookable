from django.conf import settings
from django.core.validators import URLValidator
from django.db import models
from cloudinary.models import CloudinaryField


REGISTRATION_STATUS = ((0, 'Pending'), (1, 'Approved'), (2, 'Disapproved'))

class Category(models.Model):
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
        ordering = ['title']

class Company(models.Model):
    brand_image = CloudinaryField('image', default='placeholder')
    company_name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    google_map = models.CharField(max_length=255, validators=[URLValidator()])
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    website = models.CharField(max_length=255, validators=[URLValidator()])
    spots = models.PositiveIntegerField('How many spots or seats?')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True)
    registered_on = models.DateTimeField(auto_now_add=True)
    registration_status = models.IntegerField(choices=REGISTRATION_STATUS, default=0)

    class Meta:
        ordering = ['company_name']

    def __str__(self) -> str:
        return self.company_name


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    company = models.OneToOneField(Company, on_delete=models.CASCADE, primary_key=True)


class Image(models.Model):
    image = CloudinaryField('image', default='placeholder')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'


class Booking(models.Model):
    BOOKING_STATUS_PENDING = 'P'
    BOOKING_STATUS_ACCEPTED = 'A'
    BOOKING_STATUS_REJECTED = 'R'
    BOOKING_STATUS_CHOICES = [
      (BOOKING_STATUS_PENDING, 'Pending'),
      (BOOKING_STATUS_ACCEPTED, 'Accepted'),
      (BOOKING_STATUS_REJECTED, 'Rejected')
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    booking_status = models.CharField(
        max_length=1,
        choices=BOOKING_STATUS_CHOICES,
        default=BOOKING_STATUS_PENDING
        )
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    class Meta:
        permissions = [
                ('reject_booking', 'Can reject booking'),
                ('accept_booking', 'Can accept booking'),
            ]
        ordering = ['-placed_at']

    def __str__(self) -> str:
        return f'Booking Number {self.id}'


class BookingItem(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.PROTECT)
    spot_type_quantity = models.PositiveSmallIntegerField()

    def __str__(self) -> str:
        return f'Booking Item Number {self.id}'

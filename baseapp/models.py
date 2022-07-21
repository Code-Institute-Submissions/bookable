import django
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.

REGISTRATION_STATUS = ((0, 'Pending'), (1, 'Approved'), (2, 'Disapproved'))

class Category(models.Model):
    title = models.CharField(max_length=255)

class Company(models.Model):
    SPOT_TYPE_SEATS = 'SE'
    SPOT_TYPE_SPOTS = 'SP'
    SPOT_CHOICES = [
      (SPOT_TYPE_SEATS, 'SEATS'),
      (SPOT_TYPE_SPOTS, 'SPOTS'),
    ]
    brand_image = CloudinaryField('image', default='placeholder')
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    company = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    description = models.TextField()
    spot_type = models.CharField(
        max_length=2,
        choices=SPOT_CHOICES,
        default=SPOT_TYPE_SEATS
        )
    spots = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    registered_on = models.DateTimeField(auto_now_add=True)
    registration_status = models.IntegerField(choices=REGISTRATION_STATUS, default=0)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return str(self.name)


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    company = models.OneToOneField(Company, on_delete=models.CASCADE, primary_key=True)


class Offer(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    offer_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True)
    last_update = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)


class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)


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


class BookingItem(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.PROTECT)
    offer = models.ForeignKey(Offer, on_delete=models.PROTECT)
    spot_type_quantity = models.PositiveSmallIntegerField()
    offer_price = models.DecimalField(max_digits=6, decimal_places=2)

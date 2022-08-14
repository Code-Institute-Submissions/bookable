from django.conf import settings
from django.core.validators import URLValidator
from django.utils.text import slugify
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import cloudinary
from cloudinary.models import CloudinaryField


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
    google_map = models.CharField(max_length=255, validators=[URLValidator()])
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=255)
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

    class Meta:
        ordering = ['company_name']

    def __str__(self) -> str:
        return self.company_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.company_name)
        super(Company, self).save(*args, **kwargs)


@receiver(pre_delete, sender=Company)
def brand_image_delete(sender, instance, **kwargs):
    cloudinary.uploader.destroy(instance.brand_image.public_id)


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    company = models.OneToOneField(Company, on_delete=models.CASCADE, primary_key=True)


class Image(models.Model):
    image = CloudinaryField('image', default='placeholder')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


@receiver(pre_delete, sender=Image)
def image_delete(sender, instance, **kwargs):
    cloudinary.uploader.destroy(instance.image.public_id)


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

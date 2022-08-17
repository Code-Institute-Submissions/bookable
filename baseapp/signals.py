"""Baseapp Signals"""
from django.db.models.signals import post_delete
from django.dispatch import receiver
import cloudinary
from .models import Company


@receiver(post_delete, sender=Company)
def brand_image_delete_cloudinary(sender, instance, **kwargs):
    """Signal to delete company brand image
       when company object is deleted"""
    cloudinary.uploader.destroy(instance.brand_image.public_id)

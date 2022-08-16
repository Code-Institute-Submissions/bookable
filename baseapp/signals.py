"""Baseapp Signals"""
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import cloudinary
from .models import Company

@receiver(pre_delete, sender=Company)
def company_brand_image_delete(sender, instance, **kwargs):
    """Signal to delete company brand image
       when company object is deleted"""
    cloudinary.uploader.destroy(instance.brand_image.public_id)
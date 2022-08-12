from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Custom Company User"""
    email = models.EmailField(null=True)

    username = models.CharField(
        max_length=255,
        blank=False,
        unique=True
        )

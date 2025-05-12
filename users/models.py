from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Add role choices
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('mechanic', 'Mechanic'),
        ('admin', 'Admin'),
    )
    
    # Add role field
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='customer'
    )
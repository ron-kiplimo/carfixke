from django.db import models

# Create your models here.
from django.db import models
from users.models import User

class Mechanic(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'mechanic'})
    specialties = models.CharField(max_length=200, help_text="e.g., Brakes, Diagnostics, Bodywork")
    certifications = models.TextField(blank=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='mechanic_profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Mechanic"
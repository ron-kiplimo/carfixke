from django.db import models

# Create your models here.
from django.db import models
from mechanics.models import Mechanic

class Garage(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(Mechanic, on_delete=models.CASCADE, related_name='garages')
    address = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    services = models.CharField(max_length=200, help_text="e.g., Oil Change, Tire Services")
    phone = models.CharField(max_length=20, blank=True)
    logo = models.ImageField(upload_to='garage_logos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
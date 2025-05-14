from django.db import models

class Garage(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='garages/', blank=True, null=True)
    location = models.CharField(max_length=200)
    contact = models.CharField(max_length=20)

    def __str__(self):
        return self.name
from django.db import models

class Mechanic(models.Model):
    name = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to='mechanic_profiles/', blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name
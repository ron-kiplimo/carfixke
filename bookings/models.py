from django.db import models
from django.conf import settings
from mechanics.models import Mechanic
from garages.models import Garage

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings',
        limit_choices_to={'role': 'customer'},
    )
    mechanic = models.ForeignKey(
        Mechanic,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bookings',
    )
    garage = models.ForeignKey(
        Garage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bookings',
    )
    booking_date = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(mechanic__isnull=False, garage__isnull=True) | 
                      models.Q(mechanic__isnull=True, garage__isnull=False),
                name='mechanic_or_garage'
            )
        ]

    def __str__(self):
        target = self.mechanic if self.mechanic else self.garage
        return f"Booking by {self.customer.username} for {target} on {self.booking_date}"
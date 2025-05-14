

# Register your models here.
from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer', 'mechanic', 'garage', 'booking_date', 'status')
    list_filter = ('status', 'booking_date')
    search_fields = ('customer__username', 'mechanic__name', 'garage__name')
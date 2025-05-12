# bookings/models.py
from django.db import models
from users.models import User
from mechanics.models import Mechanic
from garages.models import Garage

class TimeSlot(models.Model):
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE, related_name='time_slots')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.mechanic.user.username}: {self.start_time} - {self.end_time}"

class Booking(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'customer'})
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE)
    garage = models.ForeignKey(Garage, on_delete=models.CASCADE, null=True, blank=True)
    time_slot = models.OneToOneField(TimeSlot, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='pending')

    def __str__(self):
        return f"{self.customer.username} - {self.mechanic.user.username} - {self.service_type}"

# bookings/forms.py
from django import forms
from .models import TimeSlot, Booking

class TimeSlotForm(forms.ModelForm):
    class Meta:
        model = TimeSlot
        fields = ['start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['service_type']

# bookings/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from .forms import TimeSlotForm, BookingForm
from .models import TimeSlot, Booking
from mechanics.models import Mechanic

@login_required
def create_time_slot(request):
    if not request.user.is_mechanic():
        messages.error(request, "Only mechanics can create time slots.")
        return redirect('home')

    if request.method == 'POST':
        form = TimeSlotForm(request.POST)
        if form.is_valid():
            time_slot = form.save(commit=False)
            time_slot.mechanic = request.user.mechanic
            time_slot.save()
            messages.success(request, 'Time slot created successfully!')
            return redirect('mechanic_profile', username=request.user.username)
    else:
        form = TimeSlotForm()
    
    return render(request, 'bookings/create_time_slot.html', {'form': form})

def book_service(request, mechanic_id, time_slot_id):
    mechanic = Mechanic.objects.get(id=mechanic_id)
    time_slot = TimeSlot.objects.get(id=time_slot_id)

    if time_slot.is_booked:
        messages.error(request, "This time slot is already booked.")
        return redirect('mechanic_profile', username=mechanic.user.username)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.mechanic = mechanic
            booking.time_slot = time_slot
            booking.save()
            time_slot.is_booked = True
            time_slot.save()

            # Send confirmation email
            send_mail(
                'CarFixKE Booking Confirmation',
                f'Your booking with {mechanic.user.username} for {booking.service_type} on {time_slot.start_time} is confirmed.',
                'from@carfixke.com',
                [booking.customer.email],
                fail_silently=False,
            )

            messages.success(request, 'Booking created successfully!')
            return redirect('booking_confirmation', booking_id=booking.id)
    else:
        form = BookingForm()
    
    return render(request, 'bookings/book_service.html', {
        'form': form,
        'mechanic': mechanic,
        'time_slot': time_slot
    })

def booking_confirmation(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    return render(request, 'bookings/confirmation.html', {'booking': booking})

# bookings/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('time-slot/create/', views.create_time_slot, name='create_time_slot'),
    path('book/<int:mechanic_id>/<int:time_slot_id>/', views.book_service, name='book_service'),
    path('confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
]
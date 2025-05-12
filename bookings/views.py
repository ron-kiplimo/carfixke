from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import TimeSlotForm, BookingForm
from .models import TimeSlot, Booking, Mechanic
from django.core.mail import send_mail

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

def booking_confirmation(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    return render(request, 'bookings/confirmation.html', {'booking': booking})
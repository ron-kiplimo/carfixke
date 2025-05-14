from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Booking
from .forms import BookingForm

@login_required
def create_booking(request):
    if request.user.role != 'customer':
        return HttpResponseForbidden("Only customers can create bookings.")
    if request.method == 'POST':
        form = BookingForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('bookings:booking_list')
    else:
        form = BookingForm(user=request.user)
    return render(request, 'bookings/create_booking.html', {'form': form})

@login_required
def booking_list(request):
    if request.user.role == 'customer':
        bookings = Booking.objects.filter(customer=request.user)
    elif request.user.role == 'mechanic':
        bookings = Booking.objects.filter(mechanic__name=request.user.username)
    elif request.user.role == 'admin':
        bookings = Booking.objects.all()
    else:
        return HttpResponseForbidden("You do not have permission to view bookings.")
    return render(request, 'bookings/booking_list.html', {'bookings': bookings})

@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if not (
        request.user == booking.customer or
        (request.user.role == 'mechanic' and booking.mechanic and booking.mechanic.name == request.user.username) or
        request.user.role == 'admin'
    ):
        return HttpResponseForbidden("You do not have permission to view this booking.")
    return render(request, 'bookings/booking_detail.html', {'booking': booking})

@login_required
def update_booking_status(request, booking_id, status):
    booking = get_object_or_404(Booking, id=booking_id)
    if not (
        (request.user.role == 'mechanic' and booking.mechanic and booking.mechanic.name == request.user.username) or
        request.user.role == 'admin'
    ):
        return HttpResponseForbidden("You do not have permission to update this booking.")
    if status in dict(Booking.STATUS_CHOICES).keys():
        booking.status = status
        booking.save()
    return redirect('bookings:booking_list')
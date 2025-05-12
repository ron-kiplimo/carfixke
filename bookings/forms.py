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
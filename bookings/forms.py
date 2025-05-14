from django import forms
from .models import Booking
from mechanics.models import Mechanic
from garages.models import Garage
from django.utils import timezone

class BookingForm(forms.ModelForm):
    book_mechanic = forms.BooleanField(
        label="Book a Mechanic (uncheck to book a Garage)",
        required=False,
        initial=True
    )
    mechanic = forms.ModelChoiceField(
        queryset=Mechanic.objects.all(),
        required=False,
        empty_label="Select a Mechanic"
    )
    garage = forms.ModelChoiceField(
        queryset=Garage.objects.all(),
        required=False,
        empty_label="Select a Garage"
    )

    class Meta:
        model = Booking
        fields = ['mechanic', 'garage', 'booking_date']
        widgets = {
            'booking_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user and self.user.role != 'customer':
            raise forms.ValidationError("Only customers can create bookings.")

    def clean_booking_date(self):
        booking_date = self.cleaned_data['booking_date']
        if booking_date < timezone.now():
            raise forms.ValidationError("Booking date cannot be in the past.")
        return booking_date

    def clean(self):
        cleaned_data = super().clean()
        book_mechanic = cleaned_data.get('book_mechanic')
        mechanic = cleaned_data.get('mechanic')
        garage = cleaned_data.get('garage')

        if book_mechanic:
            if not mechanic:
                self.add_error('mechanic', "Please select a mechanic.")
            cleaned_data['garage'] = None
        else:
            if not garage:
                self.add_error('garage', "Please select a garage.")
            cleaned_data['mechanic'] = None

        return cleaned_data

    def save(self, commit=True):
        booking = super().save(commit=False)
        booking.customer = self.user
        if commit:
            booking.save()
        return booking
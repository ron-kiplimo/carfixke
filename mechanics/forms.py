from django import forms
from .models import Mechanic

class MechanicProfileForm(forms.ModelForm):
    class Meta:
        model = Mechanic
        fields = ['specialties', 'certifications', 'hourly_rate', 'bio', 'profile_image']
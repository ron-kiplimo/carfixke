from django import forms
from .models import Garage

class GarageForm(forms.ModelForm):
    class Meta:
        model = Garage
        fields = ['name', 'address', 'latitude', 'longitude', 'services', 'phone', 'logo']
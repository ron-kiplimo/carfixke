from django.shortcuts import render
from .models import Garage

def garages_home(request):
    garages = Garage.objects.all()
    return render(request, 'garages/garages_home.html', {'garages': garages})
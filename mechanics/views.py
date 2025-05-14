from django.shortcuts import render
from .models import Mechanic



def home(request):
    mechanics = Mechanic.objects.all()
    return render(request, 'mechanics/mechanics_home.html', {'mechanics': mechanics})

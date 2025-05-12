from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import GarageForm
from .models import Garage
from django.contrib import messages

@login_required
def create_garage(request):
    if not request.user.is_mechanic():
        messages.error(request, "Only mechanics can create garages.")
        return redirect('home')

    if request.method == 'POST':
        form = GarageForm(request.POST, request.FILES)
        if form.is_valid():
            garage = form.save(commit=False)
            garage.owner = request.user.mechanic
            garage.save()
            messages.success(request, 'Garage created successfully!')
            return redirect('garage_detail', garage_id=garage.id)
    else:
        form = GarageForm()
    
    return render(request, 'garages/create_garage.html', {'form': form})

def garage_detail(request, garage_id):
    garage = Garage.objects.get(id=garage_id)
    return render(request, 'garages/detail.html', {'garage': garage})
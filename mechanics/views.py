from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import MechanicProfileForm
from .models import Mechanic
from django.contrib import messages


def home(request):
    return render(request, 'mechanics/home.html')  # This path is correct



@login_required
def create_mechanic_profile(request):
    if not request.user.is_mechanic():
        messages.error(request, "Only mechanics can create profiles.")
        return redirect('home')
    
    try:
        mechanic = request.user.mechanic
    except Mechanic.DoesNotExist:
        mechanic = None

    if request.method == 'POST':
        form = MechanicProfileForm(request.POST, request.FILES, instance=mechanic)
        if form.is_valid():
            mechanic = form.save(commit=False)
            mechanic.user = request.user
            mechanic.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('mechanic_profile', username=request.user.username)
    else:
        form = MechanicProfileForm(instance=mechanic)
    
    return render(request, 'mechanics/create_profile.html', {'form': form})

def mechanic_profile(request, username):
    mechanic = Mechanic.objects.get(user__username=username)
    return render(request, 'mechanics/profile.html', {'mechanic': mechanic})
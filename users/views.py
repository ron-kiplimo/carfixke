from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from django.shortcuts import redirect

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after registration
            login(request, user)
            # Redirect based on role
            if user.role == 'mechanic':
                return redirect('mechanics:mechanics_home')
            elif user.role == 'admin':
                return redirect('admin:index')
            else:  # customer
                return redirect('mechanics:mechanics_home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect based on role
            if user.role == 'mechanic':
                return redirect('mechanics:mechanics_home')
            elif user.role == 'admin':
                return redirect('admin:index')
            else:  # customer
                return redirect('mechanics:mechanics_home')
        else:
            return render(request, 'users/login.html', {'error': 'Invalid credentials'})
    return render(request, 'users/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('mechanics:mechanics_home')

@login_required
def profile(request):
    return render(request, 'users/profile.html', {'user': request.user})


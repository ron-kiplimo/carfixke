
from django.shortcuts import redirect
from django.contrib.auth import logout

def user_logout(request):
    logout(request)
    return redirect('mechanics')  # instead of 'home'

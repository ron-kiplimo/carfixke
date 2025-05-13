from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')  # Assumes a home.html template
    # Or use a simple response for testing:
    # return HttpResponse("Welcome to CarFixKE!")
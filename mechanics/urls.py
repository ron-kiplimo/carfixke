
from django.urls import path
from . import views

app_name = 'mechanics'  # This sets the namespace

urlpatterns = [
    path('', views.home, name='mechanics_home'),  # This name must match
]

from django.urls import path
from . import views

app_name = 'garages'
urlpatterns = [
    path('', views.garages_home, name='garages_home'),
]
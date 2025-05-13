from django.urls import path
from . import views

app_name = 'reviews'
urlpatterns = [
    path('', views.some_view, name='some_view_name'),
    # Add other URL patterns here
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/create/', views.create_mechanic_profile, name='create_mechanic_profile'),
    path('profile/<str:username>/', views.mechanic_profile, name='mechanic_profile'),
]

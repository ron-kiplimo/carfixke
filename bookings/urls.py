from django.urls import path
from . import views

urlpatterns = [
    path('time-slot/create/', views.create_time_slot, name='create_time_slot'),
    path('book/<int:mechanic_id>/<int:time_slot_id>/', views.book_service, name='book_service'),
    path('confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
]
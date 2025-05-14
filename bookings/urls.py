from django.urls import path
from . import views

app_name = 'bookings'
urlpatterns = [
    path('create/', views.create_booking, name='create_booking'),
    path('', views.booking_list, name='booking_list'),
    path('<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('<int:booking_id>/status/<str:status>/', views.update_booking_status, name='update_booking_status'),
]
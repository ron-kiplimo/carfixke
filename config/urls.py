from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bookings/', include('bookings.urls')),
    path('garages/', include('garages.urls')),
    path('mechanics/', include('mechanics.urls')),
    path('reviews/', include('reviews.urls')),
    path('users/', include('users.urls')),
]
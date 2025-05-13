from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/mechanics/', permanent=False), name='home'),  # Redirect to mechanics
    path('admin/', admin.site.urls),
    path('bookings/', include('bookings.urls')),
    path('garages/', include('garages.urls')),
    path('mechanics/', include('mechanics.urls')),
    path('reviews/', include('reviews.urls')),
    path('users/', include('users.urls')),
]
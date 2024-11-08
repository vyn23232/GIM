# gym_management1/urls.py
from django.contrib import admin
from django.urls import path, include  # Import include to include app URLs

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),  # Include URLs from the accounts app
]

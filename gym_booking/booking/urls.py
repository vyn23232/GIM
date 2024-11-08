from django.urls import path
from . import views

urlpatterns = [
    path('', views.booking_home, name='booking_home'),  # Root of booking/
    path('schedule/', views.trainer_schedule, name='trainer_schedule'),
    path('book/', views.book_trainer, name='book_trainer'),
]

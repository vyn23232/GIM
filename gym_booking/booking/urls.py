from django.urls import path
from . import views

urlpatterns = [
    path('schedule/', views.trainer_schedule, name='trainer_schedule'),
    path('book/', views.book_trainer, name='book_trainer'),
    
]
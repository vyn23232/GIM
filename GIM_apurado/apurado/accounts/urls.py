from django.urls import path
from .views import (
    register, profile_view, membership_management, add_user,
    payment_options, credit_card,
    login_view, home_view, about_view, about2_view,
    process_credit_card_payment, payment_confirmation, payment_error, benefits, home2,
    book_trainer, trainer_schedule, payment_success, dashboard, logout_view, change_password
)
from . import views
urlpatterns = [
    # Home view
    path('', home_view, name='home'),  # Root URL for the homepage
    path('login/', login_view, name='login'),

    # Home2 page
    path('home2/', home2, name='home2'),  # URL for home2 page

    # User management URLs
    path('register/', register, name='register'),
    path('profile/', profile_view, name='profile'),
    path('membership/', membership_management, name='membership_management'),
    path('add_user/', add_user, name='add_user'),

    # Payment-related views
    path('payment/', payment_options, name='payment_options'),
    path('credit/', credit_card, name='credit_card'),
    path('process_credit_card_payment/', process_credit_card_payment, name='process_credit_card_payment'),
    path('payment_confirmation/', payment_confirmation, name='payment_confirmation'),
    path('payment_error/', payment_error, name='payment_error'),

    # Informational views
    path('about/', about_view, name='about'),
    path('about2/', about2_view, name='about2'),
    path('benefits/', benefits, name='benefits'),

    # Trainer-related views
    path('book_trainer/', book_trainer, name='book_trainer'),
    path('trainer_schedule/', trainer_schedule, name='trainer_schedule'),
    path('payment_success/', payment_success, name='payment_success'),
    path('dashboard/', dashboard, name='dashboard'),
    path('book_trainer/', views.book_trainer, name='book_trainer'),
    path('trainer_schedule/', views.trainer_schedule, name='trainer_schedule'),
    path('trainer_schedule/<int:trainer_id>/', views.trainer_schedule, name='trainer_schedule'),
    path('trainer_schedule/<int:trainer_id>/', views.trainer_schedule, name='trainer_schedule_trainer'), 

    
    # Logout view
    path('logout/', logout_view, name='logout'),

    # Change password view
    path('change_password/', change_password, name='change_password'),
]

from django.urls import path
from .views import (
    register, profile_view, membership_management, add_user,  # Updated profile import
    payment_options, credit_card, paypal, bank_transfer,
    login_view, home_view, about_view,
    process_credit_card_payment, payment_confirmation, payment_error, dashboard_view, benefits, home2,
    book_trainer, trainer_schedule
)

urlpatterns = [
    # Home view
    path('', home_view, name='home'),  # Root URL for the homepage
    path('login/', login_view, name='login'),

    # Add this line for the home2 page:
    path('home2/', home2, name='home2'),  # URL for home2 page

    # User management URLs
    path('register/', register, name='register'),
    path('profile/', profile_view, name='profile'),  # Use the updated profile view function
    path('membership/', membership_management, name='membership_management'),
    path('add_user/', add_user, name='add_user'),

    # Payment-related views
    path('payment/', payment_options, name='payment_options'),
    path('credit/', credit_card, name='credit_card'),
    path('process_credit_card_payment/', process_credit_card_payment, name='process_credit_card_payment'),
    path('payment_confirmation/', payment_confirmation, name='payment_confirmation'),
    path('payment_error/', payment_error, name='payment_error'),
    path('paypal/', paypal, name='paypal'),
    path('bank/', bank_transfer, name='bank_transfer'),

    # Authentication-related views
    #path('forgot_password/', forgot_password, name='forgot_password'),
    #path('send_reset_link/', send_reset_link, name='send_reset_link'),

    # Informational views
    path('about/', about_view, name='about'),
    path('benefits/', benefits, name='benefits'),

    # Dashboard view
    path('dashboard/', dashboard_view, name='dashboard_view'),

    # Booking trainer view
    path('book_trainer/', book_trainer, name='book_trainer'),
    path('trainer_schedule/', trainer_schedule, name='trainer_schedule'),
]

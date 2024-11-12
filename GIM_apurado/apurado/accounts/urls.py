from django.urls import path
from .views import (
    register, profile, membership_management, add_user, 
    payment_options, credit_card, paypal, bank_transfer, 
    login_view, forgot_password, send_reset_link, home_view, about_view,
    process_credit_card_payment, payment_confirmation, payment_error, dashboard_view
)

urlpatterns = [
    # Home view - this will direct to the homepage
    path('', home_view, name='home'),  # Root URL (home)

    # User management URLs
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
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

    # TOVI's URLs
    path('login/', login_view, name='login'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('send_reset_link/', send_reset_link, name='send_reset_link'),
    path('about/', about_view, name='about'),
    path('dashboard/', dashboard_view, name='dashboard'),  # Dashboard URL
    # SACEDA'S URLs
    # Other views can be added below
]

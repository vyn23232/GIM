from django.urls import path
from .views import (
    register, profile, membership_management, add_user, 
    payment_options, credit_card, paypal, bank_transfer, 
    login_view, forgot_password, send_reset_link,
    process_credit_card_payment, payment_confirmation, payment_error  # New views
)

urlpatterns = [
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('membership/', membership_management, name='membership_management'),
    path('add_user/', add_user, name='add_user'),
    path('payment/', payment_options, name='payment_options'), 
    path('credit/', credit_card, name='credit_card'),
    path('process_credit_card_payment/', process_credit_card_payment, name='process_credit_card_payment'),  # New URL
    path('payment_confirmation/', payment_confirmation, name='payment_confirmation'),  # New URL
    path('payment_error/', payment_error, name='payment_error'),  # New URL
    path('paypal/', paypal, name='paypal'),
    path('bank/', bank_transfer, name='bank_transfer'),
    
    # TOVI'S URLs
    path('login/', login_view, name='login'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('send_reset_link/', send_reset_link, name='send_reset_link'),
]

from django.urls import path
from django.views.generic import TemplateView
from .views import register, profile, membership_management, add_user, login_view, forgot_password, send_reset_link, reset_password  # Import the necessary views

urlpatterns = [
    path('register/', register, name='register'),  # Registration page
    path('profile/', profile, name='profile'),  # User profile page
    path('membership/', membership_management, name='membership_management'),  # Membership management page
    path('add_user/', add_user, name='add_user'),  # Add user page
    path('login/', login_view, name='login'),  # Login page
    path('forgot_password/', forgot_password, name='forgot_password'),  # Forgot password page
    path('send_reset_link/', send_reset_link, name='send_reset_link'),
    path('reset-password/', reset_password, name='reset_password'),  # Update: no user_id parameter
    path('email_sent/', TemplateView.as_view(template_name='accounts/email_sent.html'), name='email_sent'),
]

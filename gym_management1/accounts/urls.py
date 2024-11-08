from django.urls import path
from .views import home_view, login_view, register_view, ForgotPasswordView, send_reset_link, reset_password, about_view

urlpatterns = [
    path('', home_view, name='home'),
    path('about/', about_view, name='about'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),  # Added route for registration
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('send-reset-link/', send_reset_link, name='send_reset_link'),
    path('reset-password/<int:user_id>/', reset_password, name='reset_password'),
]

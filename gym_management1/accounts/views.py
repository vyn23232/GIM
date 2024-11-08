from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.views import View

# Home view
def home_view(request):
    return render(request, 'accounts/home.html')

# About view
def about_view(request):
    return render(request, 'accounts/about.html')

# Login view
def login_view(request):
    return render(request, 'accounts/login.html')

# Registration view
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'accounts/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'accounts/register.html')

        # Create new user
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password)  # Hash the password
        )
        messages.success(request, 'Account created successfully! You can log in now.')
        return redirect('login')

    return render(request, 'accounts/register.html')

# Forgot password view
class ForgotPasswordView(View):
    def get(self, request):
        return render(request, 'accounts/forgot_password.html')

# Send reset link view
def send_reset_link(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = User.objects.get(email=email)
            reset_link = f'http://127.0.0.1:8000/reset-password/{user.id}/'
            
            send_mail(
                'Password Reset Request',
                f'Click the link below to reset your password:\n\n{reset_link}',
                'admin@example.com',
                [email],
                fail_silently=False,
            )
            messages.success(request, 'A reset link has been sent to your email.')
            return render(request, 'accounts/email_sent.html')
            
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email.')
            return render(request, 'accounts/send_reset_link.html')

    return render(request, 'accounts/send_reset_link.html')

# Reset password view
def reset_password(request, user_id):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            try:
                user = User.objects.get(pk=user_id)
                user.password = make_password(new_password)
                user.save()
                messages.success(request, 'Password successfully reset! You can now log in.')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'User not found.')
                return redirect('send_reset_link')
        else:
            messages.error(request, 'Passwords do not match!')

    return render(request, 'accounts/reset_password.html', {'user_id': user_id})

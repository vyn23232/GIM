from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login  # Import authenticate and login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail

def register(request):
    if request.method == 'POST':
        pass
    return render(request, 'accounts/register.html')

def profile(request):
    return render(request, 'accounts/profile.html')

def membership_management(request):
    users = User.objects.all() 
    return render(request, 'accounts/membership_management.html', {'users': users})

def add_user(request):
    if request.method == 'POST':
        name = request.POST['name']
        mobile = request.POST['mobile']
        email = request.POST['email']
        gym_class = request.POST['gym_class']
        User.objects.create(name=name, mobile=mobile, email=email, gym_class=gym_class)
        return redirect('membership_management')
    return HttpResponse(status=405)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profile')  # Redirect to the profile or another page after login
        else:
            error = "Invalid username or password."
            return render(request, 'accounts/login.html', {'error': error})

    return render(request, 'accounts/login.html')  # Render the login template for GET requests

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print(f"Email submitted: {email}")  # Debug print statement
        # Logic to send the password reset link would go here
        return redirect('send_reset_link')  # Redirect to the send reset link page
    print("GET request or no email submitted")  # Debug print statement
    return render(request, 'accounts/forgot_password.html')  # Render the forgot password template for GET requests

# Send reset link view
def send_reset_link(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = User.objects.get(email=email)
            # Logic to generate a reset link
            reset_link = f'http://yourdomain.com/reset-password/{user.id}/'
            
            send_mail(
                'Password Reset Request',
                f'Click the link below to reset your password:\n\n{reset_link}',
                'admin@example.com',
                [email],
                fail_silently=False,
            )
            messages.success(request, 'A reset link has been sent to your email.')
            return render(request, 'accounts/email_sent.html')  # Updated path
            
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email.')
            return render(request, 'accounts/send_reset_link.html')  # Updated path

    return render(request, 'accounts/send_reset_link.html')  # Updated path

def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            try:
                user = User.objects.get(email=email)
                user.password = make_password(new_password)
                user.save()
                messages.success(request, 'Password successfully reset! You can now log in.')
                return redirect('login')  # Redirect to the login page after success
            except User.DoesNotExist:
                messages.error(request, 'User with this email does not exist.')
                return redirect('send_reset_link')  # Redirect if user not found
        else:
            messages.error(request, 'Passwords do not match!')

    return render(request, 'accounts/reset_password.html')  # Adjust this template name accordingly

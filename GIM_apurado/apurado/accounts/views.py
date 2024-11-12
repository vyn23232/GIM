from django.shortcuts import render, redirect
from .models import User, Dashboard, Booking, Payment
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login

# Existing views

def register(request):
    if request.method == 'POST':
        pass  # Handle registration logic
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

# Payment-related views
def payment_options(request):
    return render(request, 'accounts/payment_options.html')

def credit_card(request):
    return render(request, 'accounts/credit_card.html')

def paypal(request):
    return render(request, 'accounts/paypal.html')

def bank_transfer(request):
    return render(request, 'accounts/bank_transfer.html')

# TOVI'S VIEWS

# Home view
def home_view(request):
    return render(request, 'accounts/home.html')

# About view
def about_view(request):
    return render(request, 'accounts/about.html')

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

def process_credit_card_payment(request):
    if request.method == 'POST':
        # Process payment logic
        payment_success = True  # Example variable; replace with actual payment processing

        if payment_success:
            messages.success(request, "Payment successful!")
            return render(request, 'accounts/payment_confirmation.html')
        else:
            messages.error(request, "Payment failed. Please try again.")
            return render(request, 'accounts/payment_error.html')

    return redirect('credit_card') 

# Payment confirmation view
def payment_confirmation(request):
    return render(request, 'accounts/payment_confirmation.html')

# Payment error view
def payment_error(request):
    return render(request, 'accounts/payment_error.html')

# Dashboard view for logged-in users
@login_required
def dashboard_view(request):
    user = request.user  # Get the logged-in user

    try:
        # Get the user's dashboard data (assuming one-to-one relationship with Dashboard)
        dashboard = Dashboard.objects.get(user=user)
        
        # Get upcoming bookings for the user (assuming status 'upcoming' for pending bookings)
        upcoming_bookings = Booking.objects.filter(user=user, status='upcoming')

        # Get payment history (sorted by most recent)
        payment_history = Payment.objects.filter(attendance__user=user).order_by('-payment_date')

        # Pass data to the template
        return render(request, 'accounts/dashboard.html', {
            'dashboard': dashboard,
            'upcoming_bookings': upcoming_bookings,
            'payment_history': payment_history,
        })

    except Dashboard.DoesNotExist:
        # If no dashboard is found for the user, redirect them with an error message
        messages.error(request, "Dashboard not found. Please contact support.")
        return redirect('home_view')  # Redirect to home or another page

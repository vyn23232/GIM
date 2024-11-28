from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import User, Dashboard, Booking, Payment
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

def home2(request):
    return render(request, 'accounts/home2.html')
# Register view
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        email = request.POST.get('email')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')

        # Check if passwords match
        if password != password_confirm:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('register')

        # Save user
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=firstname,
            last_name=lastname,
        )

        # Automatically log in the user after registration
        login(request, user)

        messages.success(request, "Registration successful!")
        return redirect('dashboard_view')

    return render(request, 'accounts/register.html')


# Login view


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log the user in
            login(request, user)

            # Redirect to the home page
            return redirect('home2')  # Redirect to the home page
        else:
            # Authentication failed
            messages.error(request, "Invalid username or password.")
            return redirect('login')  # Redirect back to the login page
    else:
        # Render the login page
        return render(request, 'accounts/login.html')

# Profile view
@login_required
def profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = get_object_or_404(User, user_id=user_id)
    return render(request, 'accounts/profile.html', {'user': user})


# Dashboard view
@login_required
def dashboard_view(request):
    # Get user_id from session
    user_id = request.session.get('user_id')
    
    if not user_id:
        return redirect('login')  # Redirect to login if user_id is not found in session

    try:
        # Fetch the User instance based on the user_id from the session
        user = get_object_or_404(User, id=user_id)

        # Fetch the user's dashboard using the User instance
        dashboard = Dashboard.objects.get(user=user)

        # Get the upcoming bookings and payment history related to the user
        upcoming_bookings = Booking.objects.filter(user=user, status='upcoming')
        payment_history = Payment.objects.filter(attendance__user=user).order_by('-payment_date')

        # Ensure only relevant data is passed to the template
        return render(request, 'accounts/dashboard.html', {
            'dashboard_data': dashboard,  # Pass the dashboard data
            'upcoming_bookings': upcoming_bookings,
            'payment_history': payment_history,
        })
    
    except Dashboard.DoesNotExist:
        # Handle the case where the Dashboard does not exist for the user
        messages.error(request, "Dashboard not found. Please contact support.")
        return redirect('home_view')
    except User.DoesNotExist:
        # Handle case where User with the given ID is not found
        messages.error(request, "User not found. Please log in again.")
        return redirect('login')




# Membership management view
def membership_management(request):
    users = User.objects.all()
    return render(request, 'accounts/membership_management.html', {'users': users})


# Add user view
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


def process_credit_card_payment(request):
    if request.method == 'POST':
        payment_success = True  # Placeholder logic
        if payment_success:
            messages.success(request, "Payment successful!")
            return render(request, 'accounts/payment_confirmation.html')
        else:
            messages.error(request, "Payment failed. Please try again.")
            return render(request, 'accounts/payment_error.html')
    return redirect('credit_card')


def payment_confirmation(request):
    return render(request, 'accounts/payment_confirmation.html')


def payment_error(request):
    return render(request, 'accounts/payment_error.html')


# Home view
def home_view(request):
    return render(request, 'accounts/home.html')


# About view
def about_view(request):
    return render(request, 'accounts/about.html')

# Gym Benefits
def benefits(request):
    return render(request, 'accounts/gym_benefits.html')

# Forgot password view
#def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Logic to send the password reset link would go here
        return redirect('send_reset_link')
    return render(request, 'accounts/forgot_password.html')


# Send reset link view
#def send_reset_link(request):
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
            return render(request, 'accounts/email_sent.html')
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email.')
            return render(request, 'accounts/send_reset_link.html')

    return render(request, 'accounts/send_reset_link.html')

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User, Dashboard, Booking, Payment, Class
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from .models import Trainer, Booking, Exercise
from django.contrib.auth.models import User
from datetime import date, timedelta
from .forms import BookingForm
from django.contrib.auth import get_user

@login_required
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
        return redirect('login')

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
            # Render the login page with the error message
            return render(request, 'accounts/login.html')
    else:
        # Render the login page
        return render(request, 'accounts/login.html')
    
# Logout view
def logout_view(request):
    # Log the user out
    logout(request)
    return redirect('login')  # Redirect to the login page    

# Profile view
@login_required
def profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = get_object_or_404(User, user_id=user_id)
    return render(request, 'accounts/profile.html', {'user': user})

def profile_view(request):
    # The authenticated user is already available via `request.user`
    return render(request, 'accounts/profile.html', {'user': request.user})

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
        logout(request)  # Log the user out
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

def about2_view(request):
    return render(request, 'accounts/about2.html')

# Gym Benefits
def benefits(request):
    return render(request, 'accounts/gym_benefits.html')


@login_required
def user_bookings(request):
    # Fetch bookings for the logged-in user
    bookings = Booking.objects.filter(user=request.user).order_by('date', 'time')
    
    return render(request, 'accounts/user_bookings.html', {'bookings': bookings})

@login_required
def trainer_schedule(request, trainer_id=None):
    # Check if a trainer_id is provided, otherwise, show the user's own bookings
    if trainer_id:
        try:
            trainer = Trainer.objects.get(id=trainer_id)
            # Fetch bookings for this specific trainer
            bookings = Booking.objects.filter(trainer=trainer).order_by('date', 'time')
        except Trainer.DoesNotExist:
            return render(request, 'error.html', {'message': 'Trainer not found.'})
    else:
        # Fetch all bookings for the logged-in user (this is the user's schedule)
        bookings = Booking.objects.filter(user=request.user).order_by('date', 'time')
    
    return render(request, 'accounts/trainer_schedule.html', {'bookings': bookings})


@login_required  # Ensure the user is authenticated
def book_trainer(request):
    if request.method == 'POST':
        trainer_id = request.POST.get('trainer_id')
        exercise_id = request.POST.get('exercise_id')
        date = request.POST.get('date')
        time = request.POST.get('time')
        
        try:
            # Fetch the trainer and exercise objects
            trainer = Trainer.objects.get(id=trainer_id)
            exercise = Exercise.objects.get(id=exercise_id)
        except Trainer.DoesNotExist:
            messages.error(request, "Trainer not found!")
            return redirect('book_trainer')
        except Exercise.DoesNotExist:
            messages.error(request, "Exercise not found!")
            return redirect('book_trainer')
        
        # Explicitly fetch the user instance by ID (this may not be necessary)
        user_instance = User.objects.get(id=request.user.id)
        
        # Check if the trainer is already booked for the selected time slot
        if Booking.objects.filter(trainer=trainer, date=date, time=time).exists():
            messages.error(request, "This trainer is already booked for the selected time.")
            return redirect('book_trainer')
        
        # Create and save the booking
        booking = Booking(
            user=user_instance,  # Now explicitly using the user_instance
            trainer=trainer,
            exercise=exercise,
            date=date,
            time=time
        )
        booking.save()

        # Display a success message
        messages.success(request, "Your booking was successful!")
        
        # Redirect to the trainer schedule page
        return redirect('trainer_schedule')
    
    # If the method is GET, show the booking form with the list of trainers and exercises
    trainers = Trainer.objects.all()
    exercises = Exercise.objects.all()
    return render(request, 'accounts/book_trainer.html', {'trainers': trainers, 'exercises': exercises})


@login_required
def trainer_schedule(request):
    # Fetch all bookings for the logged-in user
    bookings = Booking.objects.filter(user=request.user).order_by('date', 'time')
    
    # If the user has no bookings, display a message
    if not bookings:
        messages.info(request, "You have no upcoming bookings.")
    
    return render(request, 'accounts/trainer_schedule.html', {'bookings': bookings})
@login_required
def payment_success(request):
    user = request.user
    payment_method = request.GET.get('paymentMethod')
    payment_date = request.GET.get('paymentDate')
    membership_type = request.GET.get('plan')
    amount_due = calculate_amount_due(membership_type)

    # Save payment data, for example in the session or database
    request.session['payment_info'] = {
        'name': user.first_name,
        'membership_type': membership_type,
        'amount_due': amount_due,
        'payment_method': payment_method,
        'payment_date': payment_date,
    }

    # Redirect to dashboard
    return redirect('dashboard')

def calculate_amount_due(membership_type):
    if membership_type == 'Basic':
        return 29.00
    elif membership_type == 'Premium':
        return 49.00
    elif membership_type == 'VIP':
        return 79.00
    return 0.00

# Dashboard view to display payment data
@login_required
def dashboard(request):
    payment_data = request.session.get('payment_data', {})
    context = {
        'user': request.user,
        'plan': payment_data.get('plan', 'N/A'),
        'payment_method': payment_data.get('payment_method', 'N/A'),
        'payment_date': payment_data.get('payment_date', 'N/A'),
    }
    return render(request, 'accounts/dashboard.html', context)

def payment_success(request):
    if request.method == 'GET':
        plan = request.GET.get('plan', '')
        payment_method = request.GET.get('paymentMethod', '')
        payment_date = request.GET.get('paymentDate', now().date())

        # Save payment data to session for the dashboard
        request.session['payment_data'] = {
            'plan': plan,
            'payment_method': payment_method,
            'payment_date': payment_date,
        }
        return render(request, 'accounts/payment_success.html', {
            'user': request.user,
            'plan': plan,
            'payment_method': payment_method,
            'payment_date': payment_date,
        })
    return redirect('payment_options')  # Redirect if accessed incorrectly

@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('currentPassword')
        new_password = request.POST.get('newPassword')
        confirm_password = request.POST.get('confirmPassword')

        if new_password == confirm_password:
            if request.user.check_password(current_password):
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)  # Important to keep the user logged in
                messages.success(request, 'Your password was successfully updated!')
            else:
                messages.error(request, 'Current password is incorrect.')
        else:
            messages.error(request, 'New passwords do not match.')

    return redirect('profile')
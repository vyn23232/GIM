
from django.shortcuts import render, redirect
from .models import Trainer, Booking, Exercise
from .forms import BookingForm
from django.contrib.auth.models import User
from datetime import date, timedelta



def trainer_schedule(request):
    trainers = Trainer.objects.all()
    today = date.today()
    week_days = [today + timedelta(days=i) for i in range(7)]


    schedule = {}

    for trainer in trainers:
        trainer_bookings = Booking.objects.filter(trainer=trainer, date__in=week_days)
        trainer_schedule = {day: [] for day in week_days}

        # Assign booked times for each day
        for booking in trainer_bookings:
            trainer_schedule[booking.date].append(booking.time)


        schedule[trainer] = trainer_schedule

    return render(request, 'booking/trainer_schedule.html', {
        'schedule': schedule, 
        'week_days': week_days
    })

def book_trainer(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            # Manually set the user to the currently logged-in user
            if request.user.is_authenticated:
                booking.user = request.user
            else:
                # Default to user with ID 1 if no user is logged in
                booking.user = User.objects.get(id=1)

            booking.save()
            # Redirect to the trainer schedule page after booking
            return redirect('trainer_schedule')  # Redirect to the 'trainer_schedule' URL pattern
    else:
        form = BookingForm()

    return render(request, 'booking/book_trainer.html', {'form': form})
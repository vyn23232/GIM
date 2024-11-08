from django.shortcuts import render, redirect
from .models import Trainer, Booking
from datetime import date, timedelta
from .forms import BookingForm

def booking_home(request):
    return render(request, 'booking/booking_home.html')

def home(request):
    return render(request, 'booking/home.html')

def trainer_schedule(request):
    trainers = Trainer.objects.all()
    today = date.today()
    week_days = [today + timedelta(days=i) for i in range(7)]
    schedule = {}

    for trainer in trainers:
        trainer_bookings = Booking.objects.filter(trainer=trainer, date__in=week_days)
        trainer_schedule = {day: [] for day in week_days}

        for booking in trainer_bookings:
            trainer_schedule[booking.date].append(booking.time)

        # Only include trainers who have bookings
        if any(trainer_schedule.values()):
            schedule[trainer] = trainer_schedule
    
    return render(request, 'booking/trainer_schedule.html', {'schedule': schedule, 'week_days': week_days})

# View for booking a trainer
def book_trainer(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('trainer_schedule')  # Redirect to the schedule view
    else:
        form = BookingForm()
    return render(request, 'booking/book_trainer.html', {'form': form})

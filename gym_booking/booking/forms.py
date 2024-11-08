from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    time = forms.TimeField(input_formats=['%I:%M %p', '%H:%M'])  # Accepts 12-hour (e.g., 12:30 PM) and 24-hour formats (e.g., 14:30)

    class Meta:
        model = Booking
        fields = ['trainer', 'exercise', 'date', 'time']

    # Optional: Validation to prevent double-booking
    def clean(self):
        cleaned_data = super().clean()  
        trainer = cleaned_data.get('trainer')
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')

        if Booking.objects.filter(trainer=trainer, date=date, time=time).exists():
            raise forms.ValidationError("This trainer is already booked for the selected time.")
        return cleaned_data

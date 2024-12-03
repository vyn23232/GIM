from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['trainer', 'exercise', 'date', 'time']

    widgets = {
        'date': forms.SelectDateWidget(),
        'time': forms.TextInput(attrs={'placeholder': 'Enter time (e.g., 3:30 PM)'}),
    }

    def clean(self):
        cleaned_data = super().clean()
        trainer = cleaned_data.get('trainer')
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')

        # Check if the trainer is already booked for the selected time
        if trainer and date and time:
            if Booking.objects.filter(trainer=trainer, date=date, time=time).exists():
                raise forms.ValidationError("This trainer is already booked for the selected time.")

        return cleaned_data

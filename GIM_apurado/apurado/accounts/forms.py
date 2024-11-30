from django import forms
from .models import Class

class BookTrainerForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your full name',
            'class': 'form-control',
        }),
        label="Full Name"
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email address',
            'class': 'form-control',
        }),
        label="Email Address"
    )
    date = forms.DateField(
        widget=forms.SelectDateWidget(attrs={
            'class': 'form-control',
        }),
        label="Preferred Date"
    )
    time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'placeholder': 'HH:MM (24-hour format)',
            'type': 'time',  # Use HTML5 time input
            'class': 'form-control',
        }),
        label="Preferred Time"
    )
    class_id = forms.ModelChoiceField(
        queryset=Class.objects.all(),
        label="Class",
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    status = forms.CharField(
        widget=forms.HiddenInput(),
        initial='Pending'
    )

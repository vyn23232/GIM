# forms.py
from django import forms
from .models import Class

class BookTrainerForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    date = forms.DateField(widget=forms.SelectDateWidget)
    time = forms.TimeField(widget=forms.TimeInput)
    class_id = forms.ModelChoiceField(queryset=Class.objects.all(), label="Class")
    status = forms.CharField(widget=forms.HiddenInput(), initial='Pending')
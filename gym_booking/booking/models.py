# booking/models.py
from django.db import models
from django.contrib.auth.models import User

class Trainer(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Allow NULL values
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

    class Meta:
        unique_together = ('trainer', 'date', 'time')

    def __str__(self):
        return f"{self.trainer.name} booked for {self.exercise.name} on {self.date} at {self.time}"

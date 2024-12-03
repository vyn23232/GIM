from django.db import models
from django.contrib.auth.models import User

class Trainer(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)  # e.g., "Yoga", "Strength Training"
    availability = models.JSONField(default=dict)  # Can store available days/times

    def __str__(self):
        return f"{self.name} ({self.specialty})"

class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)  # Consistent with form
    date = models.DateField()
    time = models.TimeField()

    class Meta:
        unique_together = ('trainer', 'date', 'time')  # Prevent double-booking of trainers

    def __str__(self):
        return f"{self.user.username} booked {self.trainer.name} for {self.exercise.name} on {self.date} at {self.time}"

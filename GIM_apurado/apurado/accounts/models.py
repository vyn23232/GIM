from django.db import models
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import BaseUserManager





class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    next_page = 'home'
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True, blank=True)
    contact = models.CharField(max_length=12)
    registration_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.username

class Dashboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dashboard')
    membership_status = models.CharField(max_length=50)
    upcoming_bookings = models.IntegerField(default=0)
    payment_history = models.CharField(max_length=50)

class Membership(models.Model):
    membership_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memberships')  # Mandatory one-to-optional many
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=50)
    membership_type = models.CharField(max_length=50)
    renewal_date = models.DateField()

class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')  # Mandatory one-to-optional many
    class_id = models.ForeignKey('Class', on_delete=models.SET_NULL, null=True, related_name='bookings')  # Mandatory one, optional one
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15)

class Class(models.Model):
    class_id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    schedule = models.CharField(max_length=50)
    instructor = models.CharField(max_length=50)
    max_participants = models.IntegerField()

class Attendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendances')  # Mandatory one, optional one
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='attendances')  # Mandatory one, optional one
    date_attended = models.DateField()

class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, related_name='payments')  # Mandatory one, optional one
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=50)

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
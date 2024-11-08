from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    gym_class = models.CharField(max_length=100)
    joined = models.DateField(auto_now_add=True)
    expiration = models.DateField()

    def __str__(self):
        return self.name


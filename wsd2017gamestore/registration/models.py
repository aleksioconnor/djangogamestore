from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(default=datetime.date.today)
    email = models.EmailField(default='')
    user_type = models.CharField(max_length=200)
    is_activated = models.BooleanField(default=False)
    activation_key = models.CharField(max_length=25, default='')


# class Developer(models.Model):
#     user =
#     Games =

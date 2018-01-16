from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField()
    email = models.EmailField()
    user_type = models.CharField(max_length=200)


# class Developer(models.Model):
#     user =
#     Games =

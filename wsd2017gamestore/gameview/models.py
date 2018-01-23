from django.db import models
from django.contrib.auth.models import User
from store.models import Game

# Create your models here.
class HighScore(models.Model):
    player = models.ForeignKey(User)
    score = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    game = models.ForeignKey(Game)

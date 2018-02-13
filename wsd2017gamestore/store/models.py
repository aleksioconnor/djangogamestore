from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
      return self.name

class Game(models.Model):
    name = models.CharField(max_length=200)
    # pub_date = models.DateTimeField('date published')
    price = models.IntegerField(default=0)
    url = models.URLField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    developer_id = models.IntegerField(default=0)

class BoughtGames(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

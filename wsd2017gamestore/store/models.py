from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    name = models.CharField(max_length=200)
    # pub_date = models.DateTimeField('date published')
    price = models.IntegerField(default=0)
    # TODO: Check what really should be the default value
    url = models.URLField(max_length=200)
    # category = models.ForeignKey(Category, on_delete=models.CASCADE)
    developer_id = models.IntegerField(default=0)

	# What is this if you find out please tell me where this is called, apparently right now this is not being used anywhere
    #def add_game(self, name, price, url):
    #    game = self.create(name=name, price=price, url=url)
    #    return game

class Category(models.Model):
    name = models.CharField(max_length=200)

class BoughtGames(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

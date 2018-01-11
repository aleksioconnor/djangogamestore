from django.db import models

class Game(models.Model):
    name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    price = models.IntegerField(default=0)
    # category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Category(models.Model):
    name = models.CharField(max_length=200)

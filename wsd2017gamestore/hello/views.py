from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Game


def index(request):
	most_recent_game = Game.objects.order_by('pub_date')
	games = most_recent_game
	context = {
		'games' : games
	}
	return render(request, 'hello/index.html', context)

# Create your views here.

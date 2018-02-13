from django.shortcuts import render
from django.template import loader
from .models import Game, BoughtGames
from django.contrib.auth.models import User

def index(request):
	most_recent_game = Game.objects.order_by('price')
	games = most_recent_game

	if request.user.is_authenticated():
		owned_games = BoughtGames.objects.filter(user=request.user)
	else:
		owned_games = BoughtGames.objects.none()

	context = {
		'games' : games,
		'id' : id,
		'owned_games' : owned_games,
	}
	return render(request, 'store/index.html', context)

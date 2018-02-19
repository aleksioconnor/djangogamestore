from django.shortcuts import render
from django.template import loader
from .models import Game, BoughtGames, Category
from django.contrib.auth.models import User
from itertools import chain

def index(request):
	most_recent_game = Game.objects.order_by('price')
	games = most_recent_game
	user_id = request.user.id
	# Retrieve all categories
	categories = Category.objects.all()

	if request.user.is_authenticated():
		bought_games = []
		# getting game models from user's bought games
		for i in BoughtGames.objects.all().filter(user=request.user):
			bought_games.append(i.game)

		# games the user has developed
		developed_games = Game.objects.all().filter(developer_id=user_id)
		# combining bought and developed games
		combined_games = list(chain(bought_games, developed_games))
		# removing possible duplicate games from set
		owned_games = list(set(combined_games))
	else:
		owned_games = BoughtGames.objects.none()

	context = {
		'games' : games,
		'id' : id,
		'owned_games' : owned_games,
		'categories' : categories,
	}
	return render(request, 'store/index.html', context)

def error_404(request):
	data = {}
	return render(request, 'store/error404.html', data)

def error_500(request):
	data = {}
	return render(request, 'store/error500.html', data)
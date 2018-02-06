from django.shortcuts import render
from django.template import loader
from .models import Game, BoughtGames
from django.contrib.auth.models import User

from .forms import GameForm

def index(request):
	most_recent_game = Game.objects.order_by('price')
	games = most_recent_game
	owned_games = BoughtGames.objects.filter(user=request.user)
	for i in owned_games:
		print(i.game.name)

	# handling form actions
	if request.method == 'POST':
		form = GameForm(request.POST)
		if form.is_valid():
			#Take form data
			# ***********************************************************************
			# IMPORTANT: IF YOU ADD STUFF TO THE FORM, REMEMBER TO ADD THEM HERE!!!!!
			name = form.cleaned_data['game_name']
			price = form.cleaned_data['game_price']
			url = form.cleaned_data['game_url']
			#*************************************************************************
			#TODO: Sanitize the data
			dev_id = request.user.id #collects id of the current user
			g = Game(name=name, price=price, url=url, developer_id = dev_id) # And also here
			g.save()
			form = GameForm() #empties the form
	else:
		form = GameForm() #Load a empty GameForm when arriving at the site for the first time

	context = {
		'games' : games,
		'form' : form,
		'id' : id,
		'owned_games' : owned_games,
	}
	return render(request, 'store/index.html', context)

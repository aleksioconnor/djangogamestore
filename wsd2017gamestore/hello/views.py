from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Game

from .forms import GameForm

def index(request):
	most_recent_game = Game.objects.order_by('price')
	games = most_recent_game

	# handling form actions
	if request.method == 'POST':
		form = GameForm(request.POST)
		if form.is_valid():
			#Take form data
			name = form.cleaned_data['game_name']
			price = form.cleaned_data['game_price']
			#TODO: Sanitize the data
			g = Game(name=name, price=price)
			g.save()
			form = GameForm() #empties the form
	else:
		form = GameForm() #Load a empty GameForm when arriving at the site for the first time

	context = {
		'games' : games,
		'form' : form
	}
	return render(request, 'hello/index.html', context)

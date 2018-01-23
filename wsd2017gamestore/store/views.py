from django.shortcuts import render
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
			# ***********************************************************************
			# IMPORTANT: IF YOU ADD STUFF TO THE FORM, REMEMBER TO ADD THEM HERE!!!!!
			name = form.cleaned_data['game_name']
			price = form.cleaned_data['game_price']
			url = form.cleaned_data['game_url']
			#*************************************************************************
			#TODO: Sanitize the data
			g = Game(name=name, price=price, url=url) # And also here
			g.save()
			form = GameForm() #empties the form
	else:
		form = GameForm() #Load a empty GameForm when arriving at the site for the first time

	context = {
		'games' : games,
		'form' : form,
		'id' : id
	}
	return render(request, 'store/index.html', context)

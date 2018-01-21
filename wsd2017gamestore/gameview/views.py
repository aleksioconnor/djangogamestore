from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from store.models import Game
# Create your views here.

def index(request, game_id):
	current_game = Game.objects.get(id=game_id)
	context = {'game': current_game}
	return render(request, 'gameview/index.html', context)
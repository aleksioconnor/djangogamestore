from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from store.models import Game
from .models import HighScore

def index(request, game_id):
	current_game = Game.objects.get(id=game_id)
	context = {'game': current_game}
	return render(request, 'gameview/index.html', context)

# Defines an 'endpoint' for our ajax POST function in the gameview template.
# When submitting a score, a function sends the score with an ajax function
# and it gets handled here.
def score(request, game_id):
	# Request contains the crsftoken and the data sent from the template
	# can be accessed via POST
	post = request.POST
	# Accessed via the key value
	score = post['score']
	# gets the correct game being played
	currentGame = Game.objects.get(id=game_id)
	# adds a new high score model/object
	newScore = HighScore(player=request.user, score=score, game=currentGame)
	newScore.save()

	# Retrieves all high score objects, filters out only the ones
	# associated with this game, orders them, and only returns
	# the top 5.
	scores = HighScore.objects.all().filter(game=currentGame).order_by('-score')[:5]
	return HttpResponse(scores)

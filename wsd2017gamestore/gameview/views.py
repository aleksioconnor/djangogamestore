from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from store.models import Game
from .models import HighScore
from .models import GameState

from django.http import JsonResponse
from django.core import serializers

from django.db.utils import OperationalError
from hashlib import md5

import json

def index(request, game_id):
	current_game = Game.objects.get(id=game_id)
	high_score_list = HighScore.objects.all().filter(game=current_game).order_by('-score')[:5]
	context = {'game': current_game, 'high_scores': high_score_list}
	return render(request, 'gameview/index.html', context)

# Defines an 'endpoint' for our ajax POST function in the gameview template.
# When submitting a score, a function sends the score with an ajax function
# and it gets handled here.

#TODO & IMPORTANT: Not sure, but i'm pretty confident that the score input can be manipulated. For example,
# if the score key-value is intercepted a mysql-injection can be performed. This is something that should
# be investigated

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

	# Safe is false to allow non-dict objects to be serialized
	return JsonResponse(serializers.serialize('json', scores), safe=False)

def state(request, game_id):
	post = request.POST
	state = post['state']
	currentGame = Game.objects.get(id=game_id)
	newState = GameState(player=request.user, state=state, game=currentGame)
	newState.save()
	return HttpResponse("game saved")

def load(request, game_id):
	currentGame = Game.objects.get(id=game_id)
	try:
		mostRecentSave = GameState.objects.all().filter(game=currentGame).filter(player=request.user).order_by('-date')[:1]
	# In case of no game saves
	except OperationalError:
		return (HttpResponse("error"))
	return JsonResponse(serializers.serialize('json', mostRecentSave, fields=('state')), safe=False)

def buy(request, game_id):
	game = Game.objects.get(id=game_id)

	pid = "12345" # TODO Change to a unique id (f.ex. gameid + userid)
	sid = "AKAGameStore"
	amount = game.price
	secret_key = "5ba99a03e46a687041b16ec552bcdf9c"
	checksum_str = "pid={}&sid={}&amount={}&token={}".format(pid, sid, amount, secret_key)
	m = md5(checksum_str.encode("ascii")) # encoding the checksum
	checksum = m.hexdigest()

	context = {
		'pid': pid,
		'sid': sid,
		'amount': amount,
		'secret_key': secret_key,
		'checksum': checksum,
		'game_id': game_id
	}

	return render(request, 'gameview/payment.html', context)

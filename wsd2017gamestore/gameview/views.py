from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from store.models import Game
from .models import HighScore

from django.http import JsonResponse
from django.core import serializers

from hashlib import md5

import json

def index(request, game_id):
	current_game = Game.objects.get(id=game_id)
	context = {'game': current_game}
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

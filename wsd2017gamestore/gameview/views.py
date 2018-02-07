from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from store.models import Game, BoughtGames
from django.contrib.auth.models import User
from .models import HighScore
from .models import GameState

from django.http import JsonResponse
from django.core import serializers

from django.db.utils import OperationalError
from hashlib import md5

import json

def index(request, game_id):
	# Checks what game is being currently viewed from the id
	current_game = Game.objects.get(id=game_id)

	# Retrieves global top five scores associated with this game
	high_score_list = HighScore.objects.all().filter(game=current_game).order_by('-score')[:5]

	# Checks if user owns this game, True if does, False if not
	user_owns_game = len(BoughtGames.objects.all().filter(game=current_game).filter(user=request.user)) > 0

	context = {'game': current_game, 'high_scores': high_score_list, 'owned': user_owns_game}
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

def buy_game(request, game_id):
	game = Game.objects.get(id=game_id)
	user_id = request.user.id # TODO case none = nobody logged in
	pid = str(user_id) + "-" + game_id # Can be any random id, just needs to be unique
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
		'game_id': game_id,
		'game': game
	}

	return render(request, 'gameview/payment.html', context)

def successful_payment(request, game_id):
	pid = request.GET['pid'] # payment ID
	ref = request.GET['ref'] # reference to payment
	url_checksum = request.GET['checksum']

	secret_key = "5ba99a03e46a687041b16ec552bcdf9c"
	checksum_str = "pid={}&ref={}&result={}&token={}".format(pid, ref, "success", secret_key)

	m = md5(checksum_str.encode("ascii"))
	checksum = m.hexdigest()

	# user_id, game_id = pid.split('-')
	game = Game.objects.get(id=game_id)
	current_user = request.user

	if current_user:
		if url_checksum == checksum:
			# TODO check from owned games that it is not already purchased
			# TODO add to owned games
			# TODO add to game purchase history

			user = User.objects.get(id=current_user.id) # Is this equal to current_user?
			print(user)

			print(current_user)

			bought_game = BoughtGames(game = game, user = user)
			bought_game.save()

			context = {
				'game': game,
			}

			return render(request, 'gameview/success.html', context)
		else:
			return render(request, 'gameview/success.html', {'error': "error"}) # TODO

def error_payment(request, game_id):
	pid = request.GET['pid'] # payment ID
	ref = request.GET['ref'] # reference to payment
	url_checksum = request.GET['checksum']

	secret_key = "5ba99a03e46a687041b16ec552bcdf9c"
	checksum_str = "pid={}&ref={}&result={}&token={}".format(pid, ref, "error", secret_key)

	m = md5(checksum_str.encode("ascii"))
	checksum = m.hexdigest()

	# user_id, game_id = pid.split('-')
	game = Game.objects.get(id=game_id)
	user = request.user
	if user:
		if url_checksum == checksum:
			# TODO check from owned games that it is not already purchased
			# TODO add to owned games
			# TODO add to game purchase history

			context = {
				'game': game,
			}

			return render(request, 'gameview/error.html', context)
		else: # wrong checksum
			return render(request, 'gameview/success.html', {'error': "error"}) # TODO
	else: # user not logged in
		return render(request, 'gameview/success.html', {'error': "error"}) # TODO

def cancel_payment(request, game_id):
	pid = request.GET['pid'] # payment ID
	ref = request.GET['ref'] # reference to payment
	url_checksum = request.GET['checksum']

	secret_key = "5ba99a03e46a687041b16ec552bcdf9c"
	checksum_str = "pid={}&ref={}&result={}&token={}".format(pid, ref, "cancel", secret_key)

	m = md5(checksum_str.encode("ascii"))
	checksum = m.hexdigest()

	# user_id, game_id = pid.split('-')
	game = Game.objects.get(id=game_id)

	if url_checksum == checksum:
		# TODO check from owned games that it is not already purchased
		# TODO add to owned games
		# TODO add to game purchase history

		context = {
			'game': game,
		}

		return render(request, 'gameview/cancel.html', context)
	else:
		return render(request, 'gameview/success.html', {'error': "error"}) # TODO

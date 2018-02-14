from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.db.utils import OperationalError
from django.utils.datastructures import MultiValueDictKeyError
from hashlib import md5
import json

from store.models import Game, BoughtGames
from django.contrib.auth.models import User
from .models import HighScore
from .models import GameState

# Renders the main view
def index(request, game_id):
	# Checks what game is being currently viewed from the id
	current_game = Game.objects.get(id=game_id)

	# Gets users id
	user_id = request.user.id

	# Retrieves global top five scores associated with this game
	high_score_list = HighScore.objects.all().filter(game=current_game).order_by('-score')[:5]

	# Checks if user owns or has developed this game, True if does, False if not
	if request.user.is_authenticated():
		user_owns_game = len(BoughtGames.objects.all().filter(game=current_game).filter(user=request.user)) > 0
		user_developed_game = len(Game.objects.all().filter(name=current_game.name).filter(developer_id=user_id)) > 0
	else:
		user_owns_game = False

	context = {'game': current_game, 'high_scores': high_score_list, 'owned': user_owns_game, 'developed': user_developed_game, 'logged_in': request.user.is_authenticated()}
	return render(request, 'gameview/index.html', context)

# Defines an 'endpoint' for our ajax POST function in the gameview template.
# When submitting a score, a function sends the score with an ajax function
# and it gets handled here.
def score(request, game_id):
	post = request.POST
	# Accessed via the key value
	try:
		score = post['score']
	# In case of invalid data being sent to the endpoint
	except MultiValueDictKeyError:
		return HttpResponse(status=400)
	# gets the correct game being played
	currentGame = Game.objects.get(id=game_id)
	# adds a new high score model/object
	newScore = HighScore(player=request.user, score=score, game=currentGame)
	newScore.save()

	return HttpResponse(status=201)

# This endpoint retrieves the top 5 high scores for the game
def scores(request, game_id):
	# Gets current game or returns 404 if not found
	currentGame = get_object_or_404(Game, id=game_id)

	# Retrieves all scores, filters out top five associated with the current game
	scores = HighScore.objects.all().filter(game=currentGame).order_by('-score')[:5]

	# Loop through scores, generate data
	data = [{'score': item.score, 'player': item.player.username } for item in scores]

	# Return as json
	return HttpResponse(json.dumps(data), content_type='application/json')

# Endpoint receives game state and saves it to the database
def state(request, game_id):
	# Get post content
	post = request.POST
	print(post)

	# Access state from HTTP post
	try:
		state = post['state']
	except MultiValueDictKeyError:
		return HttpResponse(status=400)

	# Get game or 404
	currentGame = get_object_or_404(Game, id=game_id)

	# Creates new state in the database
	newState = GameState(player=request.user, state=state, game=currentGame)
	newState.save()

	# Returns 'created' response code
	return HttpResponse(status=201)

# Endpoint returns most recently saved game
def load(request, game_id):
	# Gets current game
	currentGame = get_object_or_404(Game, id=game_id)

	try:
		mostRecentSave = GameState.objects.all().filter(game=currentGame).filter(player=request.user).order_by('-date')[:1]
	# If try give operationalError, meaning no saves found
	except OperationalError:
		return (HttpResponse(status=400))
	# Check if most recent save is empty or not
	if not mostRecentSave:
		return (HttpResponse(status=400))

	else:
		data = [{'data': item.state} for item in mostRecentSave]
		return HttpResponse(json.dumps(data), content_type='application/json')

# Handles game purchases
@login_required
def buy_game(request, game_id):
	game = Game.objects.get(id=game_id)
	user_id = request.user.id

	# Check if user owns game.
	user_owns_game = len(BoughtGames.objects.all().filter(game=game).filter(user=request.user)) > 0

	if request.user.is_authenticated() and not user_owns_game:
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
	# If user owns game, redirect to home page.
	else:
		return redirect('/store/')

# Handles what happens after payment is received
@login_required
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
			bought_game = BoughtGames(game = game, user = user)
			bought_game.save()

			context = {
				'game': game,
			}

			return render(request, 'gameview/success.html', context)
		else:
			return render(request, 'gameview/success.html', {'error': "error"}) # TODO

# Handles erros in payment
@login_required
def error_payment(request, game_id):
	pid = request.GET['pid'] # payment ID
	ref = request.GET['ref'] # reference to payment
	url_checksum = request.GET['checksum']

	secret_key = "5ba99a03e46a687041b16ec552bcdf9c"
	checksum_str = "pid={}&ref={}&result={}&token={}".format(pid, ref, "error", secret_key)

	m = md5(checksum_str.encode("ascii"))
	checksum = m.hexdigest()

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

# Handles canceled payments
def cancel_payment(request, game_id):
	pid = request.GET['pid'] # payment ID
	ref = request.GET['ref'] # reference to payment
	url_checksum = request.GET['checksum']

	secret_key = "5ba99a03e46a687041b16ec552bcdf9c"
	checksum_str = "pid={}&ref={}&result={}&token={}".format(pid, ref, "cancel", secret_key)

	m = md5(checksum_str.encode("ascii"))
	checksum = m.hexdigest()

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

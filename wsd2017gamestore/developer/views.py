from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView
from .forms import NewGameForm
from store.models import Game, BoughtGames
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from django import template
from common.util import user_is_developer

# If user is not logged in and tries to access developer page, user is prompted to log in.
@user_passes_test(user_is_developer, login_url='/auth/login/', redirect_field_name=None)
def index(request):
    # handling form actions
    if request.method == 'POST':
        form = NewGameForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['game_name']
            price = form.cleaned_data['game_price']
            url = form.cleaned_data['game_url']
            category = form.cleaned_data['category']
            dev_id = request.user.id
            g = Game(name=name, price=price, url=url, developer_id=dev_id, category=category)
            g.save()
            form = NewGameForm()
    else:
        form = NewGameForm()
        print(request.user.id)

    return render(request, 'developer/index.html', {'form':form})

@login_required
def edit(request):
    games = Game.objects.filter(developer_id = request.user.id)
    # Get stats of sold games
    for game in games:
      single_game_stats = BoughtGames.objects.all().filter(game = game)
      game.sales = len(single_game_stats)
    context = { 'games': games }

    return render(request, 'developer/edit.html', context)

# Takes the template from store/game_form.html TODO: change this
class GameEdit(UpdateView):
        model = Game
        fields = ['name', 'price', 'url']

class GameDelete(DeleteView):
    model = Game
    success_url = reverse_lazy('edit')

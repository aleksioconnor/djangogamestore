from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic.edit import UpdateView
from .forms import NewGameForm
from store.models import Game

# Create your views here.
def index(request):
    print("juu")
    # handling form actions
    if request.method == 'POST':
        form = NewGameForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['game_name']
            price = form.cleaned_data['game_price']
            url = form.cleaned_data['game_url']
            dev_id = request.user.id
            g = Game(name=name, price=price, url=url, developer_id=dev_id)
            g.save()
            form = NewGameForm()
    else:
        form = NewGameForm()
        print(request.user.id)

    return render(request, 'developer/index.html', {'form':form})

def edit(request):
    games = Game.objects.filter(developer_id = request.user.id)
    context = { 'games': games }

    return render(request, 'developer/edit.html', context)

# Takes the template from store/game_form.html TODO: change this
class GameEdit(UpdateView):
        model = Game
        fields = ['name', 'price', 'url']

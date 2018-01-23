from django.shortcuts import render
from .forms import NewGameForm
from store.models import Game

# Create your views here.
def index(request):
    # handling form actions
    if request.method == 'POST':
        form = NewGameForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['game_name']
            price = form.cleaned_data['game_price']
            url = form.cleand_data['game_url']
            g = Game(name=name, price=price, url=url)
            g.save()
            form = NewGameForm()
    else:
        form = NewGameForm()

    return render(request, 'developer/index.html', {'form':form})

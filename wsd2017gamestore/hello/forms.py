from django import forms

class GameForm(forms.Form):
    game_name = forms.CharField(label='Game name', max_length=200)
    game_price = forms.IntegerField(label='Game price')

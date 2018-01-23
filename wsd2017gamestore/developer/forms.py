from django import forms

class NewGameForm(forms.Form):
    game_name = forms.CharField(label='Game name', max_length=200)
    game_price = forms.IntegerField(label='Game price')
    game_url = forms.URLField(label='Game url')

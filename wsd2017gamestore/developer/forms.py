from django import forms
from store.models import Category

class NewGameForm(forms.Form):
    game_name = forms.CharField(label='Game name', max_length=200)
    game_price = forms.IntegerField(label='Game price')
    game_url = forms.URLField(label='Game url')

    # Returns all categories as a queryset
    categories = Category.objects.all()
    category = forms.ModelChoiceField(queryset=categories, to_field_name="name")

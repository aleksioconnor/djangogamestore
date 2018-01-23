from django.conf.urls import url

from . import views
# The url mapping takes a four digit number that should be mapped to an individual game.
urlpatterns = [
	url(r'^(?P<game_id>[0-9]+)/$', views.index, name='index'),
	url(r'^(?P<game_id>[0-9]+)/score/', views.score),
]

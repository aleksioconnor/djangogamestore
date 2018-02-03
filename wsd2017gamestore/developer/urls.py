from django.conf.urls import url

from . import views

urlpatterns = [
	url('index/', views.index, name='index'),
	url(r'edit/$', views.edit, name='edit'),
	url(r'edit/(?P<pk>[0-9]+)/', views.GameEdit.as_view(success_url="/dev/edit"), name='GameEdit')
]

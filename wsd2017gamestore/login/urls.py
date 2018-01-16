from django.conf.urls import url
from django.contrib.auth import views as auth_views

# from . import views

urlpatterns = [
	url('', auth_views.login, {'template_name': 'login/login.html'}, name='login'),
]

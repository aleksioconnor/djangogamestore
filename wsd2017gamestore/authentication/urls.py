from django.conf.urls import url
from django.contrib.auth import views as auth_views

# At the moment no other implementation than url mappings to auth_views.login and auth_views.logout
urlpatterns = [
	url('login/', auth_views.login, {'template_name': 'login/login.html'}, name='login'),
	url('logout/', auth_views.logout, {'next_page': '/'}),
]

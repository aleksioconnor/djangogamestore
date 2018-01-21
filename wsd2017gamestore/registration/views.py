from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from .forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user_type = form.cleaned_data.get('user_type')
            user = authenticate(username=username, password=raw_password, user_type=user_type)
            login(request, user)
            group = Group.objects.get(name=user_type)
            user.groups.add(group)
            return redirect('/store/')
    else:
        form = SignUpForm()

        #TODO: allaoleva form:form contextina eteenpäin
    return render(request, 'registration/index.html', {'form': form})

def logout_view(request):
	logout(request)

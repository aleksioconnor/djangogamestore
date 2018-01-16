from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
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
            return redirect('/hello/')
    else:
        form = SignUpForm()

        #TODO: allaoleva form:form contextina eteenpäin
    return render(request, 'registration/index.html', {'form': form})

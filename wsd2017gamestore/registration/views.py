from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group

from .forms import SignUpForm

def signup(request):
    if request.method == 'POST': #?
        form = SignUpForm(request.POST)

        # Else clause for if form is not valid?
        if form.is_valid():
            # form.save() creates and saves a database object from the data bound to the form
            form.save()

            # Get relevant data from form
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user_type = form.cleaned_data.get('user_type')

            # Authenticate verifies a set of credentials.
            # It takes credentials as keyword arguments, and
            # checks them against the authentication backend.
            # Returns a User object if the credentials are
            # valid. If authentication fails, returns None.
            # Should be clarified why this works in registration - couldn't find why in django docs
            user = authenticate(username=username, password=raw_password, user_type=user_type)

            # Login takes a HttpRequest object and a User object as a parameter
            login(request, user)

            # Returns the desired group object
            group = Group.objects.get(name=user_type)

            # Adds the user to the desired group
            user.groups.add(group)

            # Redirect user to 'front page'
            return redirect('/store/')

    else:
        # Imported from forms.py
        form = SignUpForm()
        #TODO: allaoleva form:form contextina eteenpäin
    return render(request, 'registration/index.html', {'form': form})

def logout_view(request):
    logout(request)

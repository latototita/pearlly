from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .home import store
from django.views import View
from .forms import RegistrationForm



def signup(response):
    if response.method=="POST":
        form=RegistrationForm(response.POST)
        if form.is_valid():
            form.save()
        return redirect('store')
    else:
        form=RegistrationForm()

    return render(response,'signup.html',{"form":form})
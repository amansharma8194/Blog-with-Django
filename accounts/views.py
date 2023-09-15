from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import *
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
# Create your views here.
def register_page(request):
    form = RegisterUser()
    if request.method=='POST':
        form = RegisterUser(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('accounts:login_page'))
        else:
            print("something wrong happened")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    context = {'form': form}
    return render(request, 'accounts/register_page.html', context)

def logout_page(request):
    logout(request)
    return redirect(reverse('home_page'))

def login_page(request):
    form = LoginUserForm()
    if request.method=='POST':
        form = LoginUserForm(request, data = request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username = username, password=password)
            if user is None:
                messages.error(request, 'Incorrect Username or Password')
            else:
                login(request, user)
                return redirect(reverse('home_page'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    context = {'form': form}
    return render(request, 'accounts/login_page.html', context)
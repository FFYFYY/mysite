from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


def register(request):
    if request.method != 'POST':
        form = RegisterForm()
    else:
        form = RegisterForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = User.objects.create_user(username, email, password)
            user.save()
            # del request.session['register_code']
            authenticated_user = authenticate(
                username=username,
                password=password,
            )
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('home'))
    context = {'form': form}
    return render(request, 'users/register.html', context)


def login_view(request):
    if request.method != 'POST':
        form = LoginForm()
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
            # return redirect(request.GET.get('from', reverse('home')))
    context = {'form': form}
    return render(request, 'users/login.html', context)

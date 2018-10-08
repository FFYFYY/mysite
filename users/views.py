import string
import random
from django.core.mail import send_mail
from mysite.settings import DEFAULT_FROM_EMAIL
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User


def logout_view(request):
    logout(request)
    return redirect(request.GET.get('from', reverse('home')))


def register(request):
    # 判断用户是否已经登录
    if request.user.is_authenticated:
        return redirect(request.GET.get('from', reverse('home')))
    if request.method != 'POST':
        form = RegisterForm()
    else:
        form = RegisterForm(data=request.POST, request=request)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = User.objects.create_user(username, email, password)
            user.save()
            del request.session['code']
            del request.session['email']
            authenticated_user = authenticate(
                username=username,
                password=password,
            )
            login(request, authenticated_user)
            return redirect(request.GET.get('from', reverse('home')))
    context = {'form': form}
    return render(request, 'users/register.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect(request.GET.get('from', reverse('home')))
    if request.method != 'POST':
        form = LoginForm()
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    context = {'form': form}
    return render(request, 'users/login.html', context)


def send_code(request):
    email = request.GET.get('email')
    data = {}
    if User.objects.filter(email=email).exists():
        data['status'] = 'ERROR'
        data['message'] = '该邮箱地址已注册'
        return JsonResponse(data)
    code = ''.join(random.sample(string.digits, 6))
    html_msg = """<h3>欢迎注册<光着脚丫子的鱼><h3>
                <p>这是你的验证码<span style="font-weight:bold;color:#da8e8c;font-size:25px;border-bottom: 1px dashed rgb(204, 204, 204);">{0}</span>，
                请收好，记得不要告诉别人哦！</p>""".format(code)
    try:
        send_mail('光着脚丫子的鱼--账号注册', '', DEFAULT_FROM_EMAIL, [email], fail_silently=False, html_message=html_msg)
    except Exception:
        data['status'] = 'ERROR'
        data['message'] = '请输入正确的邮箱地址'
        return JsonResponse(data)
    request.session['code'] = code
    request.session['email'] = email
    request.session.set_expiry(0)
    data['status'] = 'SUCCESS'
    return JsonResponse(data)

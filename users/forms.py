from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        max_length=16,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入4-16位用户名', 'autocomplete': 'off', }),
    )
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入邮箱'})
    )
    password1 = forms.CharField(
        label='密码',
        min_length=6,
        max_length=18,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '6-18位'}),
    )
    password2 = forms.CharField(
        label='确认密码',
        min_length=6,
        max_length=18,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '再次输入密码'}),
    )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(RegisterForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('两次输入的密码不一致')
        return password2


class LoginForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        max_length=16,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '用户名', 'autocomplete': 'off', }),
    )

    password = forms.CharField(
        label='密码',
        min_length=6,
        max_length=18,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '密码'}),
    )

    def clean(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            password = self.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                self.cleaned_data['user'] = user
            else:
                raise forms.ValidationError(u'密码错误')
        else:
            raise forms.ValidationError(u'用户不存在')
        return self.cleaned_data

    # def clean(self):
    #     username = self.cleaned_data['username']
    #     password = self.cleaned_data['password']
    #     user = auth.authenticate(username=username, password=password)
    #     if user:
    #         self.cleaned_data['user'] = user
    #     else:
    #         raise forms.ValidationError('用户名或密码不正确')
    #     return self.cleaned_data

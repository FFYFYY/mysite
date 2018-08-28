from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        max_length=16,
        widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
    )
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'off'})
    )
    verification_code = forms.CharField(
        label='验证码',
        max_length=6,
        widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'none': 'true', })
    )
    password1 = forms.CharField(
        label='密码',
        min_length=6,
        max_length=18,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '6-18位', 'autocomplete': 'off'}),
    )
    password2 = forms.CharField(
        label='确认密码',
        min_length=6,
        max_length=18,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
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

    def clean_verification_code(self):
        code = self.request.session.get('code', '')
        email = self.request.session.get('email', '')
        verification_code = self.cleaned_data['verification_code']
        cd_email = self.cleaned_data['email']
        if not (code != '' and code == verification_code and email == cd_email):
            raise forms.ValidationError('验证码不正确')
        return verification_code

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError('两次输入的密码不一致')
        return password2


class LoginForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', }),
    )

    password = forms.CharField(
        label='密码',
        min_length=6,
        max_length=18,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'off', }),
    )

    def clean(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            password = self.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                self.cleaned_data['user'] = user
                return self.cleaned_data
            else:
                raise forms.ValidationError('密码错误')
        elif User.objects.filter(email=username).exists():
            password = self.cleaned_data['password']
            user_name = User.objects.get(email=username).username
            user = auth.authenticate(username=user_name, password=password)
            if user:
                self.cleaned_data['user'] = user
                return self.cleaned_data
            else:
                raise forms.ValidationError('密码错误')
        else:
            raise forms.ValidationError('用户不存在')



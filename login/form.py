# -*- coding: utf-8 -*-
# @Time    : 2022/4/25 19:55
# @Author  : xiaosong
# @File    : form.py
# @Software: PyCharm
from django import forms
from django.core.validators import EmailValidator

from .myValidators import pdComplexityValidator, judgeRegistered, verifyCode


class createNewUser(forms.Form):
    username = forms.CharField(min_length=5, label="用户名", widget=forms.TextInput(attrs={
        'type': 'text',
        'class': 'form-control rounded mb-1',
        'id': "username",
        'placeholder': "Username",
        'name': "username",
    }), error_messages={"min_length": "你太短了", "required": "该字段不能为空!", "invalid": "输入无效"},
                               validators=[judgeRegistered])

    password = forms.CharField(label="密码", min_length=8, widget=forms.PasswordInput(attrs={
        'type': 'password',
        'class': 'form-control rounded',
        'id': "password",
        'placeholder': "Password",
        'name': "password",
    }), error_messages={"min_length": "你太短了", "required": "该字段不能为空！"},
                               validators=[pdComplexityValidator])

    email = forms.EmailField(label="邮箱", widget=forms.EmailInput(attrs={
        'type': 'email',
        'class': 'form-control rounded',
        'id': "email",
        'placeholder': "Email",
        'name': "email",
    }), validators=[EmailValidator])

    code = forms.CharField(label="验证码", widget=forms.TextInput(attrs={
        'type': 'code',
        'class': 'form-control rounded',
        'id': "code",
        'placeholder': "Code",
        'name': "code",
    }), validators=[verifyCode])


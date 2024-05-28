from . import models
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_recaptcha.fields import ReCaptchaField

from .models import Answer


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = models.Assignment
        fields = ['title', 'description', 'due_date']


class GradeForm(forms.ModelForm):
    class Meta:
        model = models.Grade
        fields = '__all__'


class RegistrationForm(UserCreationForm):
    status_choices = (
        ('user', '-'),
        ('teacher', 'Учитель'),
        ('student', 'Ученик')
    )
    captcha = ReCaptchaField()
    status = forms.ChoiceField(choices=status_choices)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'captcha']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)
    #captcha = ReCaptchaField()


class LectureForm(forms.ModelForm):
    class Meta:
        model = models.Lecture
        fields = '__all__'


class RegisterForm(UserCreationForm):
    captcha = ReCaptchaField()

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2','captcha')


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content', 'file']
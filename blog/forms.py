from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'имя пользователя'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'пароль'}))

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text':forms.Textarea({
                'class':'form-control col-md-12',
                'placeholder':'Текст Коментария'
            })
        }

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text']
        widgets = {
            'title':forms.TextInput({
                'class':'form-control col-md-12',
                'placeholder':'Заголовок'
            }),
            'text':forms.Textarea({
                'class':'form-control col-md-12',
                'placeholder':'Тело поста'
            })
        }

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name','surname','lastname','photo']
        widgets = {
            'name':forms.TextInput({
                'class': 'form-control'
            }),
            'surname':forms.TextInput({
                'class': 'form-control'
            }),
            'lastname':forms.TextInput(attrs={
                'class': 'form-control',
                'label':'Listing Title'

            })
        }
        labels = {
            'name': 'Имя',
            'surname': 'Фамилия',
            'lastname': 'Отчество',
            'photo': 'Ваше Фото'
        }

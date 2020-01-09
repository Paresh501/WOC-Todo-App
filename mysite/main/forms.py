from django import forms
from .models import Task
from tinymce.widgets import TinyMCE
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class PostForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ('task_title', 'task_content')
        widgets = {
            'task_content': TinyMCE(),
        }

class UserCreateForm(UserCreationForm):

    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        
        if commit:
            user.save()
        return user
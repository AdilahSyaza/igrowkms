from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from .models import *


class SharingForm(forms.ModelForm):
    class Meta:
        model = Feed
        fields = '__all__'

class CreateInDiscussion(ModelForm):
    class Meta:
        model= Group
        fields = '__all__'
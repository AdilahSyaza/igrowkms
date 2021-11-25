from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from .models import *


class PersonForm(forms.ModelForm):
    class Meta:  
        model = Person 
        fields = "__all__"  

class UserUpdateForm(forms.ModelForm):
    Username = forms.CharField(required=True)
    Password = forms.CharField(required=True)
    Email = forms.EmailField(required=True)
    Name = forms.CharField(required=False)
    DateOfBirth = forms.CharField(required=False)
    Age = forms.CharField(required=False)
    District = forms.CharField(required=False)
    State = forms.CharField(required=False)
    Occupation = forms.CharField(required=False)
    About = forms.CharField(required=False)
    Gender = forms.CharField(required=False)
    MaritalStatus = forms.CharField(required=False)

    class Meta:
        model = Person
        fields = ['Email', 'Password', 'Username', 'Name', 'DateOfBirth', 'Age', 'District', 'State', 'Occupation', 'About', 'Gender', 'MaritalStatus']



class UserDeleteForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = []
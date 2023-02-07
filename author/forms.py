from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms


class CreationUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email']


class Update(UserChangeForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email']


class ProfileUpdate(forms.ModelForm):
    class Meta:
        model = Profile 
        fields = ['image'] 
    

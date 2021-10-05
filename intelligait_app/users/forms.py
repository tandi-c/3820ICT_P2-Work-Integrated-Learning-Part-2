from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile



# User register form
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User 
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']



# User update form
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User 
        fields = ['first_name', 'last_name', 'username', 'email'] 



# Profile update form
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
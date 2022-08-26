from dataclasses import fields
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from .models import Profile
# from django.forms import extras


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField
    # email = forms.CharField()
    #password1 = forms.CharField
    #password2 = forms.PasswordInput()
    # password2 = forms.PasswordInput
    # password1_address = forms.EmailField( 
    #     label="Please enter your email address",
    #   )
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            #'email': forms.EmailField()
            #'email':forms.EmailInput(attrs={'class': 'form-control','placeholder':'Enter your email'}),
              'email': forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter your email'}),
              'username': forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Unique username'}),
             #'password1': forms.CharField(),
             #'password1': forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Password'}),
            #   'password2':forms.Textarea(attrs={'class': 'form-control','placeholder':'Enter your Password'})
            #   'password2': forms.TextInput(attrs={'class': 'form-control','placeholder':'Confirm Password'}),
            

        }

class UserUpdateForm(forms.ModelForm):
     email = forms.EmailField()
     
     class Meta:
          model = User
          fields = ['username','email'] 
          
          
          
class DateInput(forms.DateInput):
    input_type = 'date'


class ProfileUpdateForm(forms.ModelForm):
     birthday =  forms.DateField(widget=DateInput)

     class Meta:
          model = Profile
          fields = ['first_name','last_name','birthday','bio','phone']
          widgets = {
              'birthday':DateInput(attrs={'class': 'form-control'}),
          }
          
class ProfileImageForm(forms.ModelForm):
     class Meta:
          model = Profile
          fields = ['image']
          
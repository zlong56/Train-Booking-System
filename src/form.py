from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from decimal import Decimal
from .models import *

class AdminRegisterAdmin(UserCreationForm):
    class Meta:
        model = Admin
        fields = ['Name', 'Username', 'password1', 'password2']
        
class ClientRegister(UserCreationForm):
    class Meta:
        model = Client
        fields = ['Name', 'Username', 'password1', 'password2']

class AccountRegistrationForm(UserCreationForm):
    class Meta:
        model = Client
        fields = ['Username', 'Name', 'IC', 'PhoneNumber', 'Email', 'RawPassword']
  
from django import forms
from .models import Signup
from django.contrib.auth.models import User
from betterforms.multiform import MultiForm
from django.contrib.auth.forms import UserCreationForm
from django.forms import DateInput


class DateInput(forms.DateInput):
    input_type='date'

class SignupForm(forms.ModelForm):
    
    class Meta:
        model=Signup
        fields=('name','nickname','birth','gender','phone', 'image','intro')
        widgets={
            'birth': DateInput(),
        }

class UserCreationMultiForm(MultiForm):
    form_classes = {
        'User':UserCreationForm,
        'signup':SignupForm,
        
    }


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')

class UpdateForm(forms.ModelForm):
    class Meta:
        model= Signup
        fields=('nickname', 'image', 'intro')


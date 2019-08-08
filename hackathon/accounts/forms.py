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
        labels = {
            'name': ('사용자이름'),
            'nickname': ('닉네임'),
            'birth':('생년월일'),
            'gender':('성별'),
            'phone': ('핸드폰번호'),
            'image':('프로필 사진'),
            'intro':('자기소개'),    
        }
        widgets={
            'birth': DateInput(),
        }

class UserCreationMultiForm(MultiForm):
    labels={ 'username': ('사용자 아이디')}
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


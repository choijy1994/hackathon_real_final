from django import forms
from .models import Post

class NewPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body',  'yourMaleNumber', 'yourFemaleNumber']
        labels = {
            'title': ('제목'), 'body':('내용'),
            'yourMaleNumber':('희망 동행 남성 인원'), 'yourFemaleNumber':('희망 동행 여성 인원'), 
        }
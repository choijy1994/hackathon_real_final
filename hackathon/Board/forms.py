from django import forms
from .models import Post

class NewPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'ourMaleNumber', 'ourFemaleNumber', 'yourMaleNumber', 'yourFemaleNumber']
        labels = {
            'title': ('제목'), 'body':('내용'),
            'ourMaleNumber':('작성자측 남성 인원'), 'ourFemaleNumber':('작성자측 여성 인원'),
            'yourMaleNumber':('희망 동행 남성 인원'), 'yourFemaleNumber':('희망 동행 여성 인원'), 
        }
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post
from .models import Comment
from taggit.forms import TagWidget

class UserRegisterForm(UserCreationForm):
    email=forms.EmailField(required=True)

    class Meta:
        model=User
        fields=['username','email','password1','password2']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','email']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write a comment...'
            }),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
            'tags': TagWidget(attrs={'class': 'form-control', 'placeholder': 'Add tags separated by commas'}),
        }
 
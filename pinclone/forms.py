from django import forms
from .models import *
from django.contrib.auth.models import User

class BlogForm(forms.ModelForm):
    class Meta:
        model = blog
        fields = ['title','text','image','category']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Blog_comments
        fields = ['blog_comments']

class CommentPinForm(forms.ModelForm):
    class Meta:
        model = pin_comment
        fields = ['pin_comments']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email','first_name','last_name','username']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = profile
        fields = ['pfp','cover','desc']

class UploadForm(forms.ModelForm):
    class Meta:
        model = gallery
        fields = ['caption', 'image']
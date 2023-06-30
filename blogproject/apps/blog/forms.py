from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post
from .models import Comment


class blogForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'header_image', 'body']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author','content','created')


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']

 
class ProfileUpdateForm(forms.ModelForm):
    email =forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class EmailForm(forms.Form):
    recipient = forms.EmailField()

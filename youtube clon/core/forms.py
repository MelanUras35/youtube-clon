from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Video, Comment


class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'video_file', 'thumbnail']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter video title'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'placeholder': 'Enter video description', 'rows': 4}),
            'video_file': forms.FileInput(attrs={'class': 'form-file', 'accept': 'video/*'}),
            'thumbnail': forms.FileInput(attrs={'class': 'form-file', 'accept': 'image/*'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'comment-input', 'placeholder': 'Add a comment...', 'rows': 2}),
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

from django import forms
from .models import *

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['topic', 'title', 'localisation', 'description', 'image']

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'bio', 'avatar']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'custom-file-input'}),
        }

class ChatmessageCreateForm(forms.ModelForm):
    class Meta:
        model = GroupMessage
        fields = ['body']
        widgets = {
            'body': forms.TextInput(attrs={'placeholder': 'Add message...', 'label': ''}),
        }

class PrivateMessageCreateForm(forms.ModelForm):
    class Meta:
        model = PrivateMessage
        fields = ['body']
        widgets = {
            'body': forms.TextInput(attrs={'placeholder': 'Napisz wiadomość...', 'label': ''}),
        }
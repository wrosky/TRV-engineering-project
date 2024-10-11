from django import forms
from .models import Post, User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['host', 'participants', 'rate']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'custom-file-input'}),
        }

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'bio', 'avatar']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'custom-file-input'}),
        }
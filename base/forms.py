from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['host', 'participants', 'rate']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'custom-file-input'}),
        }
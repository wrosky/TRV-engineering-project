from django import forms
from .models import *
from django_select2.forms import Select2Widget
from django_countries.fields import CountryField

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['country', 'city', 'image', 'description', 'note', 'rate']
        widgets = {
            'rate': forms.RadioSelect(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
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

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = [
            'title',
            'country',
            'location',
            'start_date',
            'end_date',
            'flight_from',
            'flight_from_airport',
            'flight_to',
            'flight_to_airport',
            'flight_back_from',
            'flight_back_from_airport',
            'flight_back_to',
            'flight_back_to_airport',
            'flight_price',
            'accommodation_name',
            'accommodation_price',
            'transport_type',
            'transport_price',
            'visa_required',
            'visa_price',
        ]
        widgets = {
            'country': Select2Widget(attrs={'data-placeholder': 'Select a country...'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'flight_from': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'flight_to': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'flight_back_from': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'flight_back_to': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
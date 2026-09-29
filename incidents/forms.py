from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Incident


class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = [
            'title',
            'description',
            'date_time',
            'location',
            'aircraft_type',
            'category',
            'severity',
            'status',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Engine flameout during initial climb',
                'required': True,
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Provide detailed narrative of observations, actions taken, and aftermath...',
                'required': True,
            }),
            'date_time': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'required': True,
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., LAX / Los Angeles International Airport',
                'required': True,
            }),
            'aircraft_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Boeing 777-300ER',
                'required': True,
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
            }),
            'severity': forms.Select(attrs={
                'class': 'form-select',
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
            }),
        }


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Optional email address'})
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

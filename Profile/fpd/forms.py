# forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import re

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = (
            "Your password must contain at least:<br>"
            "- 8 characters<br>"
            "- One uppercase letter<br>"
            "- One lowercase letter<br>"
            "- One number<br>"
            "- One special character"
        )
        self.fields['password2'].help_text = "Enter the same password as before, for verification."

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long.')
        if not re.search(r'[A-Z]', password1):
            raise forms.ValidationError('Password must contain at least one uppercase letter.')
        if not re.search(r'[a-z]', password1):
            raise forms.ValidationError('Password must contain at least one lowercase letter.')
        if not re.search(r'\d', password1):
            raise forms.ValidationError('Password must contain at least one number.')
        if not re.search(r'[@$!%*?&#]', password1):
            raise forms.ValidationError('Password must contain at least one special character.')
        return password1

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
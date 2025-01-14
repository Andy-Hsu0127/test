# quotation_app/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='必填。請提供有效的電子郵件地址。')

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

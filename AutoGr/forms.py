import random
import string

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not email.endswith('@sjsu.edu'):
            raise forms.ValidationError('Only SJSU email addresses are allowed.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        if commit:
            user.save()
        return user

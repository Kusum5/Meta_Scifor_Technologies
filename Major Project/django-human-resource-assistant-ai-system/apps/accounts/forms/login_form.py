from django import forms
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    email = forms.CharField(
        label="E-mail",
        required=True,
        widget=forms.TextInput(attrs={
            "placeholder": "Enter your email",  # Modified placeholder for email
            'class': "form-control form-control-lg fs-6"
        })
    )

    password = forms.CharField(
        label="Palavra-passe",
        required=True,
        widget=forms.PasswordInput(attrs={
            "placeholder": "Enter your password",  # Modified placeholder for password
            'class': "form-control form-control-lg fs-6"
        })
    )


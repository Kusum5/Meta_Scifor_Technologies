from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()


class PasswordResetForm(forms.Form):
    class Meta:
        model = User
        fields = ['email']

    email = forms.CharField(
        label="E-mail",
        required=True,
        widget=forms.TextInput(attrs={
            "placeholder": "Enter your email",  # Placeholder updated to en-IN style
            'class': "form-control form-control-lg fs-6"
        })
    )


class PasswordChangeForm(forms.Form):
    class Meta:
        model = User
        fields = ['new_password', 'confirmation_password']

    new_password = forms.CharField(
        label="New Password",  # Label updated to English
        required=True,
        widget=forms.PasswordInput(attrs={
            "placeholder": "Enter your new password",  # Placeholder updated to en-IN style
            'class': "form-control form-control-lg fs-6"
        })
    )

    confirmation_password = forms.CharField(
        label="Confirm Password",  # Label updated to English
        required=True,
        widget=forms.PasswordInput(attrs={
            "placeholder": "Confirm your new password",  # Placeholder updated to en-IN style
            'class': "form-control form-control-lg fs-6"
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("new_password")
        password2 = cleaned_data.get("confirmation_password")

        if password != password2:
            raise ValidationError({
                'new_password': "Passwords do not match",  # Error message in English
                'confirmation_password': "Passwords do not match"
            })
        elif len(password) < 8:
            raise ValidationError({
                'new_password': "Password must be at least 8 characters long",  # Error message in English
                'confirmation_password': "Password must be at least 8 characters long"
            })

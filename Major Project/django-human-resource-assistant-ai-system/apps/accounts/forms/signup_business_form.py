import re
from .. import utils
from django import forms
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from ..models import Sector

User = get_user_model()

def is_email_valid(email: str) -> bool:
    """Function to validate an email address."""
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,7}$'  # Regular expression for a valid email
    return re.match(regex, email) is not None  # Returns True if the email matches the regex

class SignupBusinessForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'username',
            'email',
            'nif',
            'sector',
            'phone',
            'address',
            'website',
            'password',
            'password2'
        ]

    first_name = forms.CharField(
        label="Company Name",
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder": "Enter the company name",  # Updated placeholder
            "class": "form-control form-control-lg fs-6",
            "iconClass": "person",
        }),
        error_messages={
            "required": "This field cannot be empty!"
        },
    )

    username = forms.CharField(
        label="Username",
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder": "Enter username",  # Updated placeholder
            "class": "form-control form-control-lg fs-6",
            "iconClass": "person",
        }),
    )

    email = forms.EmailField(
        label="Email",
        required=True,
        max_length=100,
        widget=forms.EmailInput(attrs={
            "placeholder": "Enter your email",  # Updated placeholder
            "class": "form-control form-control-lg fs-6",
            "iconClass": "envelope",
        }),
        error_messages={
            'required': 'This field is required'
        }
    )

    nif = forms.CharField(
        label="Tax Identification Number (NIF)",
        required=True,
        max_length=14,
        widget=forms.TextInput(attrs={
            "placeholder": "Enter TAX Identity",  # Updated placeholder
            "class": "form-control form-control-lg fs-6",
            "iconClass": "person",
        }),
    )

    sector = forms.ModelChoiceField(
        label='Sector',
        required=True,
        queryset=Sector.objects.all(),
        widget=forms.Select(attrs={
            "class": "form-select form-control-lg fs-6",
            "iconClass": 'company',
        }),
    )

    phone = forms.CharField(
        label="Phone",
        required=True,
        max_length=13,
        widget=forms.TextInput(attrs={
            'type': 'tel',
            "placeholder": "Enter phone with country code",  # Updated placeholder
            "class": "form-control form-control-lg fs-6",
            "iconClass": "telephone",
        })
    )

    address = forms.CharField(
        label="Address",
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs={
            "placeholder": "Enter your address",  # Updated placeholder
            "class": "form-control form-control-lg fs-6",
            "iconClass": "house",
        }),
    )

    website = forms.URLField(
        label="Website",
        required=True,
        max_length=255,
        widget=forms.URLInput(attrs={
            "placeholder": "e.g., https://company.com",  # Updated placeholder
            "class": "form-control form-control-lg fs-6",
            "iconClass": "globe",
        }),
    )

    password = forms.CharField(
        label='Password',
        required=True,
        max_length=32,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Create a password",  # Updated placeholder
                "class": "form-control form-control-lg fs-6",
                "iconClass": "lock",
            }
        ),
    )

    password2 = forms.CharField(
        label='Confirm Password',
        required=True,
        max_length=32,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Re-enter your password",  # Updated placeholder
                "class": "form-control form-control-lg fs-6",
                "iconClass": "lock",
            }
        ),
    )

    def clean_first_name(self):
        return self.cleaned_data.get('first_name').strip()

    def clean_email(self):
        email = self.cleaned_data.get('email').strip()
        if not is_email_valid(email):
            raise ValidationError("This email is invalid", code='invalid')
        elif User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists", code='invalid')
        return email

    def clean_username(self):
        data = self.cleaned_data.get('username').strip()
        if ' ' in data:
            raise ValidationError("Username cannot contain spaces", code='invalid')
        return data

    def clean_nif(self):
        nif = self.cleaned_data.get('nif').strip()
        if len(nif) != 14:
            raise ValidationError("Tax identification number must be 14 characters long.")
        return nif

    def clean_phone(self):
        phone = self.cleaned_data.get('phone').strip()
        if phone:
            if "+91" not in phone:  # Assuming +91 is the country code for India
                phone = "+91" + phone
            if not re.match(r'^\+91\d{10}$', phone):  # Validating 10 digit number for India
                raise ValidationError("Phone number must contain 10 digits.")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password != password2:
            raise ValidationError({
                'password': "Both password fields must match.",
                'password2': "Both password fields must match."
            })
        elif len(password) < 8:
            raise ValidationError({
                'password': "Passwords must be at least 8 characters long.",
                'password2': "Passwords must be at least 8 characters long."
            })


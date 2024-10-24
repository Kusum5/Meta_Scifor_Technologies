import re
from django import forms
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .. import utils

User = get_user_model()

def is_email_valid(email: str) -> bool:
    """Function to validate an email address."""
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,7}$'  # Regular expression for a valid email
    return re.match(regex, email) is not None  # Returns True if the email matches the regex

class SignupPersonalForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username',
            'email', 'bi', 'phone', 'birthday',
            'gender', 'address', 'password', 'password2'
        ]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    first_name = forms.CharField(
        label="First Name",
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder": "Enter your first name",  # Updated placeholder
            "class": "form-control form-control-lg fs-6",
            "iconClass": "person",
        }),
        error_messages={
            "required": "First name cannot be empty!"
        },
    )

    last_name = forms.CharField(
        label="Last Name",
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder": "Enter your last name",  # Updated placeholder
            "class": "form-control form-control-lg fs-6",
            "iconClass": "person",
        })
    )

    username = forms.CharField(
        label="Username",
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder": "Choose a username",  # Updated placeholder
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

    bi = forms.CharField(
        label="ID Number",
        required=True,
        max_length=14,
        widget=forms.TextInput(attrs={
            "placeholder": "Enter your ID number",  # Updated placeholder
            "class": "form-control form-control-lg fs-6",
            "iconClass": "person",
        }),
    )

    birthday = forms.DateField(
        label='Date of Birth',
        required=True,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control form-control-lg fs-6',
            "iconClass": "calendar2-date",
        }),
        error_messages={
            "required": "Date of birth cannot be empty!"
        },
    )

    phone = forms.CharField(
        label="Phone",
        required=True,
        max_length=13,
        widget=forms.TextInput(attrs={
            'type': 'tel',
            "placeholder": "e.g., 940811141",  # Updated placeholder
            "class": "form-control form-control-lg fs-6",
            "iconClass": "telephone",
        })
    )

    gender = forms.ChoiceField(
        label="Gender",
        required=True,
        choices=utils.GENDER,
        widget=forms.Select(attrs={
            "class": "form-select form-control-lg fs-6",
            "iconClass": "gender-male",
        }),
        error_messages={"required": "Gender cannot be empty!"},
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

    def clean_last_name(self):
        return self.cleaned_data.get('last_name').strip()

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

    def clean_birthday(self):
        birthday = self.cleaned_data.get('birthday')
        if birthday and birthday >= timezone.now().date():
            raise ValidationError("Date of birth must be in the past.", code='invalid')
        return birthday

    def clean_bi(self):
        bi = self.cleaned_data.get('bi').strip()
        if len(bi) != 14:
            raise ValidationError("ID number must be 14 characters long.")
        return bi

    def clean_phone(self):
        phone = self.cleaned_data.get('phone').strip()
        if phone:
            if "+244" not in phone:
                phone = "+244" + phone
            if not re.match(r'^\+244\d{10}$', phone):
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

import re
from django import forms
from apps.accounts import utils
from django.contrib.auth import get_user_model
from apps.accounts.models import PersonalProfile
from django.core.exceptions import ValidationError

User = get_user_model()


class PersonalProfileInformationForm(forms.ModelForm):
    class Meta:
        model = PersonalProfile
        fields = ["bi", "birthday", "gender", "phone", "address", "image"]

    bi = forms.CharField(
        label="ID Number",
        required=True,
        max_length=14,
        widget=forms.TextInput(attrs={
            "placeholder": "ID Number",
            "class": "form-control"
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
            "required": "The Date of Birth field cannot be empty!"
        },
    )

    phone = forms.CharField(
        label="Phone",
        required=True,
        max_length=13,
        widget=forms.TextInput(attrs={
            'type': 'tel',
            "placeholder": "E.g.: 940811141",
            "class": "form-control form-control-lg fs-6",
            "iconClass": "telephone",
        })
    )

    gender = forms.ChoiceField(
        label="Gender",
        required=True,
        choices=utils.GENDER,
        widget=forms.Select(attrs={
            "class": "form-control",
            "iconClass": "gender-male"
        }),
        error_messages={"required": "The Gender field cannot be empty!"}
    )

    address = forms.CharField(
        label="Address",
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs={
            "placeholder": "Address",
            "class": "form-control form-control-lg fs-6",
            "iconClass": "house"
        }),
    )

    image = forms.ImageField(
        label='Profile Image',
        widget=forms.FileInput(attrs={
            "class": "form-control"
        }),
    )

    def clean_bi(self):
        bi = self.cleaned_data.get('bi').strip()
        if len(bi) != 14:
            raise ValidationError("The identification number must be 14 characters long.")
        return bi

    def clean_phone(self):
        phone = self.cleaned_data.get('phone').strip()
        if phone:
            # Check if phone starts with the country code
            if not phone.startswith("+244"):
                phone = "+244" + phone
            if not re.match(r'^\+244\d{9}$', phone):
                raise ValidationError("The phone number must be in the format +244XXXXXXXXX.")
        return phone


class PersonalInformationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    first_name = forms.CharField(
        label="First Name",
        widget=forms.TextInput(attrs={
            "placeholder": "First Name",
            "class": "form-control form-control-lg fs-6",
            "readonly": True
        }),
        error_messages={
            "required": "The first name field cannot be empty!"
        },
    )

    last_name = forms.CharField(
        label="Last Name",
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder": "Last Name",
            "class": "form-control form-control-lg fs-6",
            "readonly": True
        })
    )

    username = forms.CharField(
        label="Username",
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder": "Username",
            "class": "form-control form-control-lg fs-6",
            "readonly": True
        }),
    )

    email = forms.EmailField(
        label="Email",
        required=True,
        max_length=100,
        widget=forms.EmailInput(attrs={
            "placeholder": "E-mail",
            "class": "form-control",
            "readonly": True
        }),
        error_messages={
            'required': 'This field is required'
        }
    )

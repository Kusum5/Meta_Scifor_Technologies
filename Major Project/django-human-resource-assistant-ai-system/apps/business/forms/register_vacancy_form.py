"""register form for vacancy

Raises:
    ValidationError: expiration date can not be in a past date
    ValidationError: The minimum salary cannot be higher than the maximum salary
    ValidationError: The maximum salary cannot be lower than the minimum salary
    ValidationError: _description_
    ValidationError: _description_

Returns:
    _type_: _description_
"""
from django import forms
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from ..models import Vacancy, JobType

User = get_user_model()

class RegisterVacancyForm(forms.ModelForm):
    """register vacancy form model"""
    class Meta:
        model = Vacancy
        fields = [
            'title', 'job_type', 'description', 
            'city', 'expiration_data', 'min_wage', 'max_wage', 
            'entry_time', 'exit_time']

    title = forms.CharField(
        label="Position",
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder": "Position",
            "class": "form-control",
            "tamanho": "col-12 col-sm-6 mt-4",
        }),
        error_messages={
            "required": "The Position field cannot be empty!" 
        },
    )

    job_type = forms.ModelChoiceField(
        label='Job Type',
        required=True,
        queryset=JobType.objects.all(),
        widget=forms.Select(attrs={
            "placeholder": "Job Type", 
            "class": "form-control",
            "tamanho": "col-12 col-sm-6 mt-4", 
        }),
    )

    description = forms.CharField(
        label="Description",
        required=True,
        widget=forms.Textarea(attrs={
            "placeholder": "Description",
            "class": "form-control",
            "tamanho": "col-12 mt-4", 
        })
    )

    city = forms.CharField(
        label="City",
        required=True,
        max_length=150,
        widget=forms.TextInput(attrs={
            "placeholder": "City",
            "class": "form-control form-control-lg fs-6",
            "tamanho": "col-12 col-sm-6 mt-4", 
        }),
    )

    expiration_data = forms.DateField(
        label='Application Deadline',
        required=True,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'format': "%H/%M", 
            'class': 'form-control form-control-lg fs-6',
            "tamanho": "calendar2-date col-12 col-sm-6 mt-4",
        }),
        error_messages={
            "required": "The Application Deadline field cannot be empty!" },
    )

    min_wage = forms.DecimalField(
        label="Minimum Salary (INR)",
        required=True,
        widget=forms.NumberInput(attrs={
            "placeholder": "Minimum Salary",
            "class": "form-control",
            "tamanho": "col-12 col-sm-6 mt-4",
        }),
        error_messages={
            "required": "The Minimum Salary field cannot be empty!" 
        },
    )

    max_wage = forms.DecimalField(
        label="Maximum Salary (INR)",
        required=True,
        widget=forms.NumberInput(attrs={
            "placeholder": "Maximum Salary",
            "class": "form-control",
            "tamanho": "col-12 col-sm-6 mt-4",
        }),
        error_messages={
            "required": "The Maximum Salary field cannot be empty!" 
        },
    )

    entry_time = forms.TimeField(
        label='Start Time',
        required=True,
        widget=forms.TimeInput(attrs={
            'format': "%H/%M",
            'type': 'time',
            'class': 'form-control',
            "tamanho": "col-12 col-sm-6 mt-4",
        })
    )

    exit_time = forms.TimeField(
        label='End Time',
        required=True,
        widget=forms.TimeInput(attrs={
            'format': "%H/%M",
            'type': 'time',
            'class': 'form-control',
            "tamanho": "col-12 col-sm-6 mt-4",
        })
    )

    def clean_title(self):
        """remove the whitespaces at the end of string"""
        return self.cleaned_data.get('title').strip()

    def clean_description(self):
        """remove the whitespaces at the end of string"""
        description = self.cleaned_data.get('description')
        description = description.strip()
        description = description.replace('\n', '<br/>')
        return description

    def clean_address(self):
        """remove the whitespaces at the end of string"""
        return self.cleaned_data.get('address').strip()

    def clean_expiration_data(self):
        """remove the whitespaces at the end of string"""
        expiration_data = self.cleaned_data.get('expiration_data')
        if expiration_data and expiration_data <= timezone.now().date():
            raise ValidationError("The expiration date must be in the future!", "invalid")
        return expiration_data

    def clean_min_wage(self):
        """verify if min_wage is higher than 0"""
        min_wage = self.cleaned_data.get('min_wage')
        if min_wage <= 0:
            raise ValidationError("The minimum salary must be greater than zero!", "invalid")
        return min_wage

    def clean_max_wage(self):
        """verify if max_wage is higher than 0"""
        max_wage = self.cleaned_data.get('max_wage')
        if max_wage <= 0:
            raise ValidationError("The maximum salary must be greater than zero!", "invalid")
        return max_wage

    def clean(self):
        """verify:
        1- if min_wage if lower than max_wage
        2- if entry_time is a before date than exit_time
        """
        cleaned_data = super().clean()
        min_wage = cleaned_data.get("min_wage")
        max_wage = cleaned_data.get("max_wage")

        entry_time = self.cleaned_data.get('entry_time')
        exit_time = self.cleaned_data.get('exit_time')

        if min_wage > max_wage:
            raise ValidationError({
                'min_wage': "The minimum salary cannot be greater than the maximum salary!",
                'max_wage': "The minimum salary cannot be greater than the maximum salary!"})

        if entry_time > exit_time:
            raise ValidationError({
                'entry_time': "The end time is earlier than the start time",
                'exit_time': "The end time is earlier than the start time"})

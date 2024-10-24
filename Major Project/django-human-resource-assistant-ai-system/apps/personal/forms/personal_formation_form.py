import re
from django import forms
from apps.accounts import utils
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from ..models import AcademicInstitution, ProfissionalInstitution, AcademicFormationItem, ProfissionalFormationItem

User = get_user_model()

class ProfissionalFormationForm(forms.ModelForm):
    class Meta:
        model = ProfissionalFormationItem
        fields = ["title", "hours", "institution", "year", ]

    title = forms.CharField(
        label="Title",
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs={
            "placeholder": "Course or Certification Name",
            "class": "form-control",
        }),
    )

    institution = forms.ModelChoiceField(
        label='Institution',
        required=True,
        queryset=ProfissionalInstitution.objects.all(),
        widget=forms.Select(attrs={
            "placeholder": "Institution",
            "class": "form-control form-control-xl fs-6 ",
            "iconClass": "company",
        }),
    )

    hours = forms.IntegerField(
        label="Number of Hours",
        required=True,
        widget=forms.NumberInput(attrs={
            "placeholder": "No. of Hours",
            "class": "form-control",
            "min": 1,
            "max": 1000000,
        }),
    )
    year = forms.IntegerField(
        label="Year",
        required=True,
        widget=forms.NumberInput(attrs={
            "placeholder": "Year",
            "class": "form-control",
            "min": 1970,
            "max": 2070,
        }),
    )

    def clean_title(self):
        title = self.cleaned_data.get('title').strip()
        return title

    def clean_hours(self):
        hours = self.cleaned_data.get('hours')
        if hours < 1:
            raise ValidationError("The course must have at least 1 hour of duration")
        return hours

    def clean_year(self):
        year = self.cleaned_data.get('year')
        if year > timezone.now().date().year:
            raise ValidationError("The year of completion of the course cannot exceed the current year")
        return year


class AcademicFormationForm(forms.ModelForm):
    class Meta:
        model = AcademicFormationItem
        fields = ["course", "institution", "start_year", "end_year", "is_finished", ]

    course = forms.CharField(
        label="Course",
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs={
            "placeholder": "Course",
            "class": "form-control",
        }),
    )

    institution = forms.ModelChoiceField(
        label='Institution',
        required=True,
        queryset=AcademicInstitution.objects.all(),
        widget=forms.Select(attrs={
            "placeholder": "Institution",
            "class": "form-control form-control-lg fs-6",
            "iconClass": "company",
        }),
    )

    start_year = forms.IntegerField(
        label="Start Year",
        required=True,
        widget=forms.NumberInput(attrs={
            "placeholder": "Start Year",
            "class": "form-control",
            "min": 1970,
            "max": 2070,
        }),
    )

    end_year = forms.IntegerField(
        label="End Year",
        required=True,
        widget=forms.NumberInput(attrs={
            "placeholder": "End Year",
            "class": "form-control",
            "min": 1970,
            "max": 2070,
        }),
    )

    is_finished = forms.BooleanField(
        label="Finished?",
        widget=forms.CheckboxInput(attrs={
            "placeholder": "Course",
        }),
    )

    def clean_start_year(self):
        start_year = self.cleaned_data.get('start_year')
        if start_year > timezone.now().date().year:
            raise ValidationError("The start year cannot exceed the current year")
        return start_year

    def clean_end_year(self):
        end_year = self.cleaned_data.get('end_year')
        if end_year < 1970 or end_year > 2050:
            raise ValidationError("Invalid end year")
        return end_year


    # def clean(self):
    #     cleaned_data = super().clean()
    #     start_year =  cleaned_data.get("start_year")
    #     end_year = cleaned_data.get("end_year")

    #     if start_year >= end_year:
    #         raise ValidationError({
    #             'start_year': "O ano de término deve ser maior que o ano de início",
    #             'end_year': "O ano de término deve ser maior que o ano de início",
    #         })


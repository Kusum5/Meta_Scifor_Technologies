from django import forms
from django.contrib.auth import get_user_model
from ..models import ProfissionalExperienceItem

User = get_user_model()


class ProfissionalExperienceForm(forms.ModelForm):
    class Meta:
        model = ProfissionalExperienceItem
        fields = ["institution", "years", "description", ]

    institution = forms.CharField(
        label="Institution",
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs={
            "placeholder": "Institution where you worked",
            "class": "form-control",
        }),
    )

    years = forms.IntegerField(
        label="Years of Experience",
        required=True,
        widget=forms.NumberInput(attrs={
            "placeholder": "How many years did you work at the company?",
            "class": "form-control",
            "min": 0,
            "max": 80,
        }),
    )

    description = forms.CharField(
        label="Description",
        required=True,
        widget=forms.Textarea(attrs={
            "placeholder": "Describe the work you did and the experience you gained",
            "class": "form-control",
        }),
    )

    def clean_institution(self):
        institution = self.cleaned_data.get('institution').strip()
        return institution

    def clean_description(self):
        description = self.cleaned_data.get('description').strip()
        return description

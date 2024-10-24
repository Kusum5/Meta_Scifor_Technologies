"""register form for vacancy skills"""

from django import forms
from ..models import Responsibility


class VacancyResponsibilityForm(forms.ModelForm):
    """register vacancy responsibility form model"""
    class Meta:
        model = Responsibility
        fields = ['title']

    title = forms.CharField(
        label="Short Description",
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs={
            "placeholder": "Description",
            "class": "form-control",
            "tamanho": "col-12 mt-4",
        }),
        error_messages={
            "required": "The Description field cannot be empty!" 
        },
    )

    def clean_title(self):
        """remove the whitespaces at the end of string"""
        return self.cleaned_data.get('title').strip()
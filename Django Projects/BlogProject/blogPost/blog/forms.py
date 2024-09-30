from django import forms
from .models import PostModel

class PostModelForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':2}))
    class Meta:
        model = PostModel
        fields = ('title','content')
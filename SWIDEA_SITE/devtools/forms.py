from django import forms
from .models import Devtool

class DevtoolForm(forms.ModelForm):
    class Meta:
        model = Devtool
        fields = ['name', 'kind', 'content']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'kind': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

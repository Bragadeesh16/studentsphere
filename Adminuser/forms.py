from django import forms
from .models import *

class GroupForm(forms.Form):
    name = forms.CharField(max_length=30)

class uploding_documents(forms.ModelForm):
    class Meta:
        model = file_uplode
        fields = ["notes"]


class uploding_folder(forms.ModelForm):
    class Meta:
        model = folders
        fields = ["name"]

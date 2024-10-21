from django import forms
from .models import *


class uploding_documents(forms.ModelForm):
    class Meta:
        model = file_uplode
        fields = ["notes"]


class uploding_folder(forms.ModelForm):
    class Meta:
        model = folders
        fields = ["name"]

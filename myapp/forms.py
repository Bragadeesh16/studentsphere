from django import forms

class GroupForm(forms.Form):
    name = forms.CharField(max_length=30)
from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.admin.widgets import AdminDateWidget


class signup_from(UserCreationForm):
    email = forms.EmailField(max_length=100, label="email")

    class Meta:
        model = CustomUser
        fields = ["email", "username", "password1", "password2"]


class uploding_documents(forms.ModelForm):
    class Meta:
        model = file_uplode
        fields = ["notes"]


class uploding_folder(forms.ModelForm):
    class Meta:
        model = folders
        fields = ["name"]


class profile_form(forms.ModelForm):
    # date_of_birth = forms.DateField(widget= AdminDateWidget)
    class Meta:
        model = profiles
        exclude = ["profile_user"]

    def __init__(self, *args, **kwargs):
        super(profile_form, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "input-form"
            field.label = profiles._meta.get_field(field_name).verbose_name
            field.widget.attrs["placeholder"] = f"Enter your {field.label}"


class message_form(forms.ModelForm):
    class Meta:
        model = messages
        fields = "__all__"


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

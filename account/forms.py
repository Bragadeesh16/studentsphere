from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser,UserProfile

class signup_from(UserCreationForm):
    email = forms.EmailField(max_length=100, label="email")

    class Meta:
        model = CustomUser
        fields = ["email", "password1", "password2"]

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

class profile_form(forms.ModelForm):
    # date_of_birth = forms.DateField(widget= AdminDateWidget)
    class Meta:
        model = UserProfile
        exclude = ["profile_user"]

    def __init__(self, *args, **kwargs):
        super(profile_form, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "input-form"
            field.label = UserProfile._meta.get_field(field_name).verbose_name
            field.widget.attrs["placeholder"] = f"Enter your {field.label}"
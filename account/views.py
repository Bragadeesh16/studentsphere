from django.shortcuts import render
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from myapp.decorators import authenticate_users
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView

def signup(request):
    form = signup_from()
    if request.method == "POST":
        form = signup_from(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            user = authenticate(email=email, password=password)
            login(request, user)
            messages.success(request, "your are signed in successfully")
            return redirect("home")
    else:
        form = signup_from()

    return render(
        request,
        "register.html",
        {"form": form},
    )


def signin(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        email = form.data["email"]
        password = form.data["password"]
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "your are logged in successfully")
            return redirect("home")
        else:
            form.add_error(None, _("invalid credentials"))
            # return redirect('signin')
    print(form.non_field_errors())
    return render(request, "login.html", {"form": form})


def signout(request):
    logout(request)
    messages.success(request, "you have been logged out")
    return redirect("home")

@authenticate_users
def profile(request):
    try:
        user_profile = profiles.objects.get(profile_user=request.user)
    except profiles.DoesNotExist:
        user_profile = None

    if request.method == "POST":
        form = profile_form(request.POST, instance=user_profile)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return redirect("profile")
    else:
        form = profile_form(instance=user_profile)

        return render(
            request,
            "profile.html",
            {
                "form": form,
            },
        )
    
class CustomPasswordResetView(PasswordResetView):
    template_name = "password_reset.html"
    success_url = reverse_lazy("resetPasswordDone")
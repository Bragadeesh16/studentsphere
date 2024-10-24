from django.urls import path
from django.contrib.auth.views import (
    LogoutView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from . import views
from django.urls import reverse_lazy

urlpatterns = [
    path("signup", views.signup, name="signup"),
    path("signin", views.signin, name="signin"),
    path("signout", views.signout, name="signout"),
    path("profile", views.profile, name="profile"),
    path(
        "resetpassword/",
        views.CustomPasswordResetView.as_view(),
        name="resetPassword",
    ),
    path(
        "resetpassworddone/",
        PasswordResetDoneView.as_view(template_name="password_reset_done.html"),
        name="resetPasswordDone",
    ),
    path(
        "resetpasswordconfirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="password_reset_confirm.html",
            success_url=reverse_lazy("password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "resetpasswordcomplete/",
        PasswordResetCompleteView.as_view(
            template_name="password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]

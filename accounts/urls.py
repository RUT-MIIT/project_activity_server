from django.urls import path
from .views import LoginView, UserMeView, PasswordResetView, PasswordResetConfirmView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("user/", UserMeView.as_view(), name="user-me"),
    path(
        "password/reset/",
        PasswordResetView.as_view(),
        name="password-reset",
    ),
    path(
        "password/reset/confirm/",
        PasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
]

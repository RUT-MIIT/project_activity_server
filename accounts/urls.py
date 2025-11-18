from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    DepartmentViewSet,
    LoginView,
    PasswordResetConfirmView,
    PasswordResetView,
    RegistrationRequestViewSet,
    RoleViewSet,
    UserMeView,
)

router = DefaultRouter()
router.register(r"departments", DepartmentViewSet, basename="department")
router.register(
    r"registration-requests",
    RegistrationRequestViewSet,
    basename="registration-request",
)
router.register(r"roles", RoleViewSet, basename="role")

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
    path("", include(router.urls)),
]

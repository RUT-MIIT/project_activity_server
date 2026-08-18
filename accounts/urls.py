from django.urls import include, path
from rest_framework.routers import DefaultRouter

from accounts.entities.PreRegisteredStudent import PreRegisteredStudentViewSet
from accounts.entities.UserManagement import UserManagementViewSet

from .views import (
    DepartmentViewSet,
    LoginView,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView,
    RegistrationRequestViewSet,
    RoleViewSet,
    SemesterViewSet,
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
router.register(r"semesters", SemesterViewSet, basename="semester")
router.register(r"users", UserManagementViewSet, basename="user-management")
router.register(
    r"pre-registered-students",
    PreRegisteredStudentViewSet,
    basename="pre-registered-student",
)

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
    path(
        "password/change/",
        PasswordChangeView.as_view(),
        name="password-change",
    ),
    path("", include(router.urls)),
]

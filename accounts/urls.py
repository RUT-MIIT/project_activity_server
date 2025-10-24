from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LoginView, UserMeView, PasswordResetView, PasswordResetConfirmView,
    DepartmentViewSet, RegistrationRequestViewSet, RoleViewSet
)

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'registration-requests', RegistrationRequestViewSet, basename='registration-request')
router.register(r'user-roles', RoleViewSet, basename='user-role')

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
    path('', include(router.urls)),
]

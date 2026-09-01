"""Форма создания пользователя в admin без ручного ввода пароля."""

from django import forms
from django.contrib.auth import get_user_model

from accounts.models import UserWithEmailProvision

User = get_user_model()


class AdminUserProvisionForm(forms.ModelForm):
    """Форма для создания пользователя с автогенерацией пароля и отправкой письма."""

    class Meta:
        model = UserWithEmailProvision
        fields = (
            "email",
            "first_name",
            "last_name",
            "middle_name",
            "role",
            "department",
            "study_group",
            "phone",
            "is_staff",
            "is_active",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["role"].required = True
        self.fields["is_active"].initial = True

    def clean_email(self):
        email = self.cleaned_data["email"]
        normalized_email = User.objects.normalize_email(email)
        if User.objects.filter(email=normalized_email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email

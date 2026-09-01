from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.http import HttpResponseRedirect
from django.urls import reverse

from accounts.forms.admin_user_provision_form import AdminUserProvisionForm
from accounts.services.admin_user_provision_service import (
    AdminUserProvisionResult,
    AdminUserProvisionService,
)

from .models import (
    AcademicYear,
    Department,
    PreRegisteredStudent,
    RegistrationRequest,
    Role,
    Semester,
    Settings,
    User,
    UserWithEmailProvision,
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "middle_name",
        "role",
        "department",
        "phone",
        "is_staff",
    )
    list_filter = ("role", "is_staff", "is_active", "department")
    search_fields = ("email", "first_name", "last_name", "middle_name", "phone")
    ordering = ("id",)
    readonly_fields = ("date_joined",)
    fieldsets = (
        (None, {"fields": ("email", "phone", "password")}),
        (
            "Персональная информация",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "middle_name",
                    "role",
                    "department",
                    "study_group",
                    "position",
                    "academic_degree",
                    "academic_title",
                )
            },
        ),
        (
            "Права доступа",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Даты", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "middle_name",
                    "role",
                    "department",
                    "study_group",
                    "phone",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


@admin.register(UserWithEmailProvision)
class UserWithEmailProvisionAdmin(admin.ModelAdmin):
    """Отдельный admin-интерфейс: создание пользователя с письмом на email."""

    form = AdminUserProvisionForm
    _provision_result: AdminUserProvisionResult | None = None

    def get_queryset(self, request):
        return User.objects.none()

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        return HttpResponseRedirect(
            reverse("admin:accounts_userwithemailprovision_add")
        )

    def save_model(self, request, obj, form, change):
        if change:
            return
        self._provision_result = (
            AdminUserProvisionService().create_user_with_credentials_email(
                email=form.cleaned_data["email"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                middle_name=form.cleaned_data.get("middle_name", ""),
                role=form.cleaned_data["role"],
                department=form.cleaned_data.get("department"),
                study_group=form.cleaned_data.get("study_group"),
                phone=form.cleaned_data.get("phone"),
                is_staff=form.cleaned_data.get("is_staff", False),
                is_active=form.cleaned_data.get("is_active", True),
            )
        )

    def response_add(self, request, obj, post_url_continue=None):
        result = self._provision_result
        self._provision_result = None
        if result is None:
            return super().response_add(request, obj, post_url_continue)

        if result.email_sent:
            self.message_user(
                request,
                f"Пользователь создан. Письмо с учётными данными отправлено на {result.user.email}.",
                level=messages.SUCCESS,
            )
        else:
            self.message_user(
                request,
                (
                    "Пользователь создан, но не удалось отправить письмо: "
                    f"{result.email_error}"
                ),
                level=messages.WARNING,
            )
        return HttpResponseRedirect(
            reverse("admin:accounts_userwithemailprovision_add")
        )


@admin.register(PreRegisteredStudent)
class PreRegisteredStudentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "last_name",
        "first_name",
        "middle_name",
        "student_card",
        "personnel_number",
        "snils",
        "role",
        "department",
        "group",
        "user",
    )
    list_filter = ("role", "group__institute", "group", "department")
    search_fields = (
        "last_name",
        "first_name",
        "middle_name",
        "student_card",
        "personnel_number",
        "snils",
    )
    autocomplete_fields = ("group", "user", "department", "role")
    readonly_fields = ("user",)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "short_name",
        "parent",
        "can_save_project_applications",
    )
    search_fields = ("name", "short_name")
    list_filter = ("parent", "can_save_project_applications")


@admin.register(RegistrationRequest)
class RegistrationRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "last_name",
        "first_name",
        "middle_name",
        "email",
        "department",
        "reason",
        "status",
        "actor",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "department", "created_at")
    search_fields = (
        "email",
        "last_name",
        "first_name",
        "middle_name",
        "phone",
        "reason",
    )


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "requires_department", "is_active")
    search_fields = ("code", "name")
    list_filter = ("is_active", "requires_department")
    ordering = ("code",)


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "name")
    search_fields = ("code", "name")
    ordering = ("code",)


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "description", "value_preview")
    search_fields = ("code", "description", "value")

    @admin.display(description="Значение")
    def value_preview(self, obj: Settings) -> str:
        text = obj.value or ""
        return text if len(text) <= 80 else text[:77] + "..."


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "name", "position", "academic_year")
    search_fields = ("code", "name")
    list_filter = ("academic_year",)
    ordering = ("position",)

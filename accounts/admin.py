from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Department, RegistrationRequest, Role, User


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
                    "phone",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


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

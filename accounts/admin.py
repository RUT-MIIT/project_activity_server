from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Department


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
        "is_staff",
    )
    list_filter = ("role", "is_staff", "is_active", "department")
    search_fields = ("email", "first_name", "last_name", "middle_name")
    ordering = ("id",)
    readonly_fields = ("date_joined",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
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
                    "password1",
                    "password2",
                ),
            },
        ),
    )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "short_name", "parent")
    search_fields = ("name", "short_name")
    list_filter = ("parent",)

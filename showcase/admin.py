from django.contrib import admin

from .models import (
    ApplicationInvolvedDepartment,
    ApplicationInvolvedUser,
    ApplicationStatus,
    Institute,
    ProjectApplication,
    ProjectApplicationComment,
    ProjectApplicationStatusLog,
)


@admin.register(ApplicationStatus)
class ApplicationStatusAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "position", "is_active")
    search_fields = ("code", "name")
    list_filter = ("is_active",)
    ordering = ("position",)
    verbose_name = "Статус заявки"
    verbose_name_plural = "Статусы заявок"


@admin.register(ProjectApplicationStatusLog)
class ProjectApplicationStatusLogAdmin(admin.ModelAdmin):
    list_display = (
        "application",
        "changed_at",
        "actor",
        "from_status",
        "to_status",
        "action_type",
    )
    search_fields = ("application__title", "actor__username")
    list_filter = ("to_status", "from_status", "action_type")
    verbose_name = "Лог изменения статуса заявки"
    verbose_name_plural = "Логи изменения статусов заявок"


@admin.register(ProjectApplicationComment)
class ProjectApplicationCommentAdmin(admin.ModelAdmin):
    list_display = ("application", "author", "created_at", "field", "text")
    search_fields = ("text", "author__username", "field")
    list_filter = ("created_at",)
    verbose_name = "Комментарий к заявке"
    verbose_name_plural = "Комментарии к заявкам"


@admin.register(Institute)
class InstituteAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "position", "is_active")
    list_filter = ("is_active",)
    search_fields = ("code", "name")
    ordering = ("position",)


@admin.register(ProjectApplication)
class ProjectApplicationAdmin(admin.ModelAdmin):
    class ApplicationInvolvedUserInline(admin.TabularInline):
        model = ApplicationInvolvedUser
        extra = 0
        raw_id_fields = ("user", "added_by")
        readonly_fields = ("added_at",)
        verbose_name = "Причастный пользователь"
        verbose_name_plural = "Причастные пользователи"

    class ApplicationInvolvedDepartmentInline(admin.TabularInline):
        model = ApplicationInvolvedDepartment
        extra = 0
        raw_id_fields = ("department", "added_by")
        readonly_fields = ("added_at",)
        verbose_name = "Причастное подразделение"
        verbose_name_plural = "Причастные подразделения"

    list_display = (
        "title",
        "print_number",
        "author_lastname",
        "author_firstname",
        "company",
        "status",
        "creation_date",
    )
    list_filter = (
        "status",
        "creation_date",
        "project_level",
        "needs_consultation",
        "application_year",
    )
    search_fields = (
        "title",
        "print_number",
        "author_lastname",
        "author_firstname",
        "author_email",
        "company",
        "problem_holder",
    )
    readonly_fields = ("creation_date",)
    filter_horizontal = ("target_institutes",)
    inlines = [ApplicationInvolvedUserInline, ApplicationInvolvedDepartmentInline]

    fieldsets = (
        (
            "Основная информация",
            {
                "fields": (
                    "title",
                    "author",
                    "status",
                    "creation_date",
                    "needs_consultation",
                    "application_year",
                    "year_sequence_number",
                    "print_number",
                )
            },
        ),
        (
            "Контактные данные",
            {
                "fields": (
                    "author_lastname",
                    "author_firstname",
                    "author_middlename",
                    "author_email",
                    "author_phone",
                    "author_role",
                    "author_division",
                )
            },
        ),
        (
            "О проекте",
            {
                "fields": (
                    "company",
                    "company_contacts",
                    "target_institutes",
                    "project_level",
                )
            },
        ),
        (
            "Проблема",
            {"fields": ("problem_holder", "goal", "barrier", "existing_solutions")},
        ),
        (
            "Контекст",
            {
                "fields": (
                    "context",
                    "stakeholders",
                    "recommended_tools",
                    "experts",
                    "additional_materials",
                )
            },
        ),
    )

from django.contrib import admin
from .models import (
    ApplicationStatus,
    ProjectApplicationStatusLog,
    ProjectApplicationComment,
    ProjectApplication,
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
        "previous_status_log",
    )
    search_fields = ("application__title", "actor__username")
    list_filter = ("to_status", "from_status")
    verbose_name = "Лог изменения статуса заявки"
    verbose_name_plural = "Логи изменения статусов заявок"


@admin.register(ProjectApplicationComment)
class ProjectApplicationCommentAdmin(admin.ModelAdmin):
    list_display = ("status_log", "author", "created_at", "field", "text")
    search_fields = ("text", "author__username", "field")
    list_filter = ("created_at",)
    verbose_name = "Комментарий к изменению статуса заявки"
    verbose_name_plural = "Комментарии к изменениям статусов заявок"


@admin.register(ProjectApplication)
class ProjectApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "company", "status", "author", "creation_date")
    search_fields = ("title", "company", "author__username")
    list_filter = ("status", "company")
    ordering = ("-creation_date",)

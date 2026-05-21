from django.contrib import admin

from teams.models import Direction, StudyGroup, Team, TeamMember


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ("code", "level", "name")
    list_filter = ("level",)
    search_fields = ("code", "name")


@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "code",
        "course_number",
        "is_end",
        "direction",
        "institute",
    )
    list_filter = ("institute", "direction__level", "is_end", "course_number")
    search_fields = (
        "name",
        "code",
        "direction__code",
        "direction__name",
        "institute__code",
        "institute__name",
    )
    autocomplete_fields = ("direction", "institute")


class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 0


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "leader", "project_application", "created_at")
    search_fields = ("name", "leader__email", "leader__last_name")
    list_filter = ("created_at",)
    inlines = [TeamMemberInline]


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("id", "team", "user", "role", "joined_at")
    list_filter = ("role",)
    search_fields = ("team__name", "user__email", "user__last_name")

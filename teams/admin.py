from django.contrib import admin

from teams.models import (
    Direction,
    StudyGroup,
    Team,
    TeamEventLog,
    TeamInvitation,
    TeamJoinRequest,
    TeamSemester,
    TeamSemesterMember,
)


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
        "enrollment_year",
        "profile",
        "form",
        "is_end",
        "direction",
        "institute",
        "mentor",
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
    autocomplete_fields = ("direction", "institute", "mentor")


class TeamSemesterInline(admin.TabularInline):
    model = TeamSemester
    extra = 0
    autocomplete_fields = (
        "semester",
        "captain",
        "mentor",
        "project_application",
        "project_track",
    )


class TeamSemesterMemberInline(admin.TabularInline):
    model = TeamSemesterMember
    extra = 0
    autocomplete_fields = ("user",)
    exclude = ("semester",)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "home_study_group", "created_at")
    search_fields = ("name",)
    list_filter = ("created_at",)
    autocomplete_fields = ("home_study_group",)
    inlines = [TeamSemesterInline]


@admin.register(TeamSemester)
class TeamSemesterAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "team",
        "semester",
        "project_track",
        "status",
        "captain",
        "mentor",
        "project_application",
    )
    list_filter = ("semester", "status", "project_track")
    search_fields = (
        "team__name",
        "captain__email",
        "captain__last_name",
        "mentor__email",
    )
    autocomplete_fields = (
        "team",
        "semester",
        "captain",
        "mentor",
        "project_application",
        "project_track",
    )
    inlines = [TeamSemesterMemberInline]


@admin.register(TeamSemesterMember)
class TeamSemesterMemberAdmin(admin.ModelAdmin):
    list_display = ("id", "team_semester", "user", "role", "semester", "joined_at")
    list_filter = ("role", "semester")
    search_fields = (
        "team_semester__team__name",
        "user__email",
        "user__last_name",
    )
    autocomplete_fields = ("team_semester", "user", "semester")


@admin.register(TeamJoinRequest)
class TeamJoinRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "team_semester",
        "user",
        "status",
        "reviewed_by",
        "created_at",
    )
    list_filter = ("status",)
    search_fields = (
        "team_semester__team__name",
        "user__email",
        "user__last_name",
    )
    autocomplete_fields = ("team_semester", "user", "reviewed_by")


@admin.register(TeamInvitation)
class TeamInvitationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "team_semester",
        "user",
        "invited_by",
        "role",
        "status",
        "created_at",
    )
    list_filter = ("status", "role")
    search_fields = (
        "team_semester__team__name",
        "user__email",
        "invited_by__email",
    )
    autocomplete_fields = ("team_semester", "user", "invited_by")


@admin.register(TeamEventLog)
class TeamEventLogAdmin(admin.ModelAdmin):
    list_display = ("id", "team", "team_semester", "user", "text", "created_at")
    list_filter = ("created_at",)
    search_fields = ("team__name", "text", "user__email")
    autocomplete_fields = ("team", "team_semester", "user")
    readonly_fields = ("created_at",)

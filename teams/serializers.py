from django.contrib.auth import get_user_model
from rest_framework import serializers

from accounts.models import Semester
from showcase.models import ProjectApplication
from teams.models import StudyGroup, Team, TeamSemester, TeamSemesterMember

User = get_user_model()


class TeamMemberUserSerializer(serializers.ModelSerializer):
    """Краткое представление пользователя в составе команды."""

    full_name = serializers.CharField(source="get_full_name", read_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "full_name")


class TeamSerializer(serializers.ModelSerializer):
    """Сериализатор постоянной команды."""

    home_study_group_id = serializers.PrimaryKeyRelatedField(
        queryset=StudyGroup.objects.all(),
        source="home_study_group",
        allow_null=True,
        required=False,
    )

    class Meta:
        model = Team
        fields = (
            "id",
            "name",
            "description",
            "home_study_group_id",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class TeamSemesterMemberSerializer(serializers.ModelSerializer):
    """Сериализатор участника команды в семестре."""

    user = TeamMemberUserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="user",
        write_only=True,
    )

    class Meta:
        model = TeamSemesterMember
        fields = ("id", "user", "user_id", "role", "joined_at")
        read_only_fields = ("id", "joined_at")


class TeamSemesterSerializer(serializers.ModelSerializer):
    """Сериализатор участия команды в семестре."""

    team = TeamSerializer(read_only=True)
    team_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(),
        source="team",
        write_only=True,
    )
    semester_id = serializers.PrimaryKeyRelatedField(
        queryset=Semester.objects.all(),
        source="semester",
    )
    captain = TeamMemberUserSerializer(read_only=True)
    captain_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="captain",
        write_only=True,
        required=False,
    )
    mentor = TeamMemberUserSerializer(read_only=True)
    mentor_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="mentor",
        write_only=True,
        allow_null=True,
        required=False,
    )
    project_application_id = serializers.PrimaryKeyRelatedField(
        queryset=ProjectApplication.objects.all(),
        source="project_application",
        allow_null=True,
        required=False,
    )
    project_track_id = serializers.IntegerField(read_only=True, allow_null=True)
    status = serializers.CharField(read_only=True)
    members = TeamSemesterMemberSerializer(many=True, read_only=True)

    class Meta:
        model = TeamSemester
        fields = (
            "id",
            "team",
            "team_id",
            "semester_id",
            "project_track_id",
            "status",
            "captain",
            "captain_id",
            "mentor",
            "mentor_id",
            "project_application_id",
            "members",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
            "status",
            "project_track_id",
        )

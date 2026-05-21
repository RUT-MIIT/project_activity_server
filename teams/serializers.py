from django.contrib.auth import get_user_model
from rest_framework import serializers

from showcase.models import ProjectApplication
from teams.models import Team, TeamMember

User = get_user_model()


class TeamMemberUserSerializer(serializers.ModelSerializer):
    """Краткое представление пользователя в составе команды."""

    full_name = serializers.CharField(source="get_full_name", read_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "full_name")


class TeamMemberSerializer(serializers.ModelSerializer):
    """Сериализатор участника команды."""

    user = TeamMemberUserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="user",
        write_only=True,
    )

    class Meta:
        model = TeamMember
        fields = ("id", "user", "user_id", "role", "joined_at")
        read_only_fields = ("id", "joined_at")


class TeamSerializer(serializers.ModelSerializer):
    """Сериализатор команды."""

    leader = TeamMemberUserSerializer(read_only=True)
    leader_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="leader",
        write_only=True,
        required=False,
    )
    members = TeamMemberSerializer(many=True, read_only=True)
    project_application_id = serializers.PrimaryKeyRelatedField(
        queryset=ProjectApplication.objects.all(),
        source="project_application",
        allow_null=True,
        required=False,
    )

    class Meta:
        model = Team
        fields = (
            "id",
            "name",
            "description",
            "leader",
            "leader_id",
            "project_application_id",
            "members",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")

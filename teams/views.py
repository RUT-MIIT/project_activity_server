from rest_framework import decorators, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from teams.models import Team, TeamMember
from teams.permissions import TeamPermission
from teams.serializers import TeamMemberSerializer, TeamSerializer


class TeamViewSet(viewsets.ModelViewSet):
    """CRUD для команд и управления участниками."""

    queryset = Team.objects.select_related("leader").prefetch_related("members__user")
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated, TeamPermission]

    def perform_create(self, serializer):
        leader = serializer.validated_data.get("leader") or self.request.user
        team = serializer.save(leader=leader)
        TeamMember.objects.get_or_create(
            team=team,
            user=leader,
            defaults={"role": TeamMember.Role.LEADER},
        )

    @decorators.action(detail=True, methods=["post"], url_path="members")
    def add_member(self, request: Request, pk: int = None) -> Response:
        """POST /api/teams/teams/{id}/members/ — добавить участника."""
        team = self.get_object()
        serializer = TeamMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        role = serializer.validated_data.get("role", TeamMember.Role.MEMBER)

        if TeamMember.objects.filter(team=team, user=user).exists():
            return Response(
                {"error": "Пользователь уже состоит в команде"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        member = TeamMember.objects.create(team=team, user=user, role=role)
        return Response(
            TeamMemberSerializer(member).data,
            status=status.HTTP_201_CREATED,
        )

    @decorators.action(
        detail=True,
        methods=["delete"],
        url_path=r"members/(?P<member_id>\d+)",
    )
    def remove_member(
        self, request: Request, pk: int = None, member_id: int = None
    ) -> Response:
        """DELETE /api/teams/teams/{id}/members/{member_id}/ — удалить участника."""
        team = self.get_object()
        member = team.members.filter(pk=member_id).first()
        if not member:
            return Response(
                {"error": "Участник не найден"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if member.role == TeamMember.Role.LEADER:
            return Response(
                {"error": "Нельзя удалить руководителя команды"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @decorators.action(detail=False, methods=["get"], url_path="my")
    def my_teams(self, request: Request) -> Response:
        """GET /api/teams/teams/my/ — команды текущего пользователя."""
        queryset = self.get_queryset().filter(members__user=request.user).distinct()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

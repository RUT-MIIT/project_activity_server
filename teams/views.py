from rest_framework import decorators, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from accounts.models import Semester
from teams.models import Team, TeamSemester, TeamSemesterMember
from teams.permissions import TeamPermission, TeamSemesterPermission
from teams.serializers import (
    TeamSemesterMemberSerializer,
    TeamSemesterSerializer,
    TeamSerializer,
)


class TeamViewSet(viewsets.ModelViewSet):
    """CRUD для постоянных команд."""

    queryset = Team.objects.select_related("home_study_group")
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated, TeamPermission]

    @decorators.action(detail=False, methods=["get"], url_path="my")
    def my_teams(self, request: Request) -> Response:
        """GET /api/teams/teams/my/?semester_id= — команды пользователя в семестре."""
        try:
            semester_id = Semester.resolve_list_semester_id(
                request.query_params.get("semester_id")
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        queryset = (
            TeamSemester.objects.select_related(
                "team",
                "team__home_study_group",
                "semester",
                "captain",
                "mentor",
                "project_application",
            )
            .prefetch_related("members__user")
            .filter(semester_id=semester_id, members__user=request.user)
            .distinct()
        )
        serializer = TeamSemesterSerializer(queryset, many=True)
        return Response(serializer.data)


class TeamSemesterViewSet(viewsets.ModelViewSet):
    """CRUD для участия команды в семестре и управления составом."""

    queryset = TeamSemester.objects.select_related(
        "team",
        "team__home_study_group",
        "semester",
        "captain",
        "mentor",
        "project_application",
    ).prefetch_related("members__user")
    serializer_class = TeamSemesterSerializer
    permission_classes = [IsAuthenticated, TeamSemesterPermission]

    def get_queryset(self):
        queryset = super().get_queryset()
        raw = self.request.query_params.get("semester_id")
        if raw is None or getattr(self, "action", None) != "list":
            return queryset
        semester_id = Semester.resolve_list_semester_id(raw)
        return queryset.filter(semester_id=semester_id)

    def list(self, request: Request, *args, **kwargs) -> Response:
        try:
            return super().list(request, *args, **kwargs)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        captain = serializer.validated_data.get("captain") or self.request.user
        team_semester = serializer.save(captain=captain)
        TeamSemesterMember.objects.get_or_create(
            team_semester=team_semester,
            user=captain,
            defaults={
                "semester_id": team_semester.semester_id,
                "role": TeamSemesterMember.Role.LEADER,
            },
        )

    @decorators.action(detail=False, methods=["get"], url_path="my")
    def my_team_semesters(self, request: Request) -> Response:
        """GET /api/teams/team-semesters/my/?semester_id= — команды пользователя."""
        try:
            semester_id = Semester.resolve_list_semester_id(
                request.query_params.get("semester_id")
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        queryset = (
            self.get_queryset()
            .filter(semester_id=semester_id, members__user=request.user)
            .distinct()
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @decorators.action(detail=True, methods=["post"], url_path="members")
    def add_member(self, request: Request, pk: int = None) -> Response:
        """POST /api/teams/team-semesters/{id}/members/ — добавить участника."""
        team_semester = self.get_object()
        serializer = TeamSemesterMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        role = serializer.validated_data.get("role", TeamSemesterMember.Role.MEMBER)

        if TeamSemesterMember.objects.filter(
            team_semester=team_semester, user=user
        ).exists():
            return Response(
                {"error": "Пользователь уже состоит в команде"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if TeamSemesterMember.objects.filter(
            user=user, semester_id=team_semester.semester_id
        ).exists():
            return Response(
                {"error": "Пользователь уже состоит в команде в этом семестре"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        member = TeamSemesterMember.objects.create(
            team_semester=team_semester,
            user=user,
            role=role,
        )
        return Response(
            TeamSemesterMemberSerializer(member).data,
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
        """DELETE /api/teams/team-semesters/{id}/members/{member_id}/."""
        team_semester = self.get_object()
        member = team_semester.members.filter(pk=member_id).first()
        if not member:
            return Response(
                {"error": "Участник не найден"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if member.role == TeamSemesterMember.Role.LEADER:
            return Response(
                {"error": "Нельзя удалить руководителя команды"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

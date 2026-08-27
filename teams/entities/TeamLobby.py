"""API лобби формирования команд и «Моей команды»."""

from __future__ import annotations

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from teams.dto.team_lobby import MyTeamEventLogDTO
from teams.models import TeamSemesterMember
from teams.permissions import StudentWithStudyGroupPermission
from teams.services.team_lobby_service import TeamLobbyService


class TeamEventLogPagination(PageNumberPagination):
    """Пагинация ленты событий команды (фиксированный page_size=50)."""

    page_size = 50


_SEMESTER_PARAM = OpenApiParameter(
    name="semester_id",
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    required=False,
    description="ID семестра либо actual / next (по умолчанию actual)",
)


class CreateTeamSerializer(serializers.Serializer):
    """Создание команды в лобби."""

    track_id = serializers.IntegerField(min_value=1, required=False, allow_null=True)
    name = serializers.CharField(max_length=255)


class ApproveJoinRequestSerializer(serializers.Serializer):
    """Одобрение заявки с назначением роли."""

    role = serializers.ChoiceField(
        choices=[
            (TeamSemesterMember.Role.MEMBER, "Участник"),
        ],
        default=TeamSemesterMember.Role.MEMBER,
    )


class CreateInvitationSerializer(serializers.Serializer):
    """Приглашение одногруппника."""

    user_id = serializers.IntegerField(min_value=1)
    role = serializers.ChoiceField(
        choices=[
            (TeamSemesterMember.Role.MEMBER, "Участник"),
        ],
        default=TeamSemesterMember.Role.MEMBER,
    )


@extend_schema_view(
    list=extend_schema(
        tags=["teams-lobby"],
        parameters=[_SEMESTER_PARAM],
        summary="Лобби формирования команд",
    ),
)
class TeamLobbyViewSet(viewsets.ViewSet):
    """Студенческое лобби: треки, команды, заявки, приглашения."""

    permission_classes = [IsAuthenticated, StudentWithStudyGroupPermission]
    pagination_class = None

    def list(self, request: Request) -> Response:
        """GET /api/teams/lobby/."""
        try:
            service = TeamLobbyService()
            data = service.get_lobby(
                request.user,
                request.query_params.get("semester_id"),
            )
            return Response(data)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_403_FORBIDDEN)

    @extend_schema(tags=["teams-lobby"], request=CreateTeamSerializer)
    @action(detail=False, methods=["post"], url_path="teams")
    def create_team(self, request: Request) -> Response:
        """POST /api/teams/lobby/teams/."""
        serializer = CreateTeamSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            service = TeamLobbyService()
            result = service.create_team(
                request.user,
                track_id=serializer.validated_data.get("track_id"),
                name=serializer.validated_data["name"],
                semester_id_raw=request.query_params.get("semester_id"),
            )
            return Response(result, status=status.HTTP_201_CREATED)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_403_FORBIDDEN)

    @extend_schema(tags=["teams-lobby"])
    @action(
        detail=False,
        methods=["post"],
        url_path=r"teams/(?P<team_semester_id>\d+)/join-requests",
    )
    def create_join_request(self, request: Request, team_semester_id: int) -> Response:
        """POST /api/teams/lobby/teams/{id}/join-requests/."""
        try:
            service = TeamLobbyService()
            result = service.create_join_request(
                request.user,
                int(team_semester_id),
                request.query_params.get("semester_id"),
            )
            return Response(result, status=status.HTTP_201_CREATED)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_403_FORBIDDEN)

    @extend_schema(tags=["teams-lobby"])
    @action(
        detail=False,
        methods=["post"],
        url_path=r"invitations/(?P<invitation_id>\d+)/accept",
    )
    def accept_invitation(self, request: Request, invitation_id: int) -> Response:
        """POST /api/teams/lobby/invitations/{id}/accept/."""
        try:
            service = TeamLobbyService()
            result = service.accept_invitation(request.user, int(invitation_id))
            return Response(result)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_403_FORBIDDEN)

    @extend_schema(tags=["teams-lobby"])
    @action(
        detail=False,
        methods=["post"],
        url_path=r"invitations/(?P<invitation_id>\d+)/reject",
    )
    def reject_invitation(self, request: Request, invitation_id: int) -> Response:
        """POST /api/teams/lobby/invitations/{id}/reject/."""
        try:
            service = TeamLobbyService()
            result = service.reject_invitation(request.user, int(invitation_id))
            return Response(result)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_403_FORBIDDEN)


@extend_schema_view(
    list=extend_schema(
        tags=["teams-my-team"],
        parameters=[_SEMESTER_PARAM],
        summary="Моя команда",
    ),
)
class MyTeamViewSet(viewsets.ViewSet):
    """Раздел «Моя команда» для капитана и участника."""

    permission_classes = [IsAuthenticated, StudentWithStudyGroupPermission]
    pagination_class = None

    def list(self, request: Request) -> Response:
        """GET /api/teams/my-team/."""
        try:
            service = TeamLobbyService()
            data = service.get_my_team(
                request.user,
                request.query_params.get("semester_id"),
            )
            return Response(data)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_403_FORBIDDEN)

    @extend_schema(
        tags=["teams-my-team"],
        parameters=[_SEMESTER_PARAM],
        summary="Лог событий моей команды",
    )
    def event_log(self, request: Request) -> Response:
        """GET /api/teams/my-team/event-log/ — пагинированный лог (page_size=50)."""
        try:
            service = TeamLobbyService()
            queryset = service.get_my_team_event_logs(
                request.user,
                request.query_params.get("semester_id"),
            )
            paginator = TeamEventLogPagination()
            page = paginator.paginate_queryset(queryset, request, view=self)
            results = [MyTeamEventLogDTO(log).to_dict() for log in page]
            return paginator.get_paginated_response(results)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_403_FORBIDDEN)

    def delete_team(self, request: Request) -> Response:
        """DELETE /api/teams/my-team/ — удалить свою команду."""
        try:
            service = TeamLobbyService()
            service.delete_my_team(
                request.user,
                request.query_params.get("semester_id"),
            )
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_403_FORBIDDEN)

    @extend_schema(tags=["teams-my-team"], request=ApproveJoinRequestSerializer)
    def approve_join_request(self, request: Request, join_request_id: int) -> Response:
        """POST /api/teams/my-team/join-requests/{id}/approve/."""
        serializer = ApproveJoinRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            service = TeamLobbyService()
            result = service.approve_join_request(
                request.user,
                int(join_request_id),
                role=serializer.validated_data["role"],
                semester_id_raw=request.query_params.get("semester_id"),
            )
            return Response(result)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_403_FORBIDDEN)

    @extend_schema(tags=["teams-my-team"])
    def reject_join_request(self, request: Request, join_request_id: int) -> Response:
        """POST /api/teams/my-team/join-requests/{id}/reject/."""
        try:
            service = TeamLobbyService()
            result = service.reject_join_request(
                request.user,
                int(join_request_id),
                request.query_params.get("semester_id"),
            )
            return Response(result)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_403_FORBIDDEN)

    @extend_schema(tags=["teams-my-team"], request=CreateInvitationSerializer)
    def create_invitation(self, request: Request) -> Response:
        """POST /api/teams/my-team/invitations/."""
        serializer = CreateInvitationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            service = TeamLobbyService()
            result = service.create_invitation(
                request.user,
                invitee_user_id=serializer.validated_data["user_id"],
                role=serializer.validated_data["role"],
                semester_id_raw=request.query_params.get("semester_id"),
            )
            return Response(result, status=status.HTTP_201_CREATED)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_403_FORBIDDEN)

    @extend_schema(tags=["teams-my-team"])
    def kick_member(self, request: Request, user_id: int) -> Response:
        """DELETE /api/teams/my-team/members/{user_id}/."""
        try:
            service = TeamLobbyService()
            result = service.kick_member(
                request.user,
                int(user_id),
                request.query_params.get("semester_id"),
            )
            return Response(result)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_403_FORBIDDEN)

    @extend_schema(tags=["teams-my-team"])
    def leave(self, request: Request) -> Response:
        """POST /api/teams/my-team/leave/."""
        try:
            service = TeamLobbyService()
            service.leave_team(
                request.user,
                request.query_params.get("semester_id"),
            )
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_403_FORBIDDEN)

    @extend_schema(tags=["teams-my-team"])
    def confirm_composition(self, request: Request) -> Response:
        """POST /api/teams/my-team/confirm-composition/."""
        try:
            service = TeamLobbyService()
            result = service.confirm_composition(
                request.user,
                request.query_params.get("semester_id"),
            )
            return Response(result)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_403_FORBIDDEN)

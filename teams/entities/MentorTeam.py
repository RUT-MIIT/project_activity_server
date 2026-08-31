"""ViewSet управления командой учебной группы для наставника."""

from __future__ import annotations

from rest_framework import serializers, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from teams.domain.mentor_team import TeamEnrolledInProjectError
from teams.services.mentor_team_service import MentorTeamService


class MentorTeamCreateSerializer(serializers.Serializer):
    """Тело POST создания команды."""

    name = serializers.CharField(max_length=255)
    captainId = serializers.IntegerField(min_value=1)


class MentorTeamUpdateNameSerializer(serializers.Serializer):
    """Тело PATCH переименования команды."""

    name = serializers.CharField(max_length=255)


class MentorTeamSetCaptainSerializer(serializers.Serializer):
    """Тело PATCH назначения капитана."""

    captainId = serializers.IntegerField(min_value=1)


class MentorTeamAddMemberSerializer(serializers.Serializer):
    """Тело POST добавления участника."""

    userId = serializers.IntegerField(min_value=1, required=False)
    preRegisteredStudentId = serializers.IntegerField(min_value=1, required=False)

    def validate(self, attrs: dict) -> dict:
        """Требует ровно один идентификатор участника."""
        has_user = attrs.get("userId") is not None
        has_pre_registered = attrs.get("preRegisteredStudentId") is not None
        if has_user == has_pre_registered:
            raise serializers.ValidationError(
                "Укажите userId или preRegisteredStudentId"
            )
        return attrs


class MentorTeamViewSet(viewsets.ViewSet):
    """API наставника для управления командой группы в семестре."""

    permission_classes = [IsAuthenticated]

    def _semester_id_raw(self, request: Request) -> str | None:
        return request.query_params.get("semester_id")

    def _handle_errors(self, handler):
        """Общая обработка исключений сервиса."""
        try:
            return handler()
        except TeamEnrolledInProjectError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_409_CONFLICT)
        except PermissionError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_403_FORBIDDEN)
        except LookupError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request: Request, group_id: int) -> Response:
        """POST /study-groups/{groupId}/teams/ — создать команду."""
        serializer = MentorTeamCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = MentorTeamService()

        def action() -> Response:
            data = service.create_team(
                request.user,
                group_id=group_id,
                name=serializer.validated_data["name"],
                captain_id=serializer.validated_data["captainId"],
                semester_id_raw=self._semester_id_raw(request),
            )
            return Response(data, status=status.HTTP_201_CREATED)

        return self._handle_errors(action)

    def retrieve(
        self,
        request: Request,
        group_id: int,
        team_semester_id: int,
    ) -> Response:
        """GET /study-groups/{groupId}/teams/{teamSemesterId}/ — карточка команды."""
        service = MentorTeamService()

        def action() -> Response:
            data = service.get_detail(
                request.user,
                group_id=group_id,
                team_semester_id=team_semester_id,
                semester_id_raw=self._semester_id_raw(request),
            )
            return Response(data)

        return self._handle_errors(action)

    def partial_update(
        self,
        request: Request,
        group_id: int,
        team_semester_id: int,
    ) -> Response:
        """PATCH /study-groups/{groupId}/teams/{teamSemesterId}/ — название."""
        serializer = MentorTeamUpdateNameSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        service = MentorTeamService()

        def action() -> Response:
            data = service.update_name(
                request.user,
                group_id=group_id,
                team_semester_id=team_semester_id,
                name=serializer.validated_data["name"],
                semester_id_raw=self._semester_id_raw(request),
            )
            return Response(data)

        return self._handle_errors(action)

    def destroy(
        self,
        request: Request,
        group_id: int,
        team_semester_id: int,
    ) -> Response:
        """DELETE /study-groups/{groupId}/teams/{teamSemesterId}/ — удалить команду."""
        service = MentorTeamService()

        def action() -> Response:
            data = service.delete_team(
                request.user,
                group_id=group_id,
                team_semester_id=team_semester_id,
                semester_id_raw=self._semester_id_raw(request),
            )
            return Response(data)

        return self._handle_errors(action)

    def set_captain(
        self,
        request: Request,
        group_id: int,
        team_semester_id: int,
    ) -> Response:
        """PATCH /study-groups/{groupId}/teams/{teamSemesterId}/captain/."""
        serializer = MentorTeamSetCaptainSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = MentorTeamService()

        def action() -> Response:
            data = service.set_captain(
                request.user,
                group_id=group_id,
                team_semester_id=team_semester_id,
                captain_id=serializer.validated_data["captainId"],
                semester_id_raw=self._semester_id_raw(request),
            )
            return Response(data)

        return self._handle_errors(action)

    def confirm_composition(
        self,
        request: Request,
        group_id: int,
        team_semester_id: int,
    ) -> Response:
        """POST /study-groups/{groupId}/teams/{teamSemesterId}/confirm-composition/."""
        service = MentorTeamService()

        def action() -> Response:
            data = service.confirm_composition(
                request.user,
                group_id=group_id,
                team_semester_id=team_semester_id,
                semester_id_raw=self._semester_id_raw(request),
            )
            return Response(data)

        return self._handle_errors(action)

    def unconfirm_composition(
        self,
        request: Request,
        group_id: int,
        team_semester_id: int,
    ) -> Response:
        """POST .../unconfirm-composition/ — вернуть состав на редактирование."""
        service = MentorTeamService()

        def action() -> Response:
            data = service.unconfirm_composition(
                request.user,
                group_id=group_id,
                team_semester_id=team_semester_id,
                semester_id_raw=self._semester_id_raw(request),
            )
            return Response(data)

        return self._handle_errors(action)

    def add_member(
        self,
        request: Request,
        group_id: int,
        team_semester_id: int,
    ) -> Response:
        """POST /study-groups/{groupId}/teams/{teamSemesterId}/members/."""
        serializer = MentorTeamAddMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = MentorTeamService()

        def action() -> Response:
            data = service.add_member(
                request.user,
                group_id=group_id,
                team_semester_id=team_semester_id,
                semester_id_raw=self._semester_id_raw(request),
                user_id=serializer.validated_data.get("userId"),
                pre_registered_student_id=serializer.validated_data.get(
                    "preRegisteredStudentId"
                ),
            )
            return Response(data)

        return self._handle_errors(action)

    def remove_member(
        self,
        request: Request,
        group_id: int,
        team_semester_id: int,
        user_id: int,
    ) -> Response:
        """DELETE /study-groups/{groupId}/teams/{teamSemesterId}/members/{userId}/."""
        service = MentorTeamService()

        def action() -> Response:
            data = service.remove_member(
                request.user,
                group_id=group_id,
                team_semester_id=team_semester_id,
                member_user_id=user_id,
                semester_id_raw=self._semester_id_raw(request),
            )
            return Response(data)

        return self._handle_errors(action)

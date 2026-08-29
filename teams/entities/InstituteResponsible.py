"""ViewSet API ответственного по институтам."""

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from teams.domain.institute_access import MANAGEMENT_ROLES
from teams.services.institute_responsible_service import InstituteResponsibleService

_SEMESTER_PARAM = OpenApiParameter(
    name="semester_id",
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    required=True,
    description="ID семестра либо actual / next",
)
_INSTITUTE_PARAM = OpenApiParameter(
    name="institute_code",
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    required=False,
)
_MENTOR_PARAM = OpenApiParameter(
    name="mentor_id",
    type=OpenApiTypes.INT,
    location=OpenApiParameter.QUERY,
    required=True,
    description="ID наставника для снятия с группы",
)


class AssignMentorSerializer(serializers.Serializer):
    """Тело запроса на назначение наставника."""

    mentorId = serializers.IntegerField(min_value=1)


class InstituteResponsiblePermission(BasePermission):
    """Доступ для institute_validator, admin и cpds."""

    message = "Недостаточно прав для управления наставниками институтов"

    def has_permission(self, request: Request, view) -> bool:
        user = request.user if request.user.is_authenticated else None
        if not user:
            return False
        if user.is_staff:
            return True
        return bool(user.role and user.role.code in MANAGEMENT_ROLES)


class InstituteResponsibleViewSet(viewsets.ViewSet):
    """API ответственного по институтам: группы, сотрудники, наставники."""

    permission_classes = [IsAuthenticated, InstituteResponsiblePermission]

    @staticmethod
    def _parse_institute_code(request: Request) -> str | None:
        return request.query_params.get("institute_code") or None

    @staticmethod
    def _validate_semester_param(semester_id_raw: str | None) -> Response | None:
        if semester_id_raw is None:
            return Response(
                {"error": "semester_id не передан"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return None

    @extend_schema(
        tags=["teams"],
        parameters=[_SEMESTER_PARAM, _INSTITUTE_PARAM],
        summary="Активные группы института",
    )
    @action(detail=False, methods=["get"], url_path="groups")
    def list_groups(self, request: Request) -> Response:
        """GET /api/teams/institute-responsible/groups/."""
        semester_id_raw = request.query_params.get("semester_id")
        error_response = self._validate_semester_param(semester_id_raw)
        if error_response is not None:
            return error_response

        try:
            service = InstituteResponsibleService()
            items = service.list_groups(
                request.user,
                self._parse_institute_code(request),
                semester_id_raw,
            )
            return Response(items)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_403_FORBIDDEN)

    @extend_schema(
        tags=["teams"],
        parameters=[_INSTITUTE_PARAM],
        summary="Сотрудники института",
    )
    @action(detail=False, methods=["get"], url_path="employees")
    def list_employees(self, request: Request) -> Response:
        """GET /api/teams/institute-responsible/employees/."""
        try:
            service = InstituteResponsibleService()
            items = service.list_employees(
                request.user,
                self._parse_institute_code(request),
            )
            return Response(items)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_403_FORBIDDEN)

    @extend_schema(
        tags=["teams"],
        parameters=[_SEMESTER_PARAM, _INSTITUTE_PARAM],
        summary="Группы и назначения наставников",
    )
    @action(detail=False, methods=["get"], url_path="group-mentors")
    def list_group_mentors(self, request: Request) -> Response:
        """GET /api/teams/institute-responsible/group-mentors/."""
        semester_id_raw = request.query_params.get("semester_id")
        error_response = self._validate_semester_param(semester_id_raw)
        if error_response is not None:
            return error_response

        try:
            service = InstituteResponsibleService()
            data = service.list_group_mentors(
                request.user,
                self._parse_institute_code(request),
                semester_id_raw,
            )
            return Response(data)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_403_FORBIDDEN)

    @extend_schema(
        tags=["teams"],
        parameters=[_SEMESTER_PARAM, _INSTITUTE_PARAM],
        request=AssignMentorSerializer,
        summary="Назначить наставника группе",
    )
    @action(
        detail=False,
        methods=["post"],
        url_path=r"groups/(?P<group_id>\d+)/mentor",
    )
    def assign_mentor(self, request: Request, group_id: int) -> Response:
        """POST /api/teams/institute-responsible/groups/{id}/mentor/."""
        group_id = int(group_id)
        semester_id_raw = request.query_params.get("semester_id")
        error_response = self._validate_semester_param(semester_id_raw)
        if error_response is not None:
            return error_response

        serializer = AssignMentorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            service = InstituteResponsibleService()
            result = service.assign_mentor(
                request.user,
                group_id,
                serializer.validated_data["mentorId"],
                self._parse_institute_code(request),
                semester_id_raw,
            )
            return Response(result)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_403_FORBIDDEN)

    @extend_schema(
        tags=["teams"],
        parameters=[_SEMESTER_PARAM, _INSTITUTE_PARAM, _MENTOR_PARAM],
        summary="Снять наставника с группы",
    )
    @assign_mentor.mapping.delete
    def remove_mentor(self, request: Request, group_id: int) -> Response:
        """DELETE /api/teams/institute-responsible/groups/{id}/mentor/."""
        group_id = int(group_id)
        semester_id_raw = request.query_params.get("semester_id")
        error_response = self._validate_semester_param(semester_id_raw)
        if error_response is not None:
            return error_response

        mentor_id_raw = request.query_params.get("mentor_id")
        if mentor_id_raw is None:
            return Response(
                {"error": "mentor_id не передан"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            mentor_id = int(mentor_id_raw)
        except ValueError:
            return Response(
                {"error": "mentor_id должен быть числом"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if mentor_id <= 0:
            return Response(
                {"error": "Некорректный mentor_id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            service = InstituteResponsibleService()
            result = service.remove_mentor(
                request.user,
                group_id,
                mentor_id,
                self._parse_institute_code(request),
                semester_id_raw,
            )
            return Response(result)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_403_FORBIDDEN)

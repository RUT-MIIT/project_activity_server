"""ViewSet для проектных треков."""

from rest_framework import serializers, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from accounts.permissions import ProjectTrackPermission
from showcase.dto.project_track import ProjectTrackAssignDTO, ProjectTrackDeleteDTO
from showcase.services.project_track_service import ProjectTrackService


class ProjectTrackAssignSerializer(serializers.Serializer):
    """Сериализатор для массового назначения групп на проекты."""

    semester_id = serializers.IntegerField(required=True)
    group_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        allow_empty=False,
        required=True,
    )
    project_application_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        allow_empty=False,
        required=True,
    )


class ProjectTrackDeleteSerializer(serializers.Serializer):
    """Сериализатор для удаления связки группа — проект."""

    semester_id = serializers.IntegerField(required=True)
    group_id = serializers.IntegerField(min_value=1, required=True)
    project_application_id = serializers.IntegerField(min_value=1, required=True)


class ProjectTrackViewSet(viewsets.ViewSet):
    """API для проектных треков: список, массовое назначение, удаление."""

    permission_classes = [IsAuthenticated, ProjectTrackPermission]
    pagination_class = None

    @staticmethod
    def _parse_query_params(request: Request) -> tuple[str | None, str | None]:
        """Извлекает institute_code и semester_id из query-параметров."""
        return (
            request.query_params.get("institute_code"),
            request.query_params.get("semester_id"),
        )

    @staticmethod
    def _validate_semester_param(semester_id_raw: str | None) -> Response | None:
        """Проверяет обязательный semester_id; institute_code опционален."""
        if semester_id_raw is None:
            return Response(
                {"error": "Параметр semester_id обязателен"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return None

    def list(self, request: Request) -> Response:
        """GET /api/showcase/project-tracks/?institute_code=...&semester_id=..."""
        institute_code = request.query_params.get("institute_code")
        semester_id_raw = request.query_params.get("semester_id")

        if not institute_code:
            return Response(
                {"error": "Параметр institute_code обязателен"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if semester_id_raw is None:
            return Response(
                {"error": "Параметр semester_id обязателен"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            service = ProjectTrackService()
            queryset = service.list_tracks(
                request.user, institute_code, semester_id_raw
            )
            items = service.serialize_list(queryset)
            return Response(items)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_403_FORBIDDEN)

    def list_groups(self, request: Request) -> Response:
        """GET /api/showcase/project-tracks/groups/?semester_id=...&institute_code=..."""
        institute_code, semester_id_raw = self._parse_query_params(request)
        error_response = self._validate_semester_param(semester_id_raw)
        if error_response is not None:
            return error_response

        try:
            service = ProjectTrackService()
            items = service.list_groups(request.user, institute_code, semester_id_raw)
            return Response(items)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_403_FORBIDDEN)

    def retrieve_group(self, request: Request, group_id: int) -> Response:
        """GET /api/showcase/project-tracks/groups/{id}/?semester_id=...&institute_code=..."""
        institute_code, semester_id_raw = self._parse_query_params(request)
        error_response = self._validate_semester_param(semester_id_raw)
        if error_response is not None:
            return error_response

        try:
            service = ProjectTrackService()
            detail = service.get_group_detail(
                request.user, group_id, institute_code, semester_id_raw
            )
            return Response(detail)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_403_FORBIDDEN)

    def statistics(self, request: Request) -> Response:
        """GET /api/showcase/project-tracks/statistics/?semester_id=...&institute_code=..."""
        institute_code, semester_id_raw = self._parse_query_params(request)
        error_response = self._validate_semester_param(semester_id_raw)
        if error_response is not None:
            return error_response

        try:
            service = ProjectTrackService()
            stats = service.get_statistics(
                request.user, institute_code, semester_id_raw
            )
            return Response(stats)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_403_FORBIDDEN)

    def create(self, request: Request) -> Response:
        """POST /api/showcase/project-tracks/ — массовое назначение."""
        serializer = ProjectTrackAssignSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            service = ProjectTrackService()
            dto = ProjectTrackAssignDTO.from_dict(serializer.validated_data)
            result = service.bulk_assign(request.user, dto)
            return Response(result.to_dict(), status=status.HTTP_201_CREATED)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_403_FORBIDDEN)

    def remove(self, request: Request) -> Response:
        """DELETE /api/showcase/project-tracks/ — удаление связки по body."""
        serializer = ProjectTrackDeleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            service = ProjectTrackService()
            dto = ProjectTrackDeleteDTO.from_dict(serializer.validated_data)
            service.delete_track(request.user, dto)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_403_FORBIDDEN)

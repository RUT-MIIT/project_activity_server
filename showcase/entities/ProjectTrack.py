"""ViewSet для проектных треков."""

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from accounts.permissions import ProjectTrackPermission
from showcase.constants import DEFAULT_MAX_TEAM_MEMBERS, DEFAULT_MIN_TEAM_MEMBERS
from showcase.dto.project_track import (
    ProjectTrackAddApplicationsDTO,
    ProjectTrackAddGroupsDTO,
    ProjectTrackCreateDTO,
    ProjectTrackUpdateDTO,
)
from showcase.services.project_track_service import ProjectTrackService

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
_DEPARTMENT_PARAM = OpenApiParameter(
    name="department_id",
    type=OpenApiTypes.INT,
    location=OpenApiParameter.QUERY,
    required=False,
)


class ProjectTrackCreateSerializer(serializers.Serializer):
    """Сериализатор для создания проектного трека."""

    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True, default="")
    department_id = serializers.IntegerField(min_value=1)
    semester_id = serializers.IntegerField(min_value=1)
    minTeamMembers = serializers.IntegerField(
        min_value=1, required=False, default=DEFAULT_MIN_TEAM_MEMBERS
    )
    maxTeamMembers = serializers.IntegerField(
        min_value=1, required=False, default=DEFAULT_MAX_TEAM_MEMBERS
    )

    def validate(self, attrs: dict[str, int]) -> dict[str, int]:
        """Проверяет согласованность лимитов размера команды."""
        min_members = attrs.get("minTeamMembers", DEFAULT_MIN_TEAM_MEMBERS)
        max_members = attrs.get("maxTeamMembers", DEFAULT_MAX_TEAM_MEMBERS)
        if min_members > max_members:
            raise serializers.ValidationError(
                {
                    "minTeamMembers": (
                        "Минимальное количество человек не может быть "
                        "больше максимального."
                    )
                }
            )
        return attrs


class ProjectTrackUpdateSerializer(serializers.Serializer):
    """Сериализатор для обновления проектного трека."""

    name = serializers.CharField(max_length=255, required=False)
    description = serializers.CharField(required=False, allow_blank=True)
    department_id = serializers.IntegerField(min_value=1, required=False)
    semester_id = serializers.IntegerField(min_value=1, required=False)
    minTeamMembers = serializers.IntegerField(min_value=1, required=False)
    maxTeamMembers = serializers.IntegerField(min_value=1, required=False)

    def validate(self, attrs: dict[str, int]) -> dict[str, int]:
        """Проверяет согласованность лимитов размера команды."""
        min_members = attrs.get("minTeamMembers")
        max_members = attrs.get("maxTeamMembers")
        if (
            min_members is not None
            and max_members is not None
            and min_members > max_members
        ):
            raise serializers.ValidationError(
                {
                    "minTeamMembers": (
                        "Минимальное количество человек не может быть "
                        "больше максимального."
                    )
                }
            )
        return attrs


class ProjectTrackAddGroupsSerializer(serializers.Serializer):
    """Сериализатор для добавления групп в трек."""

    group_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        allow_empty=False,
    )


class ProjectTrackAddApplicationItemSerializer(serializers.Serializer):
    """Элемент списка заявок для добавления в трек."""

    id = serializers.IntegerField(min_value=1)
    teamsCount = serializers.IntegerField(min_value=1)
    minTeamMembers = serializers.IntegerField(min_value=1)
    maxTeamMembers = serializers.IntegerField(min_value=1)

    def validate(self, attrs: dict[str, int]) -> dict[str, int]:
        """Проверяет, что minTeamMembers не больше maxTeamMembers."""
        if attrs["minTeamMembers"] > attrs["maxTeamMembers"]:
            raise serializers.ValidationError(
                {
                    "minTeamMembers": (
                        "Минимальное количество человек не может быть "
                        "больше максимального."
                    )
                }
            )
        return attrs


class ProjectTrackAddApplicationsSerializer(serializers.ListSerializer):
    """Список заявок с рекомендуемым числом команд и лимитами размера."""

    child = ProjectTrackAddApplicationItemSerializer()

    def validate(self, data: list[dict[str, int]]) -> list[dict[str, int]]:
        """Проверяет отсутствие дубликатов id в одном запросе."""
        if not data:
            raise serializers.ValidationError("Список заявок не может быть пустым")
        ids = [item["id"] for item in data]
        if len(ids) != len(set(ids)):
            raise serializers.ValidationError(
                "id заявок в запросе не должны повторяться"
            )
        return data


@extend_schema_view(
    list=extend_schema(
        tags=["showcase"],
        parameters=[_SEMESTER_PARAM, _DEPARTMENT_PARAM, _INSTITUTE_PARAM],
        summary="Список проектных треков",
    ),
    create=extend_schema(
        tags=["showcase"],
        request=ProjectTrackCreateSerializer,
        summary="Создать проектный трек",
    ),
    retrieve=extend_schema(tags=["showcase"], summary="Детали проектного трека"),
    partial_update=extend_schema(
        tags=["showcase"],
        request=ProjectTrackUpdateSerializer,
        summary="Обновить проектный трек",
    ),
    destroy=extend_schema(tags=["showcase"], summary="Удалить проектный трек"),
)
class ProjectTrackViewSet(viewsets.ViewSet):
    """API для проектных треков: CRUD и управление составом."""

    permission_classes = [IsAuthenticated, ProjectTrackPermission]
    pagination_class = None
    serializer_class = ProjectTrackCreateSerializer

    @staticmethod
    def _parse_query_params(request: Request) -> tuple[str | None, str | None]:
        """Извлекает institute_code и semester_id из query-параметров."""
        return (
            request.query_params.get("institute_code"),
            request.query_params.get("semester_id"),
        )

    @staticmethod
    def _validate_semester_param(semester_id_raw: str | None) -> Response | None:
        """Проверяет обязательный semester_id."""
        if semester_id_raw is None:
            return Response(
                {"error": "Параметр semester_id обязателен"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return None

    def list(self, request: Request) -> Response:
        """GET /api/showcase/project-tracks/ с фильтрами semester_id, department_id."""
        semester_id_raw = request.query_params.get("semester_id")
        error_response = self._validate_semester_param(semester_id_raw)
        if error_response is not None:
            return error_response

        department_id_raw = request.query_params.get("department_id")
        department_id = int(department_id_raw) if department_id_raw else None
        institute_code = request.query_params.get("institute_code")

        try:
            service = ProjectTrackService()
            queryset = service.list_tracks(
                request.user,
                semester_id_raw,
                department_id=department_id,
                institute_code=institute_code,
            )
            items = service.serialize_list(queryset)
            return Response(items)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_403_FORBIDDEN)

    def create(self, request: Request) -> Response:
        """POST /api/showcase/project-tracks/ — создание трека."""
        serializer = ProjectTrackCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            service = ProjectTrackService()
            dto = ProjectTrackCreateDTO.from_dict(serializer.validated_data)
            result = service.create_track(request.user, dto)
            return Response(result, status=status.HTTP_201_CREATED)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request: Request, pk: int) -> Response:
        """GET /api/showcase/project-tracks/{id}/."""
        try:
            service = ProjectTrackService()
            detail = service.get_track(request.user, pk)
            return Response(detail)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request: Request, pk: int) -> Response:
        """PATCH /api/showcase/project-tracks/{id}/."""
        serializer = ProjectTrackUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        try:
            service = ProjectTrackService()
            dto = ProjectTrackUpdateDTO.from_dict(serializer.validated_data)
            result = service.update_track(request.user, pk, dto)
            return Response(result)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request: Request, pk: int) -> Response:
        """DELETE /api/showcase/project-tracks/{id}/."""
        try:
            service = ProjectTrackService()
            service.delete_track(request.user, pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_403_FORBIDDEN)

    @extend_schema(tags=["showcase"], request=ProjectTrackAddGroupsSerializer)
    @action(detail=True, methods=["post"], url_path="groups")
    def add_groups(self, request: Request, pk: int) -> Response:
        """POST /api/showcase/project-tracks/{id}/groups/."""
        serializer = ProjectTrackAddGroupsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            service = ProjectTrackService()
            dto = ProjectTrackAddGroupsDTO.from_dict(serializer.validated_data)
            result = service.add_groups_to_track(request.user, pk, dto)
            return Response(result)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_403_FORBIDDEN)

    @extend_schema(tags=["showcase"])
    @action(
        detail=True,
        methods=["delete"],
        url_path=r"groups/(?P<group_id>\d+)",
    )
    def remove_group(self, request: Request, pk: int, group_id: int) -> Response:
        """DELETE /api/showcase/project-tracks/{id}/groups/{group_id}/."""
        try:
            service = ProjectTrackService()
            result = service.remove_group_from_track(request.user, pk, group_id)
            return Response(result)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_403_FORBIDDEN)

    @extend_schema(tags=["showcase"], request=ProjectTrackAddApplicationsSerializer)
    @action(detail=True, methods=["post"], url_path="applications")
    def add_applications(self, request: Request, pk: int) -> Response:
        """POST /api/showcase/project-tracks/{id}/applications/."""
        serializer = ProjectTrackAddApplicationsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            service = ProjectTrackService()
            dto = ProjectTrackAddApplicationsDTO.from_items(serializer.validated_data)
            result = service.add_applications_to_track(request.user, pk, dto)
            return Response(result)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_403_FORBIDDEN)

    @extend_schema(tags=["showcase"])
    @action(
        detail=True,
        methods=["delete"],
        url_path=r"applications/(?P<application_id>\d+)",
    )
    def remove_application(
        self, request: Request, pk: int, application_id: int
    ) -> Response:
        """DELETE /api/showcase/project-tracks/{id}/applications/{application_id}/."""
        try:
            service = ProjectTrackService()
            result = service.remove_application_from_track(
                request.user, pk, application_id
            )
            return Response(result)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_403_FORBIDDEN)

    @extend_schema(
        tags=["showcase"],
        parameters=[_SEMESTER_PARAM, _INSTITUTE_PARAM],
        summary="Учебные группы института через треки",
    )
    @action(detail=False, methods=["get"], url_path="groups")
    def list_groups(self, request: Request) -> Response:
        """GET /api/showcase/project-tracks/groups/."""
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

    @extend_schema(
        tags=["showcase"],
        parameters=[_SEMESTER_PARAM, _INSTITUTE_PARAM],
        summary="Детали учебной группы через треки",
    )
    @action(
        detail=False,
        methods=["get"],
        url_path=r"groups/(?P<group_id>\d+)",
    )
    def retrieve_group(self, request: Request, group_id: int) -> Response:
        """GET /api/showcase/project-tracks/groups/{id}/."""
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

    @extend_schema(
        tags=["showcase"],
        parameters=[_SEMESTER_PARAM, _INSTITUTE_PARAM],
        summary="Проекты (заявки) института через треки",
    )
    @action(detail=False, methods=["get"], url_path="projects")
    def list_projects(self, request: Request) -> Response:
        """GET /api/showcase/project-tracks/projects/."""
        institute_code, semester_id_raw = self._parse_query_params(request)
        error_response = self._validate_semester_param(semester_id_raw)
        if error_response is not None:
            return error_response

        try:
            service = ProjectTrackService()
            items = service.list_projects(request.user, institute_code, semester_id_raw)
            return Response(items)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_403_FORBIDDEN)

    @extend_schema(
        tags=["showcase"],
        parameters=[_SEMESTER_PARAM, _INSTITUTE_PARAM],
        summary="Детали проекта через треки",
    )
    @action(
        detail=False,
        methods=["get"],
        url_path=r"projects/(?P<project_id>\d+)",
    )
    def retrieve_project(self, request: Request, project_id: int) -> Response:
        """GET /api/showcase/project-tracks/projects/{id}/."""
        institute_code, semester_id_raw = self._parse_query_params(request)
        error_response = self._validate_semester_param(semester_id_raw)
        if error_response is not None:
            return error_response

        try:
            service = ProjectTrackService()
            detail = service.get_project_detail(
                request.user, project_id, institute_code, semester_id_raw
            )
            return Response(detail)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_403_FORBIDDEN)

    @extend_schema(
        tags=["showcase"],
        parameters=[_SEMESTER_PARAM, _INSTITUTE_PARAM],
        summary="Статистика распределения по трекам",
    )
    @action(detail=False, methods=["get"], url_path="statistics")
    def statistics(self, request: Request) -> Response:
        """GET /api/showcase/project-tracks/statistics/."""
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

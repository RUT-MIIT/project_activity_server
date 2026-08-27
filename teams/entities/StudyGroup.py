from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from showcase.models import Institute
from teams.dto.study_group import StudyGroupReadDTO
from teams.models import Direction, StudyGroup
from teams.services.study_group_service import StudyGroupService


class DirectionNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = ["code", "level", "name"]


class InstituteNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institute
        fields = ["code", "name"]


class StudyGroupSerializer(serializers.ModelSerializer):
    direction = DirectionNestedSerializer(read_only=True)
    institute = InstituteNestedSerializer(read_only=True)

    class Meta:
        model = StudyGroup
        fields = [
            "id",
            "name",
            "code",
            "course_number",
            "is_end",
            "profile",
            "form",
            "direction",
            "institute",
        ]


class StudyGroupListSerializer(serializers.ModelSerializer):
    """Компактная выдача для списка учебных групп."""

    direction_code = serializers.CharField(source="direction.code", read_only=True)
    students_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = StudyGroup
        fields = [
            "id",
            "name",
            "course_number",
            "direction_code",
            "students_count",
        ]


class StudyGroupViewSet(viewsets.ReadOnlyModelViewSet):
    """GET /api/teams/study-groups/ — список и просмотр учебных групп."""

    serializer_class = StudyGroupSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    @staticmethod
    def _parse_is_end_filter(value: str | None) -> bool | None:
        """Парсит query-параметр is_end; None — фильтр не применяется."""
        if value is None:
            return None
        normalized = value.lower()
        if normalized in {"true", "1"}:
            return True
        if normalized in {"false", "0"}:
            return False
        raise ValueError("Параметр is_end должен быть true или false")

    def get_queryset(self):
        service = StudyGroupService()
        return service.list_study_groups(self.request.user)

    def get_serializer_class(self):
        if getattr(self, "action", None) == "list":
            return StudyGroupListSerializer
        return super().get_serializer_class()

    def list(self, request: Request, *args, **kwargs) -> Response:
        try:
            is_end = self._parse_is_end_filter(request.query_params.get("is_end"))
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        service = StudyGroupService()
        queryset = service.list_study_groups(request.user, is_end=is_end)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        try:
            service = StudyGroupService()
            group = service.get_study_group(int(kwargs["pk"]), request.user)
            dto = StudyGroupReadDTO(group)
            return Response(dto.to_dict())
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=["get"], url_path="my")
    def my_study_group(self, request: Request) -> Response:
        """GET /api/teams/study-groups/my/ — группа текущего студента."""
        service = StudyGroupService()
        try:
            data = service.get_my_study_group(
                request.user,
                semester_id_raw=request.query_params.get("semester_id"),
            )
        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except LookupError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data)

from rest_framework import serializers, status, viewsets
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
            "direction",
            "institute",
        ]


class StudyGroupViewSet(viewsets.ReadOnlyModelViewSet):
    """GET /api/teams/study-groups/ — список и просмотр учебных групп."""

    serializer_class = StudyGroupSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        service = StudyGroupService()
        return service.list_study_groups(self.request.user)

    def list(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.get_queryset()
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

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from accounts.permissions import ProjectManagementPermission
from showcase.dto.project import ProjectListDTO
from showcase.services.project_service import ProjectService


@extend_schema_view(
    list=extend_schema(
        tags=["showcase"],
        parameters=[
            OpenApiParameter(
                name="semester_id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description="ID семестра либо actual / next",
            )
        ],
        summary="Список одобренных проектов",
    )
)
class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """GET /api/showcase/projects/ — список проектов с role-based фильтрацией."""

    permission_classes = [IsAuthenticated, ProjectManagementPermission]
    pagination_class = None
    queryset = None

    def get_queryset(self):
        from showcase.models import ProjectApplication

        return ProjectApplication.objects.none()

    def get_serializer_class(self):
        from rest_framework import serializers

        class _Empty(serializers.Serializer):
            pass

        return _Empty

    def list(self, request: Request, *args, **kwargs) -> Response:
        semester_id_raw = request.query_params.get("semester_id")

        try:
            service = ProjectService()
            queryset = service.list_projects(request.user, semester_id_raw)
            items = [ProjectListDTO(app).to_dict() for app in queryset]
            return Response(items)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from accounts.permissions import ProjectManagementPermission
from showcase.dto.project import ProjectListDTO
from showcase.services.project_service import ProjectService


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """GET /api/showcase/projects/ — список проектов с role-based фильтрацией."""

    permission_classes = [IsAuthenticated, ProjectManagementPermission]
    pagination_class = None

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

"""ViewSet дашборда проектных заявок."""

from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from accounts.permissions import ProjectTrackPermission
from showcase.services.application_dashboard_service import ApplicationDashboardService


class ApplicationDashboardViewSet(viewsets.ViewSet):
    """API дашборда проектных заявок."""

    permission_classes = [IsAuthenticated, ProjectTrackPermission]

    def retrieve(self, request: Request) -> Response:
        """GET /api/showcase/project-applications/dashboard/"""
        semester_id_raw = request.query_params.get("semester_id")
        if not semester_id_raw:
            return Response(
                {"error": "Параметр semester_id обязателен"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            service = ApplicationDashboardService()
            data = service.get_dashboard(
                user=request.user,
                semester_id_raw=semester_id_raw,
                institute_code=request.query_params.get("institute_code"),
                department_id_raw=request.query_params.get("department_id"),
                status_raw=request.query_params.get("status"),
                application_type_raw=request.query_params.get("application_type"),
                days_raw=request.query_params.get("days"),
            )
            return Response(data)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_403_FORBIDDEN)

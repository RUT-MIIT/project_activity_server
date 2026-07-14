"""ViewSet дашборда проектных заявок."""

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from accounts.permissions import ProjectTrackPermission
from showcase.services.application_dashboard_service import ApplicationDashboardService


class ApplicationDashboardViewSet(viewsets.ViewSet):
    """API дашборда проектных заявок."""

    permission_classes = [IsAuthenticated, ProjectTrackPermission]
    serializer_class = None

    def get_serializer_class(self):
        from rest_framework import serializers

        class _Empty(serializers.Serializer):
            pass

        return _Empty

    @extend_schema(
        tags=["showcase"],
        parameters=[
            OpenApiParameter(
                name="semester_id",
                type=OpenApiTypes.STR,
                required=True,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="institute_code",
                type=OpenApiTypes.STR,
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="department_id",
                type=OpenApiTypes.INT,
                required=False,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="status",
                type=OpenApiTypes.STR,
                required=False,
                location=OpenApiParameter.QUERY,
                description="approved,rejected,pending,in_progress (через запятую)",
            ),
            OpenApiParameter(
                name="application_type",
                type=OpenApiTypes.STR,
                required=False,
                location=OpenApiParameter.QUERY,
                description="all | external | internal",
            ),
            OpenApiParameter(
                name="days",
                type=OpenApiTypes.INT,
                required=False,
                location=OpenApiParameter.QUERY,
            ),
        ],
        summary="Дашборд проектных заявок",
    )
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

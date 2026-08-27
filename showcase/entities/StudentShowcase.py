"""ViewSet студенческой витрины проектов."""

from __future__ import annotations

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from showcase.services.student_showcase_service import StudentShowcaseService
from teams.permissions import StudentWithStudyGroupPermission

_SEMESTER_PARAM = OpenApiParameter(
    name="semester_id",
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    required=False,
    description="ID семестра либо actual / next (по умолчанию actual)",
)


@extend_schema_view(
    list=extend_schema(
        tags=["showcase-student"],
        parameters=[_SEMESTER_PARAM],
        summary="Витрина: треки группы с проектами",
    ),
)
class StudentShowcaseViewSet(viewsets.ViewSet):
    """Студенческая витрина: треки, детали проекта, запись команды."""

    permission_classes = [IsAuthenticated, StudentWithStudyGroupPermission]
    pagination_class = None

    def list(self, request: Request) -> Response:
        """GET /api/showcase/student-showcase/."""
        try:
            service = StudentShowcaseService()
            data = service.list_tracks(
                request.user,
                request.query_params.get("semester_id"),
            )
            response = Response(data)
            response["Cache-Control"] = "private, max-age=30"
            return response
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_403_FORBIDDEN)

    @extend_schema(
        tags=["showcase-student"],
        parameters=[_SEMESTER_PARAM],
        summary="Витрина: детали проекта",
    )
    @action(
        detail=False,
        methods=["get"],
        url_path=r"projects/(?P<project_id>\d+)",
    )
    def project_detail(self, request: Request, project_id: int) -> Response:
        """GET /api/showcase/student-showcase/projects/{id}/."""
        try:
            service = StudentShowcaseService()
            data = service.get_project(
                request.user,
                int(project_id),
                request.query_params.get("semester_id"),
            )
            response = Response(data)
            response["Cache-Control"] = "private, max-age=30"
            return response
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_403_FORBIDDEN)

    @extend_schema(
        tags=["showcase-student"],
        parameters=[_SEMESTER_PARAM],
        summary="Витрина: записать команду на проект",
    )
    @action(
        detail=False,
        methods=["post"],
        url_path=r"projects/(?P<project_id>\d+)/enroll",
    )
    def enroll(self, request: Request, project_id: int) -> Response:
        """POST /api/showcase/student-showcase/projects/{id}/enroll/."""
        try:
            service = StudentShowcaseService()
            data = service.enroll(
                request.user,
                int(project_id),
                request.query_params.get("semester_id"),
            )
            return Response(data)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_403_FORBIDDEN)

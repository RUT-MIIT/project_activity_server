"""ViewSet для управления пользователями."""

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from accounts.dto.user_list import UserListDTO
from accounts.permissions import UserManagementPermission
from accounts.serializers import UserUpdateSerializer
from accounts.services.user_management_service import UserManagementService

_INCLUDE_PROJECTS = OpenApiParameter(
    name="include_authored_projects",
    type=OpenApiTypes.STR,
    location=OpenApiParameter.QUERY,
    required=False,
    description="true / 1 / yes — добавить authored_projects[]",
)


@extend_schema_view(
    list=extend_schema(
        tags=["accounts"],
        parameters=[_INCLUDE_PROJECTS],
        summary="Список пользователей",
    ),
    retrieve=extend_schema(
        tags=["accounts"],
        parameters=[_INCLUDE_PROJECTS],
        summary="Детали пользователя",
    ),
    partial_update=extend_schema(
        tags=["accounts"],
        request=UserUpdateSerializer,
        summary="Обновить пользователя",
    ),
)
class UserManagementViewSet(viewsets.ViewSet):
    """API управления пользователями: список, деталь, частичное обновление."""

    permission_classes = [IsAuthenticated, UserManagementPermission]
    pagination_class = None
    serializer_class = UserUpdateSerializer

    @staticmethod
    def _parse_include_authored_projects(request: Request) -> bool:
        """Проверяет query-параметр include_authored_projects."""
        raw = request.query_params.get("include_authored_projects", "").lower()
        return raw in {"1", "true", "yes"}

    def list(self, request: Request) -> Response:
        """GET /api/accounts/users/ — список пользователей."""
        include_projects = self._parse_include_authored_projects(request)
        try:
            service = UserManagementService()
            queryset = service.list_users(
                request.user,
                include_authored_projects=include_projects,
            )
            items = [
                UserListDTO(user, include_authored_projects=include_projects).to_dict()
                for user in queryset
            ]
            return Response(items)
        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request: Request, pk: str | None = None) -> Response:
        """GET /api/accounts/users/{id}/ — деталь пользователя."""
        include_projects = self._parse_include_authored_projects(request)
        try:
            service = UserManagementService()
            user = service.get_user(
                request.user,
                int(pk),
                include_authored_projects=include_projects,
            )
            data = UserListDTO(
                user, include_authored_projects=include_projects
            ).to_dict()
            return Response(data)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request: Request, pk: str | None = None) -> Response:
        """PATCH /api/accounts/users/{id}/ — частичное обновление."""
        serializer = UserUpdateSerializer(
            data=request.data,
            partial=True,
            context={"user_id": int(pk)},
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        fields_set = set(serializer.validated_data.keys())
        if "department" in fields_set:
            fields_set.add("department_id")
            fields_set.discard("department")

        try:
            service = UserManagementService()
            department = serializer.validated_data.get("department")
            role_obj = serializer.validated_data.get("role")
            role_code = role_obj.code if role_obj is not None else None
            user = service.update_user(
                request.user,
                int(pk),
                role_code=role_code,
                department_id=department.id if department else None,
                email=serializer.validated_data.get("email"),
                phone=serializer.validated_data.get("phone"),
                fields_set=fields_set,
            )
            refreshed = service.get_user(request.user, user.id)
            return Response(UserListDTO(refreshed).to_dict())
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

from rest_framework import serializers, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from teams.dto.direction import DirectionReadDTO
from teams.models import Direction
from teams.services.direction_service import DirectionService


class DirectionSerializer(serializers.ModelSerializer):
    """Сериализатор направления подготовки."""

    class Meta:
        model = Direction
        fields = ["code", "level", "name"]


class DirectionViewSet(viewsets.ReadOnlyModelViewSet):
    """GET /api/teams/directions/ — список и просмотр направлений."""

    serializer_class = DirectionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    lookup_field = "code"
    lookup_url_kwarg = "code"
    lookup_value_regex = r"[^/]+"

    def get_queryset(self):
        service = DirectionService()
        return service.list_directions(self.request.user)

    def list(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        try:
            service = DirectionService()
            direction = service.get_direction(kwargs["code"], request.user)
            dto = DirectionReadDTO(direction)
            return Response(dto.to_dict())
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

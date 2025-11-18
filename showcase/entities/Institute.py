from rest_framework import serializers, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from showcase.models import Institute


class InstituteSerializer(serializers.ModelSerializer):
    """Сериализатор для институтов/академий."""

    class Meta:
        model = Institute
        fields = [
            "code",
            "name",
        ]


class InstituteViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet только для чтения институтов/академий.
    Доступен для всех пользователей.
    Без пагинации - возвращает все активные институты.
    """

    queryset = Institute.objects.filter(is_active=True)
    serializer_class = InstituteSerializer
    permission_classes = [AllowAny]
    lookup_field = "code"
    pagination_class = None  # Отключаем пагинацию

    def list(self, request, *args, **kwargs):
        """Переопределяем list для возврата всех институтов без пагинации."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

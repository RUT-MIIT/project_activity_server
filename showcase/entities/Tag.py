from rest_framework import serializers, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from showcase.models import Tag


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов."""

    class Meta:
        model = Tag
        fields = [
            "id",
            "name",
            "category",
        ]


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet только для чтения тегов.
    Доступен для всех пользователей.
    Без пагинации - возвращает все теги, отсортированные по категории и названию.
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    pagination_class = None  # Отключаем пагинацию

    def list(self, request, *args, **kwargs):
        """Переопределяем list для возврата всех тегов без пагинации."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

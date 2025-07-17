from rest_framework import serializers, viewsets, permissions
from showcase.models import ApplicationStatus


class ApplicationStatusReadSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения (чтения) статусов заявок на проекты.
    Используется для GET-запросов.
    """
    class Meta:
        model = ApplicationStatus
        fields = [
            'code',
            'name',
        ]


class ApplicationStatusViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet только для чтения статусов заявок на проекты.
    Доступен только для аутентифицированных пользователей.
    """
    queryset = ApplicationStatus.objects.all()
    serializer_class = ApplicationStatusReadSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'code'

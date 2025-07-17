from rest_framework import serializers, viewsets, permissions
from showcase.models import (
    ProjectApplication, ApplicationStatus, ProjectApplicationStatusLog
)
from accounts.serializers import UserShortSerializer
from showcase.entities.ApplicationStatus import ApplicationStatusReadSerializer


class ProjectApplicationCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и обновления заявок на проекты.
    Используется для POST, PUT, PATCH-запросов.
    """
    id = serializers.IntegerField(read_only=True)
    status = ApplicationStatusReadSerializer(read_only=True)
    author = UserShortSerializer(read_only=True)
    creation_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = ProjectApplication
        fields = [
            'id',
            'title',
            'description',
            'company',
            'status',
            'author',
            'creation_date',
        ]
        read_only_fields = ['id', 'author', 'creation_date']


class ProjectApplicationReadSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения (чтения) заявок на проекты.
    Используется для GET-запросов,
    включает объект пользователя
    и статус.
    """
    author = UserShortSerializer(read_only=True)
    status = ApplicationStatusReadSerializer(read_only=True)
    author = UserShortSerializer(read_only=True)

    class Meta:
        model = ProjectApplication
        fields = [
            'id',
            'title',
            'description',
            'company',
            'creation_date',
            'status',
            'author',
        ]


class ProjectApplicationViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления заявками на проекты.
    Автоматически выбирает нужный сериализатор в зависимости от действия.
    Только для аутентифицированных пользователей.
    """
    queryset = (
        ProjectApplication.objects.select_related('author')
        .select_related('status')
    )
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProjectApplicationCreateUpdateSerializer
        return ProjectApplicationReadSerializer

    def perform_create(self, serializer):
        # Найти статус "Создана"
        try:
            created_status = ApplicationStatus.objects.get(name="Создана")
        except ApplicationStatus.DoesNotExist:
            raise serializers.ValidationError({"status": "Статус 'Создана' не найден"})
        # Сохраняем заявку с нужным статусом и автором
        application = serializer.save(author=self.request.user, status=created_status)
        # Создаём лог
        ProjectApplicationStatusLog.objects.create(
            application=application,
            actor=self.request.user,
            from_status=None,
            to_status=created_status,
            previous_status_log=None,
        )

from rest_framework import decorators, serializers, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from accounts.permissions import TagManagePermission
from showcase.dto.tag import TagCreateDTO, TagReadDTO, TagUpdateDTO
from showcase.models import Tag
from showcase.services.tag_service import TagService


class DepartmentNestedSerializer(serializers.Serializer):
    """Вложенный сериализатор для подразделения."""

    id = serializers.IntegerField()
    name = serializers.CharField()
    short_name = serializers.CharField()


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов."""

    class Meta:
        model = Tag
        fields = [
            "id",
            "name",
            "category",
            "is_base",
        ]


class TagCreateSerializer(serializers.Serializer):
    """Сериализатор для создания тега."""

    name = serializers.CharField(max_length=255, required=True)
    category = serializers.CharField(max_length=255, required=True, allow_blank=True)
    department_id = serializers.IntegerField(required=False, allow_null=True)

    def create(self, validated_data):
        """Преобразование в DTO."""
        return TagCreateDTO.from_dict(validated_data)


class TagUpdateSerializer(serializers.Serializer):
    """Сериализатор для обновления тега."""

    name = serializers.CharField(max_length=255, required=False)
    category = serializers.CharField(max_length=255, required=False, allow_blank=True)
    department_id = serializers.IntegerField(required=False, allow_null=True)

    def create(self, validated_data):
        """Преобразование в DTO."""
        return TagUpdateDTO.from_dict(validated_data)


class DepartmentAttachDetachSerializer(serializers.Serializer):
    """Сериализатор для присоединения/отцепления подразделения."""

    department_id = serializers.IntegerField(required=True)


class TagViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с тегами.

    CRUD операции доступны для ролей cpds, admin, institute_validator.
    Список и просмотр доступны всем с фильтрацией по ролям.
    Без пагинации - возвращает все доступные теги.
    """

    serializer_class = TagSerializer
    permission_classes = [AllowAny]  # Базовый доступ для всех
    pagination_class = None  # Отключаем пагинацию

    def get_permissions(self):
        """Возвращает список разрешений в зависимости от действия."""
        if self.action in [
            "create",
            "update",
            "partial_update",
            "destroy",
            "attach_department",
            "detach_department",
        ]:
            return [TagManagePermission()]
        return [AllowAny()]

    def get_queryset(self):
        """Возвращает queryset с фильтрацией по ролям."""
        service = TagService()
        return service.list_tags(self.request.user)

    def list(self, request: Request, *args, **kwargs) -> Response:
        """GET /api/showcase/tags/ - список тегов с фильтрацией по ролям."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        """GET /api/showcase/tags/{id}/ - получение тега с проверкой доступа."""
        try:
            service = TagService()
            tag = service.get_tag(int(kwargs["pk"]), request.user)
            dto = TagReadDTO(tag)
            return Response(dto.to_dict())
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

    def create(self, request: Request, *args, **kwargs) -> Response:
        """POST /api/showcase/tags/ - создание тега."""
        serializer = TagCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            service = TagService()
            dto = serializer.save()
            tag = service.create_tag(dto, request.user)
            read_dto = TagReadDTO(tag)
            return Response(read_dto.to_dict(), status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request: Request, *args, **kwargs) -> Response:
        """PUT /api/showcase/tags/{id}/ - полное обновление тега."""
        return self._update(request, *args, **kwargs)

    def partial_update(self, request: Request, *args, **kwargs) -> Response:
        """PATCH /api/showcase/tags/{id}/ - частичное обновление тега."""
        kwargs["partial"] = True
        return self._update(request, *args, **kwargs)

    def _update(
        self, request: Request, *args, partial: bool = False, **kwargs
    ) -> Response:
        """Внутренний метод для обновления тега."""
        serializer = TagUpdateSerializer(data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        try:
            service = TagService()
            dto = serializer.save()
            tag = service.update_tag(int(kwargs["pk"]), dto, request.user)
            read_dto = TagReadDTO(tag)
            return Response(read_dto.to_dict())
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        """DELETE /api/showcase/tags/{id}/ - удаление тега."""
        try:
            service = TagService()
            service.delete_tag(int(kwargs["pk"]), request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @decorators.action(
        detail=True,
        methods=["post"],
        url_path="attach-department",
        url_name="attach-department",
    )
    def attach_department(self, request: Request, pk: int = None) -> Response:
        """POST /api/showcase/tags/{id}/attach-department/ - присоединение подразделения к тегу."""
        serializer = DepartmentAttachDetachSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            service = TagService()
            tag = service.attach_department(
                int(pk), serializer.validated_data["department_id"], request.user
            )
            read_dto = TagReadDTO(tag)
            return Response(read_dto.to_dict())
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @decorators.action(
        detail=True,
        methods=["post"],
        url_path="detach-department",
        url_name="detach-department",
    )
    def detach_department(self, request: Request, pk: int = None) -> Response:
        """POST /api/showcase/tags/{id}/detach-department/ - отцепление подразделения от тега."""
        serializer = DepartmentAttachDetachSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            service = TagService()
            department_id = serializer.validated_data["department_id"]
            tag = service.detach_department(int(pk), department_id, request.user)

            # Если тег был удален (не базовый и не осталось подразделений)
            if tag is None:
                return Response(
                    {
                        "message": "Подразделение отцеплено, тег удален, так как не является базовым и не имеет подразделений",
                        "department_id": department_id,
                    },
                    status=status.HTTP_200_OK,
                )

            return Response(
                {
                    "message": "Подразделение успешно отцеплено от тега",
                    "department_id": department_id,
                },
                status=status.HTTP_200_OK,
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

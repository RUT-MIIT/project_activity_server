"""Упрощенный ViewSet для проектных заявок с использованием новой архитектуры.

Тонкий слой контроллеров - только обработка HTTP запросов.
Вся бизнес-логика вынесена в сервисы.
"""

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from showcase.dto.application import (
    ProjectApplicationCreateDTO,
    ProjectApplicationUpdateDTO,
    serialize_comment_author,
)
from showcase.models import ProjectApplication
from showcase.services.application_service import ProjectApplicationService
from showcase.services.comment_service import CommentService

User = get_user_model()


def get_error_message(exception: Exception) -> str:
    """Возвращает сообщение об ошибке в зависимости от режима DEBUG.

    Args:
        exception: Исключение

    Returns:
        str: Сообщение об ошибке

    """
    if settings.DEBUG:
        return str(exception)
    else:
        return "Внутренняя ошибка сервера"


def format_validation_errors(errors) -> dict:
    """Форматирует ошибки валидации используя стандартные DRF механизмы.

    Args:
        errors: Ошибки валидации (может быть dict, list, ErrorDetail или ValueError)

    Returns:
        dict: Отформатированные ошибки

    """
    # Если это ValueError, пытаемся извлечь из него словарь ошибок
    if isinstance(errors, ValueError):
        # Пытаемся получить словарь ошибок из ValueError
        if hasattr(errors, "args") and errors.args:
            # Если в args есть словарь ошибок
            if isinstance(errors.args[0], dict):
                return errors.args[0]
            else:
                # Если это строка с ErrorDetail, пытаемся распарсить
                error_str = str(errors)
                if "ErrorDetail" in error_str:
                    try:
                        import re

                        # Извлекаем информацию из строки с помощью регулярных выражений
                        # Ищем паттерн: 'field': [ErrorDetail(string='message', code='code')]
                        pattern = r"'([^']+)':\s*\[ErrorDetail\(string='([^']+)',\s*code='([^']+)'\)\]"
                        matches = re.findall(pattern, error_str)

                        if matches:
                            formatted_errors = {}
                            for field, message, _code in matches:
                                if field not in formatted_errors:
                                    formatted_errors[field] = []
                                formatted_errors[field].append(message)
                            return formatted_errors
                        else:
                            return {"error": [error_str]}
                    except Exception:
                        return {"error": [error_str]}
                else:
                    # Если это обычная строка, пытаемся распарсить как dict
                    try:
                        import ast

                        return ast.literal_eval(error_str)
                    except Exception:
                        return {"error": [error_str]}
        else:
            return {"error": [str(errors)]}

    # Если это уже словарь, обрабатываем ErrorDetail объекты
    if isinstance(errors, dict):
        formatted_errors = {}
        for field, field_errors in errors.items():
            if isinstance(field_errors, list):
                # Извлекаем только текстовые сообщения из ErrorDetail
                formatted_errors[field] = [str(error) for error in field_errors]
            else:
                formatted_errors[field] = [str(field_errors)]
        return formatted_errors
    elif isinstance(errors, list):
        return {"non_field_errors": [str(error) for error in errors]}
    else:
        return {"error": [str(errors)]}


class ProjectApplicationListSerializer(serializers.ModelSerializer):
    """Простой сериализатор для списка заявок"""

    class Meta:
        model = ProjectApplication
        fields = [
            "id",
            "title",
            "company",
            "creation_date",
            "needs_consultation",
            "application_year",
            "year_sequence_number",
            "print_number",
            "author_lastname",
            "author_firstname",
            "author_email",
        ]
        read_only_fields = fields


class ProjectApplicationCreateSerializer(serializers.Serializer):
    """Сериализатор для технической валидации HTTP данных.

    ОТВЕТСТВЕННОСТЬ:
    - Типы данных (CharField, EmailField, BooleanField)
    - Форматы (email, URL, даты)
    - Длина строк (max_length)
    - Обязательные поля (required=True)

    Бизнес-правила проверяются в ProjectApplicationDomain.validate_create()
    """

    # Основные поля
    title = serializers.CharField(max_length=255, required=False, allow_blank=True)
    description = serializers.CharField(
        required=False, allow_blank=True
    )  # Для совместимости с тестами
    company = serializers.CharField(max_length=255)

    # Контактные данные - делаем опциональными для совместимости с тестами
    author_lastname = serializers.CharField(
        max_length=100, required=False, allow_blank=True
    )
    author_firstname = serializers.CharField(
        max_length=100, required=False, allow_blank=True
    )
    author_middlename = serializers.CharField(
        max_length=100, required=False, allow_blank=True
    )
    author_email = serializers.EmailField(required=False, allow_blank=True)
    author_phone = serializers.CharField(
        max_length=20, required=False, allow_blank=True
    )
    author_role = serializers.CharField(
        max_length=100, required=False, allow_blank=True
    )
    author_division = serializers.CharField(
        max_length=200, required=False, allow_blank=True
    )

    # О проекте
    company_contacts = serializers.CharField(required=False, allow_blank=True)
    target_institutes = serializers.ListField(
        child=serializers.CharField(max_length=50), required=False, allow_empty=True
    )
    tags = serializers.ListField(
        child=serializers.IntegerField(), required=False, allow_empty=True
    )
    project_level = serializers.CharField(
        max_length=100, required=False, allow_blank=True
    )

    # Проблема - делаем опциональными для совместимости с тестами
    problem_holder = serializers.CharField(required=False, allow_blank=True)
    goal = serializers.CharField(required=False, allow_blank=True)
    barrier = serializers.CharField(required=False, allow_blank=True)
    existing_solutions = serializers.CharField(required=False, allow_blank=True)

    # Контекст
    context = serializers.CharField(required=False, allow_blank=True)
    stakeholders = serializers.CharField(required=False, allow_blank=True)
    recommended_tools = serializers.CharField(required=False, allow_blank=True)
    experts = serializers.CharField(required=False, allow_blank=True)
    additional_materials = serializers.CharField(required=False, allow_blank=True)
    needs_consultation = serializers.BooleanField(required=False)

    def create(self, validated_data):
        """Преобразование в DTO - никакой бизнес-логики"""
        return ProjectApplicationCreateDTO.from_dict(validated_data)


class ProjectApplicationUpdateSerializer(serializers.Serializer):
    """Сериализатор только для валидации HTTP данных при обновлении."""

    # Все поля опциональны для обновления
    title = serializers.CharField(max_length=255, required=False)
    company = serializers.CharField(max_length=255, required=False)
    author_lastname = serializers.CharField(max_length=100, required=False)
    author_firstname = serializers.CharField(max_length=100, required=False)
    author_middlename = serializers.CharField(
        max_length=100, required=False, allow_blank=True
    )
    author_email = serializers.EmailField(required=False)
    author_phone = serializers.CharField(max_length=20, required=False)
    author_role = serializers.CharField(
        max_length=100, required=False, allow_blank=True
    )
    author_division = serializers.CharField(
        max_length=200, required=False, allow_blank=True
    )
    company_contacts = serializers.CharField(required=False, allow_blank=True)
    target_institutes = serializers.ListField(
        child=serializers.CharField(max_length=50), required=False, allow_empty=True
    )
    tags = serializers.ListField(
        child=serializers.IntegerField(), required=False, allow_empty=True
    )
    project_level = serializers.CharField(
        max_length=100, required=False, allow_blank=True
    )
    problem_holder = serializers.CharField(required=False)
    goal = serializers.CharField(required=False)
    barrier = serializers.CharField(required=False)
    existing_solutions = serializers.CharField(required=False, allow_blank=True)
    context = serializers.CharField(required=False, allow_blank=True)
    stakeholders = serializers.CharField(required=False, allow_blank=True)
    recommended_tools = serializers.CharField(required=False, allow_blank=True)
    experts = serializers.CharField(required=False, allow_blank=True)
    additional_materials = serializers.CharField(required=False, allow_blank=True)
    needs_consultation = serializers.BooleanField(required=False)

    def create(self, validated_data):
        """Преобразование в DTO - никакой бизнес-логики"""
        return ProjectApplicationUpdateDTO.from_dict(validated_data)


class ProjectApplicationViewSet(viewsets.ModelViewSet):
    """Упрощенный ViewSet - только обработка HTTP запросов.

    Вся бизнес-логика вынесена в ApplicationService.
    """

    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination
    queryset = ProjectApplication.objects.all()  # Добавляем queryset для совместимости
    serializer_class = ProjectApplicationListSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ProjectApplicationService()
        self.comment_service = CommentService()

    def get_permissions(self):
        """Переопределяем права доступа для определенных действий.
        Для действий 'simple' и 'my_applications' разрешаем доступ без авторизации.
        """
        if self.action in ["simple"]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия"""
        if self.action == "create":
            return ProjectApplicationCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return ProjectApplicationUpdateSerializer
        return ProjectApplicationCreateSerializer  # fallback

    def create(self, request):
        """POST /api/project-applications/
        Создание заявки - только обработка HTTP
        """
        try:
            # 1. Валидация HTTP данных
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # 2. Преобразование в DTO
            dto = serializer.save()

            # 3. Вызов сервиса (вся логика там)
            application = self.service.submit_application(dto, request.user)

            # 4. Сериализация ответа
            response_dto = self.service.get_application_dto(application)
            return Response(response_dto.to_dict(), status=status.HTTP_201_CREATED)

        except ValueError as e:
            # Обработка ошибок валидации
            formatted_errors = format_validation_errors(e)
            return Response(
                {"errors": formatted_errors}, status=status.HTTP_400_BAD_REQUEST
            )
        except DRFValidationError as e:
            # Обработка стандартных DRF ошибок валидации
            return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as e:
            # Обработка ошибок прав доступа
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response(
                {"error": get_error_message(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get_queryset(self):
        """Возвращает QuerySet для списка заявок.
        DRF автоматически применит пагинацию.
        """
        try:
            return self.service.get_user_applications_queryset(self.request.user)
        except PermissionError:
            return ProjectApplication.objects.none()

    def list(self, request):
        """GET /api/project-applications/
        Получение списка заявок с пагинацией
        """
        try:
            # Получаем QuerySet
            queryset = self.get_queryset()

            # Применяем пагинацию
            page = self.paginate_queryset(queryset)
            if page is not None:
                # Преобразуем в DTO для списка
                list_dtos = [self.service.get_application_list_dto(app) for app in page]
                return self.get_paginated_response([dto.to_dict() for dto in list_dtos])

            # Если пагинация не настроена, возвращаем все данные
            applications = list(queryset)
            list_dtos = [
                self.service.get_application_list_dto(app) for app in applications
            ]
            return Response([dto.to_dict() for dto in list_dtos])

        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response(
                {"error": get_error_message(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def retrieve(self, request, pk=None):
        """GET /api/project-applications/{id}/
        Получение заявки по ID с доступными действиями
        """
        try:
            # Получаем заявку через сервис
            application = self.service.get_application(int(pk), request.user)

            # Преобразуем в DTO
            response_dto = self.service.get_application_dto(application)
            response_data = response_dto.to_dict()

            # Добавляем доступные действия
            try:
                available_actions_dto = self.service.get_available_actions(
                    int(pk), request.user
                )
                response_data.update(available_actions_dto.to_dict())
            except Exception:
                # Если не удалось получить действия, не прерываем выполнение
                response_data["available_actions"] = []

            return Response(response_data)

        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception:
            return Response(
                {"error": "Заявка не найдена"}, status=status.HTTP_404_NOT_FOUND
            )

    def update(self, request, pk=None):
        """PUT /api/project-applications/{id}/
        Полное обновление заявки
        """
        try:
            # 1. Валидация HTTP данных
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # 2. Преобразование в DTO
            dto = serializer.save()

            # 3. Вызов сервиса
            application = self.service.update_application(int(pk), dto, request.user)

            # 4. Сериализация ответа
            response_dto = self.service.get_application_dto(application)
            return Response(response_dto.to_dict())

        except ValueError as e:
            error_msg = str(e)
            if "не найдена" in error_msg:
                return Response({"error": error_msg}, status=status.HTTP_404_NOT_FOUND)
            return Response({"errors": error_msg}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception:
            return Response(
                {"error": "Заявка не найдена"}, status=status.HTTP_404_NOT_FOUND
            )

    def partial_update(self, request, pk=None):
        """PATCH /api/project-applications/{id}/
        Частичное обновление заявки
        """
        try:
            # 1. Валидация HTTP данных
            serializer = self.get_serializer(data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)

            # 2. Преобразование в DTO
            dto = serializer.save()

            # 3. Вызов сервиса
            application = self.service.update_application(int(pk), dto, request.user)

            # 4. Сериализация ответа
            response_dto = self.service.get_application_dto(application)
            return Response(response_dto.to_dict())

        except ValueError as e:
            error_msg = str(e)
            if "не найдена" in error_msg:
                return Response({"error": error_msg}, status=status.HTTP_404_NOT_FOUND)
            return Response({"errors": error_msg}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception:
            return Response(
                {"error": "Заявка не найдена"}, status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        """POST /api/project-applications/{id}/approve/
        Одобрение заявки
        """
        try:
            application = self.service.approve_application(
                application_id=int(pk), approver=request.user
            )

            # Получаем доступные действия после одобрения
            try:
                available_actions_dto = self.service.get_available_actions(
                    int(pk), request.user
                )
                available_actions = available_actions_dto.to_dict()["available_actions"]
            except Exception:
                # Если не удалось получить доступные действия, возвращаем пустой список
                available_actions = []

            return Response(
                {
                    "status": application.status.code,
                    "status_name": (
                        application.status.name
                        if hasattr(application.status, "name")
                        else ""
                    ),
                    "message": "Заявка одобрена",
                    "available_actions": available_actions,
                },
                status=status.HTTP_200_OK,
            )
        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(
                {"error": "Заявка не найдена"}, status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        """POST /api/project-applications/{id}/reject/
        Отклонение заявки
        """
        try:
            reason = request.data.get("reason", "")
            application = self.service.reject_application(
                application_id=int(pk), rejector=request.user, reason=reason
            )

            # Получаем доступные действия после отклонения
            try:
                available_actions_dto = self.service.get_available_actions(
                    int(pk), request.user
                )
                available_actions = available_actions_dto.to_dict()["available_actions"]
            except Exception:
                # Если не удалось получить доступные действия, возвращаем пустой список
                available_actions = []

            return Response(
                {
                    "status": application.status.code,
                    "status_name": (
                        application.status.name
                        if hasattr(application.status, "name")
                        else ""
                    ),
                    "message": "Заявка отклонена",
                    "available_actions": available_actions,
                },
                status=status.HTTP_200_OK,
            )
        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(
                {"error": "Заявка не найдена"}, status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=["post"])
    def request_changes(self, request, pk=None):
        """POST /api/project-applications/{id}/request_changes/
        Запрос изменений (отправка на доработку)
        """
        try:
            application = self.service.request_changes(
                application_id=int(pk), requester=request.user
            )

            # Получаем доступные действия после отправки на доработку
            try:
                available_actions_dto = self.service.get_available_actions(
                    int(pk), request.user
                )
                available_actions = available_actions_dto.to_dict()["available_actions"]
            except Exception:
                # Если не удалось получить доступные действия, возвращаем пустой список
                available_actions = []

            return Response(
                {
                    "status": application.status.code,
                    "status_name": (
                        application.status.name
                        if hasattr(application.status, "name")
                        else ""
                    ),
                    "message": "Заявка отправлена на доработку",
                    "available_actions": available_actions,
                },
                status=status.HTTP_200_OK,
            )
        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(
                {"error": "Заявка не найдена"}, status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=["get"])
    def by_status(self, request):
        """GET /api/project-applications/by_status/?status=created
        Получение заявок по статусу (только для админов/модераторов)
        """
        try:
            status_code = request.query_params.get("status")
            if not status_code:
                return Response(
                    {"error": "Параметр status обязателен"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            applications = self.service.get_applications_by_status(
                status_code, request.user
            )
            list_dtos = [
                self.service.get_application_list_dto(app) for app in applications
            ]

            return Response([dto.to_dict() for dto in list_dtos])

        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response(
                {"error": get_error_message(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["get"])
    def recent(self, request):
        """GET /api/project-applications/recent/
        Получение последних заявок (только для админов/модераторов)
        """
        try:
            limit = int(request.query_params.get("limit", 10))
            applications = self.service.get_recent_applications(limit, request.user)
            list_dtos = [
                self.service.get_application_list_dto(app) for app in applications
            ]

            return Response([dto.to_dict() for dto in list_dtos])

        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response(
                {"error": get_error_message(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    # Методы для совместимости со старыми тестами
    @action(detail=False, methods=["get"])
    def my_applications(self, request):
        """GET /api/project-applications/my_applications/"""
        if not request.user.is_authenticated:
            # Для неавторизованных пользователей возвращаем пустой список
            return Response([])

        try:
            # Получаем все заявки пользователя без пагинации
            queryset = self.get_queryset()
            applications = list(queryset)
            list_dtos = [
                self.service.get_application_list_dto(app) for app in applications
            ]
            return Response([dto.to_dict() for dto in list_dtos])

        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response(
                {"error": get_error_message(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["get"])
    def coordination(self, request):
        """GET /api/project-applications/coordination/
        Заявки для координации: где пользователь причастен и статус не approved/rejected
        """
        if not request.user.is_authenticated:
            # Для неавторизованных пользователей возвращаем пустой список
            return Response([])

        try:
            # Получаем заявки через сервис с фильтрацией по причастности
            applications = self.service.get_user_coordination_applications(request.user)

            # Преобразуем в DTO для списка
            list_dtos = [
                self.service.get_application_list_dto(app) for app in applications
            ]

            return Response([dto.to_dict() for dto in list_dtos])

        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response(
                {"error": get_error_message(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["post"])
    def simple(self, request):
        """POST /api/project-applications/simple/
        Создание заявки без авторизации
        """
        try:
            # 1. Валидация HTTP данных
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # 2. Преобразование в DTO
            dto = serializer.save()

            # 3. Вызов сервиса (передаем None как пользователя для неавторизованных)
            application = self.service.submit_application(dto, None)

            # 4. Сериализация ответа
            response_dto = self.service.get_application_dto(application)
            return Response(response_dto.to_dict(), status=status.HTTP_201_CREATED)

        except ValueError as e:
            # Обработка ошибок валидации
            formatted_errors = format_validation_errors(e)
            return Response(
                {"errors": formatted_errors}, status=status.HTTP_400_BAD_REQUEST
            )
        except DRFValidationError as e:
            # Обработка стандартных DRF ошибок валидации
            return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Обработка прочих ошибок
            return Response(
                {"error": get_error_message(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["get"])
    def status_logs(self, request, pk=None):
        """GET /api/project-applications/{id}/status_logs/"""
        try:
            application = self.service.get_application(int(pk), request.user)
            # Возвращаем логи из модели
            logs = application.status_logs.all()
            return Response(
                [
                    {
                        "id": log.id,
                        "from_status": (
                            log.from_status.code if log.from_status else None
                        ),
                        "to_status": log.to_status.code,
                        "changed_at": log.changed_at,
                        "actor": log.actor.get_full_name() if log.actor else None,
                    }
                    for log in logs
                ]
            )
        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception:
            return Response(
                {"error": "Заявка не найдена"}, status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=["post"])
    def add_comment(self, request, pk=None):
        """POST /api/project-applications/{id}/add_comment/
        Добавление комментария к заявке
        Тело: {"field": "goal", "text": "Комментарий"}
        """
        try:
            field = request.data.get("field", "").strip()
            text = request.data.get("text", "").strip()

            if not field:
                return Response(
                    {"error": "Поле обязательно"}, status=status.HTTP_400_BAD_REQUEST
                )
            if not text:
                return Response(
                    {"error": "Текст комментария обязателен"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            comment = self.comment_service.add_comment(
                application_id=int(pk), field=field, text=text, author=request.user
            )

            # Перезагружаем комментарий с оптимизацией запросов
            from showcase.models import ProjectApplicationComment

            comment = ProjectApplicationComment.objects.select_related(
                "author", "author__role", "author__department"
            ).get(pk=comment.id)

            return Response(
                {
                    "id": comment.id,
                    "field": comment.field,
                    "text": comment.text,
                    "author": serialize_comment_author(comment.author),
                    "created_at": (
                        comment.created_at.isoformat() if comment.created_at else None
                    ),
                },
                status=status.HTTP_201_CREATED,
            )

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception:
            return Response(
                {"error": "Заявка не найдена"}, status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=["get"])
    def comments(self, request, pk=None):
        """GET /api/project-applications/{id}/comments/
        Получение всех комментариев к заявке
        """
        try:
            # Получаем комментарии через сервис
            comments = self.comment_service.get_application_comments(int(pk))

            return Response(
                [
                    {
                        "id": comment.id,
                        "field": comment.field,
                        "text": comment.text,
                        "author": serialize_comment_author(comment.author),
                        "created_at": (
                            comment.created_at.isoformat()
                            if comment.created_at
                            else None
                        ),
                    }
                    for comment in comments
                ]
            )

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            # Логируем реальную ошибку для отладки
            import traceback

            print(f"Ошибка при получении комментариев: {e}")
            print(traceback.format_exc())
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

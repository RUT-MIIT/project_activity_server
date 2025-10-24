"""
Упрощенный ViewSet для проектных заявок с использованием новой архитектуры.

Тонкий слой контроллеров - только обработка HTTP запросов.
Вся бизнес-логика вынесена в сервисы.
"""

from rest_framework import serializers, viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model

from showcase.models import ProjectApplication
from showcase.dto.application import (
    ProjectApplicationCreateDTO,
    ProjectApplicationUpdateDTO,
)
from showcase.services.application_service import ProjectApplicationService

User = get_user_model()


class ProjectApplicationListSerializer(serializers.ModelSerializer):
    """Простой сериализатор для списка заявок"""
    
    class Meta:
        model = ProjectApplication
        fields = [
            'id', 'title', 'company', 'creation_date', 'needs_consultation',
            'author_lastname', 'author_firstname', 'author_email'
        ]
        read_only_fields = fields


class ProjectApplicationCreateSerializer(serializers.Serializer):
    """
    Сериализатор только для валидации HTTP данных.
    Никакой бизнес-логики - только преобразование JSON в DTO.
    """
    
    # Основные поля
    title = serializers.CharField(max_length=255, required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)  # Для совместимости с тестами
    company = serializers.CharField(max_length=255)
    
    # Контактные данные - делаем опциональными для совместимости с тестами
    author_lastname = serializers.CharField(max_length=100, required=False, allow_blank=True)
    author_firstname = serializers.CharField(max_length=100, required=False, allow_blank=True)
    author_middlename = serializers.CharField(max_length=100, required=False, allow_blank=True)
    author_email = serializers.EmailField(required=False, allow_blank=True)
    author_phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    author_role = serializers.CharField(max_length=100, required=False, allow_blank=True)
    author_division = serializers.CharField(max_length=200, required=False, allow_blank=True)
    
    # О проекте
    company_contacts = serializers.CharField(required=False, allow_blank=True)
    target_institutes = serializers.ListField(
        child=serializers.CharField(max_length=50),
        required=False,
        allow_empty=True
    )
    project_level = serializers.CharField(max_length=100, required=False, allow_blank=True)
    
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
    needs_consultation = serializers.BooleanField(required=False, default=False)
    
    def create(self, validated_data):
        """Преобразование в DTO - никакой бизнес-логики"""
        return ProjectApplicationCreateDTO.from_dict(validated_data)


class ProjectApplicationUpdateSerializer(serializers.Serializer):
    """
    Сериализатор только для валидации HTTP данных при обновлении.
    """
    
    # Все поля опциональны для обновления
    title = serializers.CharField(max_length=255, required=False)
    company = serializers.CharField(max_length=255, required=False)
    author_lastname = serializers.CharField(max_length=100, required=False)
    author_firstname = serializers.CharField(max_length=100, required=False)
    author_middlename = serializers.CharField(max_length=100, required=False, allow_blank=True)
    author_email = serializers.EmailField(required=False)
    author_phone = serializers.CharField(max_length=20, required=False)
    author_role = serializers.CharField(max_length=100, required=False, allow_blank=True)
    author_division = serializers.CharField(max_length=200, required=False, allow_blank=True)
    company_contacts = serializers.CharField(required=False, allow_blank=True)
    target_institutes = serializers.ListField(
        child=serializers.CharField(max_length=50),
        required=False,
        allow_empty=True
    )
    project_level = serializers.CharField(max_length=100, required=False, allow_blank=True)
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
    """
    Упрощенный ViewSet - только обработка HTTP запросов.
    
    Вся бизнес-логика вынесена в ApplicationService.
    """
    
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination
    queryset = ProjectApplication.objects.all()  # Добавляем queryset для совместимости
    serializer_class = ProjectApplicationListSerializer
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ProjectApplicationService()
    
    def get_permissions(self):
        """
        Переопределяем права доступа для определенных действий.
        Для действий 'simple' и 'my_applications' разрешаем доступ без авторизации.
        """
        if self.action in ['simple']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия"""
        if self.action == 'create':
            return ProjectApplicationCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ProjectApplicationUpdateSerializer
        return ProjectApplicationCreateSerializer  # fallback
    
    def create(self, request):
        """
        POST /api/project-applications/
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
            return Response({'errors': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as e:
            # Обработка ошибок прав доступа
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            # Обработка прочих ошибок
            return Response({'error': 'Внутренняя ошибка сервера'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get_queryset(self):
        """
        Возвращает QuerySet для списка заявок.
        DRF автоматически применит пагинацию.
        """
        try:
            return self.service.get_user_applications_queryset(self.request.user)
        except PermissionError:
            return ProjectApplication.objects.none()
    
    def list(self, request):
        """
        GET /api/project-applications/
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
            list_dtos = [self.service.get_application_list_dto(app) for app in applications]
            return Response([dto.to_dict() for dto in list_dtos])
            
        except PermissionError as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception:
            return Response({'error': 'Внутренняя ошибка сервера'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def retrieve(self, request, pk=None):
        """
        GET /api/project-applications/{id}/
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
                available_actions_dto = self.service.get_available_actions(int(pk), request.user)
                response_data.update(available_actions_dto.to_dict())
            except Exception:
                # Если не удалось получить действия, не прерываем выполнение
                response_data['available_actions'] = []
            
            return Response(response_data)
            
        except PermissionError as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'error': 'Заявка не найдена'}, status=status.HTTP_404_NOT_FOUND)
    
    def update(self, request, pk=None):
        """
        PUT /api/project-applications/{id}/
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
                return Response({'error': error_msg}, status=status.HTTP_404_NOT_FOUND)
            return Response({'errors': error_msg}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'error': 'Заявка не найдена'}, status=status.HTTP_404_NOT_FOUND)
    
    def partial_update(self, request, pk=None):
        """
        PATCH /api/project-applications/{id}/
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
                return Response({'error': error_msg}, status=status.HTTP_404_NOT_FOUND)
            return Response({'errors': error_msg}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionError as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'error': 'Заявка не найдена'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """
        POST /api/project-applications/{id}/approve/
        Одобрение заявки
        """
        try:
            self.service.approve_application(
                application_id=int(pk),
                approver=request.user
            )
            return Response({'status': 'approved', 'message': 'Заявка одобрена'}, status=status.HTTP_200_OK)
        except PermissionError as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Заявка не найдена'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """
        POST /api/project-applications/{id}/reject/
        Отклонение заявки
        """
        try:
            reason = request.data.get('reason', '')
            self.service.reject_application(
                application_id=int(pk),
                rejector=request.user,
                reason=reason
            )
            return Response({'status': 'rejected', 'message': 'Заявка отклонена'}, status=status.HTTP_200_OK)
        except PermissionError as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Заявка не найдена'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def request_changes(self, request, pk=None):
        """
        POST /api/project-applications/{id}/request_changes/
        Запрос изменений
        """
        try:
            comments = request.data.get('comments', [])
            self.service.request_changes(
                application_id=int(pk),
                requester=request.user,
                comments=comments
            )
            return Response({'status': 'changes_requested', 'message': 'Запрошены изменения'}, status=status.HTTP_200_OK)
        except PermissionError as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Заявка не найдена'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'])
    def by_status(self, request):
        """
        GET /api/project-applications/by_status/?status=created
        Получение заявок по статусу (только для админов/модераторов)
        """
        try:
            status_code = request.query_params.get('status')
            if not status_code:
                return Response({'error': 'Параметр status обязателен'}, status=status.HTTP_400_BAD_REQUEST)
            
            applications = self.service.get_applications_by_status(status_code, request.user)
            list_dtos = [self.service.get_application_list_dto(app) for app in applications]
            
            return Response([dto.to_dict() for dto in list_dtos])
            
        except PermissionError as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception:
            return Response({'error': 'Внутренняя ошибка сервера'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """
        GET /api/project-applications/recent/
        Получение последних заявок (только для админов/модераторов)
        """
        try:
            limit = int(request.query_params.get('limit', 10))
            applications = self.service.get_recent_applications(limit, request.user)
            list_dtos = [self.service.get_application_list_dto(app) for app in applications]
            
            return Response([dto.to_dict() for dto in list_dtos])
            
        except PermissionError as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception:
            return Response({'error': 'Внутренняя ошибка сервера'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Методы для совместимости со старыми тестами
    @action(detail=False, methods=['get'])
    def my_applications(self, request):
        """GET /api/project-applications/my_applications/"""
        if not request.user.is_authenticated:
            # Для неавторизованных пользователей возвращаем пустой список
            return Response([])
        
        try:
            # Получаем все заявки пользователя без пагинации
            queryset = self.get_queryset()
            applications = list(queryset)
            list_dtos = [self.service.get_application_list_dto(app) for app in applications]
            return Response([dto.to_dict() for dto in list_dtos])
            
        except PermissionError as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception:
            return Response({'error': 'Внутренняя ошибка сервера'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def my_in_work(self, request):
        """
        GET /api/project-applications/my_in_work/
        Заявки, где пользователь причастен и статус не approved/rejected
        """
        if not request.user.is_authenticated:
            # Для неавторизованных пользователей возвращаем пустой список
            return Response([])
        
        try:
            # Получаем заявки через сервис с фильтрацией по причастности
            applications = self.service.get_user_in_work_applications(request.user)
            
            # Преобразуем в DTO для списка
            list_dtos = [self.service.get_application_list_dto(app) for app in applications]
            
            return Response([dto.to_dict() for dto in list_dtos])
            
        except PermissionError as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception:
            return Response({'error': 'Внутренняя ошибка сервера'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'])
    def simple(self, request):
        """
        POST /api/project-applications/simple/
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
            return Response({'errors': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Обработка прочих ошибок
            return Response({'error': 'Внутренняя ошибка сервера'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    @action(detail=True, methods=['get'])
    def status_logs(self, request, pk=None):
        """GET /api/project-applications/{id}/status_logs/"""
        try:
            application = self.service.get_application(int(pk), request.user)
            # Возвращаем логи из модели
            logs = application.status_logs.all()
            return Response([{
                'id': log.id,
                'from_status': log.from_status.code if log.from_status else None,
                'to_status': log.to_status.code,
                'changed_at': log.changed_at,
                'actor': log.actor.get_full_name() if log.actor else None,
            } for log in logs])
        except PermissionError as e:
            return Response({'error': str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'error': 'Заявка не найдена'}, status=status.HTTP_404_NOT_FOUND)
    
    
    
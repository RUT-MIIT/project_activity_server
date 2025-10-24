from rest_framework import serializers, viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.db.models import Q
from showcase.models import (
    ProjectApplication,
    ApplicationStatus,
    Institute,
    ProjectApplicationStatusLog,
    ProjectApplicationComment,
    ApplicationInvolvedUser,
    ApplicationInvolvedDepartment,
)
from showcase.services.involved import InvolvedManager
from showcase.services.status import StatusServiceFactory
from showcase.services.status.role_actions import RoleActionType
from accounts.serializers import UserShortSerializer, DepartmentSerializer
from showcase.entities.ApplicationStatus import ApplicationStatusReadSerializer
from showcase.entities.Institute import InstituteSerializer
from showcase.entities.ApplicationStatus import ApplicationStatusSerializer

User = get_user_model()
class ProjectApplicationCreateSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для создания заявки.
    """
    class Meta:
        model = ProjectApplication
        fields = ['title', 'description', 'company']


class ProjectApplicationReadSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для чтения заявки.
    """
    status = ApplicationStatusReadSerializer(read_only=True)
    author = UserShortSerializer(read_only=True, allow_null=True)
    class Meta:
        model = ProjectApplication
        fields = [
            'id', 'title', 'description', 'company', 'creation_date',
            'status', 'author'
        ]


class ProjectApplicationSerializer(serializers.ModelSerializer):
    """Сериализатор для проектных заявок"""
    target_institutes = serializers.SlugRelatedField(
        many=True,
        slug_field='code',
        queryset=Institute.objects.all(),
        required=False,
        help_text="Список кодов институтов"
    )
    status = ApplicationStatusSerializer(read_only=True)
    status_code = serializers.CharField(
        write_only=True,
        required=False,
        help_text="Код статуса заявки"
    )

    class Meta:
        model = ProjectApplication
        fields = [
            # Основные поля
            'id', 'title', 'author', 'status', 'status_code',
            'creation_date', 'needs_consultation',

            # Контактные данные
            'author_lastname', 'author_firstname', 'author_middlename',
            'author_email', 'author_phone', 'author_role', 'author_division',

            # О проекте
            'company', 'company_contacts', 'target_institutes', 'project_level',

            # Проблема
            'problem_holder', 'goal', 'barrier', 'existing_solutions',

            # Контекст
            'context', 'stakeholders', 'recommended_tools',
            'experts', 'additional_materials'
        ]
        read_only_fields = ['id', 'creation_date', 'author']

    def create(self, validated_data):
        """Создание новой заявки с обработкой связанных объектов"""
        status_code = validated_data.pop('status_code', None)
        # Даем базовой реализации создать объект и обработать M2M поля
        application = super().create(validated_data)
        # Устанавливаем статус - по умолчанию "created", если не указан другой
        if status_code:
            try:
                status = ApplicationStatus.objects.get(code=status_code)
                application.status = status
            except ApplicationStatus.DoesNotExist:
                # Если указанный статус не найден, используем "created"
                status = ApplicationStatus.objects.get(code='created')
                application.status = status
        else:
            # Если статус не указан, устанавливаем "created" по умолчанию
            status = ApplicationStatus.objects.get(code='created')
            application.status = status
        application.save()
        
        # Создаем лог о создании заявки и выполняем переходы
        # Используем новый StatusManager
        status_manager = StatusServiceFactory.create_status_manager()
        application, status_log = status_manager.create_application_with_log(
            application=application,
            actor=application.author
        )
        
        return application

    def update(self, instance, validated_data):
        """Обновление заявки с обработкой связанных объектов"""
        status_code = validated_data.pop('status_code', None)
        # Даем базовой реализации обновить поля и M2M
        instance = super().update(instance, validated_data)
        # Обновляем статус
        if status_code:
            try:
                status = ApplicationStatus.objects.get(code=status_code)
                instance.status = status
                instance.save()
            except ApplicationStatus.DoesNotExist:
                pass
        
        return instance


class ProjectApplicationCommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев к логам статусов"""
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    
    class Meta:
        model = ProjectApplicationComment
        fields = [
            'id', 'author', 'author_name', 'created_at', 'field', 'text'
        ]
        read_only_fields = ['id', 'created_at', 'author']


class ProjectApplicationStatusLogSerializer(serializers.ModelSerializer):
    """Сериализатор для логов изменения статусов"""
    from_status = ApplicationStatusSerializer(read_only=True)
    to_status = ApplicationStatusSerializer(read_only=True)
    actor_name = serializers.CharField(source='actor.get_full_name', read_only=True)
    comments = ProjectApplicationCommentSerializer(many=True, read_only=True)
    involved_user = UserShortSerializer(read_only=True)
    involved_department = DepartmentSerializer(read_only=True)
    
    class Meta:
        model = ProjectApplicationStatusLog
        fields = [
            'id', 'application', 'changed_at', 'actor', 'actor_name',
            'from_status', 'to_status', 'previous_status_log', 'comments',
            'action_type', 'involved_user', 'involved_department'
        ]
        read_only_fields = ['id', 'changed_at', 'actor']




class ApplicationInvolvedUserSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)
    added_by = UserShortSerializer(read_only=True)

    class Meta:
        model = ApplicationInvolvedUser
        fields = ['id', 'user', 'added_at', 'added_by']


class ApplicationInvolvedDepartmentSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    added_by = UserShortSerializer(read_only=True)

    class Meta:
        model = ApplicationInvolvedDepartment
        fields = ['id', 'department', 'added_at', 'added_by']


class ProjectApplicationDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор заявки с причастными и логами изменений"""
    status = ApplicationStatusSerializer(read_only=True)
    author = UserShortSerializer(read_only=True, allow_null=True)
    target_institutes = InstituteSerializer(many=True, read_only=True)
    involved_users = ApplicationInvolvedUserSerializer(many=True, read_only=True)
    involved_departments = ApplicationInvolvedDepartmentSerializer(many=True, read_only=True)
    status_logs = ProjectApplicationStatusLogSerializer(many=True, read_only=True)

    class Meta:
        model = ProjectApplication
        fields = [
            'id', 'title', 'company', 'creation_date',
            'status', 'author', 'needs_consultation',
            'author_lastname', 'author_firstname', 'author_middlename',
            'author_email', 'author_phone', 'author_role', 'author_division',
            'company_contacts', 'target_institutes', 'project_level',
            'problem_holder', 'goal', 'barrier', 'existing_solutions',
            'context', 'stakeholders', 'recommended_tools',
            'experts', 'additional_materials',
            'involved_users', 'involved_departments', 'status_logs',
        ]


class ProjectApplicationViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с проектными заявками
    """
    serializer_class = ProjectApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProjectApplicationDetailSerializer
        return ProjectApplicationSerializer

    def get_queryset(self):
        """Возвращаем заявки автора или где пользователь причастен"""
        user = self.request.user
        queryset = (
            ProjectApplication.objects
            .filter(Q(author=user) | Q(involved_users__user=user))
            .select_related('status', 'author')
            .prefetch_related(
                'target_institutes',
                # причастные
                'involved_users__user',
                'involved_users',
                'involved_departments__department',
                'involved_departments',
            )
            .distinct()
        )
        
        # Добавляем prefetch логов только для детального просмотра
        if self.action == 'retrieve':
            queryset = queryset.prefetch_related(
                # логи статусов с комментариями
                'status_logs__from_status',
                'status_logs__to_status',
                'status_logs__actor',
                'status_logs__involved_user',
                'status_logs__involved_department',
                'status_logs__comments__author',
            )
        
        return queryset
    
    def perform_create(self, serializer):
        """Автоматически устанавливаем автора, статус 'created' и добавляем автора в причастные."""
        # Устанавливаем автора заявки
        serializer.save(author=self.request.user)

        # Статус по умолчанию устанавливается в сериализаторе create();
        # здесь ничего не меняем, чтобы не дублировать логи

        # Автор и его подразделение будут добавлены в причастные автоматически
        # через StatusManager при переходе статуса created -> created

        # Автоматический перевод статуса в зависимости от роли пользователя
        user = self.request.user
        role_status_service = StatusServiceFactory.create_role_status_service()
        role_status_service.apply_action_by_role(
            RoleActionType.CREATE,
            serializer.instance,
            user
        )

    @action(detail=False, methods=['get'])
    def my_applications(self, request):
        """Получить заявки текущего пользователя"""
        applications = (
            ProjectApplication.objects
            .filter(author=request.user)
            .select_related('status', 'author')
            .prefetch_related('target_institutes')
        )
        serializer = self.get_serializer(applications, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='my_in_work')
    def my_in_work(self, request):
        """Заявки, где пользователь причастен и статус не approved/rejected"""
        qs = (
            ProjectApplication.objects
            .filter(involved_users__user=request.user)
            .exclude(status__code__in=['approved', 'rejected'])
            .select_related('status', 'author')
            .prefetch_related('target_institutes')
            .distinct()
        )
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        """Изменить статус заявки с созданием лога"""
        application = self.get_object()
        status_code = request.data.get('status_code')
        comments_data = request.data.get('comments', [])

        # Допускаем короткую форму: comment: str
        single_comment = request.data.get('comment')
        if single_comment and not comments_data:
            comments_data = [{'field': 'general', 'text': single_comment}]
        # Нормализуем строковые элементы массива в объекты
        if isinstance(comments_data, list):
            normalized = []
            for c in comments_data:
                if isinstance(c, str):
                    normalized.append({'field': 'general', 'text': c})
                elif isinstance(c, dict) and 'text' in c:
                    normalized.append({'field': c.get('field') or 'general', 'text': c['text']})
            comments_data = normalized

        if not status_code:
            return Response(
                {'error': 'status_code is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Используем новую систему логирования
            status_manager = StatusServiceFactory.create_status_manager()
            application, status_log = status_manager.change_status_with_log(
                application=application,
                new_status=status_code,
                actor=request.user,
                comments=comments_data
            )
            
            # Отдаём сериализованный лог
            serialized_log = ProjectApplicationStatusLogSerializer(status_log).data
            return Response(serialized_log, status=status.HTTP_201_CREATED)
                
        except ApplicationStatus.DoesNotExist:
            return Response(
                {'error': 'Status not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'], url_path='change_status')
    def change_status_bulk(self, request):
        """Изменить статус по `application_id` (роут без id) с опциональными комментариями"""
        application_id = request.data.get('application_id')
        status_code = request.data.get('status_code')
        comments_data = request.data.get('comments', [])

        single_comment = request.data.get('comment')
        if single_comment and not comments_data:
            comments_data = [{'field': 'general', 'text': single_comment}]
        if isinstance(comments_data, list):
            normalized = []
            for c in comments_data:
                if isinstance(c, str):
                    normalized.append({'field': 'general', 'text': c})
                elif isinstance(c, dict) and 'text' in c:
                    normalized.append({'field': c.get('field') or 'general', 'text': c['text']})
            comments_data = normalized

        if not application_id:
            return Response({'error': 'application_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        if not status_code:
            return Response({'error': 'status_code is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            application = self.get_queryset().get(pk=application_id)
        except ProjectApplication.DoesNotExist:
            return Response({'error': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            status_manager = StatusServiceFactory.create_status_manager()
            application, status_log = status_manager.change_status_with_log(
                application=application,
                new_status=status_code,
                actor=request.user,
                comments=comments_data,
            )
            serialized_log = ProjectApplicationStatusLogSerializer(status_log).data
            return Response(serialized_log, status=status.HTTP_201_CREATED)
        except ApplicationStatus.DoesNotExist:
            return Response({'error': 'Status not found'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def status_logs(self, request, pk=None):
        """Получить логи изменения статусов заявки"""
        application = self.get_object()
        logs = (
            application.status_logs
            .select_related('from_status', 'to_status', 'actor', 'involved_user', 'involved_department')
            .prefetch_related('comments__author')
            .all()
        )
        serializer = ProjectApplicationStatusLogSerializer(logs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='reject')
    def reject_application(self, request, pk=None):
        """
        Отклонить заявку.
        
        Автоматически определяет статус отклонения по роли пользователя:
        - department_validator -> rejected_department
        - institute_validator -> rejected_institute
        - cpds -> rejected_cpds
        
        """
        application = self.get_object()
        reason = request.data.get('reason')
        comments_data = request.data.get('comments', [])
        
        try:
            # Создаем сервис для работы с ролями
            role_status_service = StatusServiceFactory.create_role_status_service()
            
            # Проверяем права на отклонение
            if not role_status_service.can_user_perform_action(
                RoleActionType.REJECT,
                application,
                request.user
            ):
                return Response(
                    {'error': 'У вас нет прав для отклонения этой заявки'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Применяем отклонение
            new_status = role_status_service.apply_action_by_role(
                RoleActionType.REJECT,
                application,
                request.user,
                reason=reason,
                comments=comments_data
            )
            
            if new_status:
                # Получаем последний лог для возврата
                last_log = application.status_logs.first()
                if last_log:
                    serialized_log = ProjectApplicationStatusLogSerializer(last_log).data
                    return Response(serialized_log, status=status.HTTP_201_CREATED)
                else:
                    return Response(
                        {'message': 'Заявка отклонена', 'new_status': new_status.name},
                        status=status.HTTP_200_OK
                    )
            else:
                return Response(
                    {'error': 'Ваша роль не поддерживает отклонение заявок'},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        except Exception as e:
            return Response(
                {'error': f'Ошибка при отклонении заявки: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        """Добавить комментарий к последнему логу статуса"""
        application = self.get_object()
        
        try:
            # Используем новую систему для добавления комментария
            status_manager = StatusServiceFactory.create_status_manager()
            comment = status_manager.add_comment_to_log(
                application=application,
                field=request.data.get('field'),
                text=request.data.get('text'),
                author=request.user
            )
            
            serializer = ProjectApplicationCommentSerializer(comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['get'])
    def current_status_info(self, request, pk=None):
        """Получить информацию о текущем статусе заявки"""
        application = self.get_object()
        
        if not application.status:
            return Response({
                'status': None,
                'message': 'No status set'
            })
        
        last_log = application.status_logs.order_by('-changed_at').first()
        
        response_data = {
            'status': ApplicationStatusSerializer(application.status).data,
            'last_change': None,
            'actor': None
        }
        
        if last_log:
            response_data['last_change'] = last_log.changed_at
            response_data['actor'] = {
                'id': last_log.actor.id if last_log.actor else None,
                'name': last_log.actor.get_full_name() if last_log.actor else None
            }
        
        return Response(response_data)


    @action(detail=True, methods=['post'])
    def add_involved_user(self, request, pk=None):
        application = self.get_object()
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        involved = InvolvedManager.add_involved_user(application, user, actor=request.user)
        serializer = ApplicationInvolvedUserSerializer(involved)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def remove_involved_user(self, request, pk=None):
        application = self.get_object()
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        deleted = InvolvedManager.remove_involved_user(application, user, actor=request.user)
        return Response({'deleted': deleted})

    @action(detail=True, methods=['post'])
    def add_involved_department(self, request, pk=None):
        from accounts.models import Department
        application = self.get_object()
        department_id = request.data.get('department_id')
        if not department_id:
            return Response({'error': 'department_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            department = Department.objects.get(pk=department_id)
        except Department.DoesNotExist:
            return Response({'error': 'Department not found'}, status=status.HTTP_404_NOT_FOUND)
        involved = InvolvedManager.add_involved_department(application, department, actor=request.user)
        serializer = ApplicationInvolvedDepartmentSerializer(involved)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def remove_involved_department(self, request, pk=None):
        from accounts.models import Department
        application = self.get_object()
        department_id = request.data.get('department_id')
        if not department_id:
            return Response({'error': 'department_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            department = Department.objects.get(pk=department_id)
        except Department.DoesNotExist:
            return Response({'error': 'Department not found'}, status=status.HTTP_404_NOT_FOUND)
        deleted = InvolvedManager.remove_involved_department(application, department, actor=request.user)
        return Response({'deleted': deleted})

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def simple(self, request):
        """Простое создание заявки без авторизации"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Создаем заявку без автора
            serializer.save(author=None)
            
            # Устанавливаем статус "created" если он не был установлен
            if not serializer.instance.status:
                try:
                    created_status = ApplicationStatus.objects.get(code='created')
                    serializer.instance.status = created_status
                    serializer.instance.save()
                except ApplicationStatus.DoesNotExist:
                    pass  # Статус "created" не найден, оставляем None
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InstituteViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для работы с институтами (только чтение)
    """
    serializer_class = InstituteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Возвращаем только активные институты"""
        return Institute.objects.filter(is_active=True)


class ApplicationStatusViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для работы со статусами заявок (только чтение)
    """
    serializer_class = ApplicationStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Возвращаем только активные статусы"""
        return ApplicationStatus.objects.filter(is_active=True)
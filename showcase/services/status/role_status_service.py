"""
Сервис для автоматического перевода статусов по ролям пользователей.

Реализует принцип SRP - отвечает только за логику перевода статусов по ролям.
Использует конфигурационный подход для определения переходов.
"""

from typing import Optional, Dict, Any
from django.contrib.auth import get_user_model
from django.db import transaction

from showcase.models import ProjectApplication, ApplicationStatus
from .manager import StatusManager
from .role_actions import RoleActionType, get_action_config, get_available_actions_for_role

User = get_user_model()


class RoleStatusService:
    """
    Сервис для автоматического перевода статусов заявок в зависимости от роли пользователя.
    
    Определяет, нужно ли переводить заявку в другой статус при создании,
    основываясь на роли автора заявки.
    """
    
    def __init__(self, status_manager: StatusManager):
        self.status_manager = status_manager
    
    def apply_action_by_role(
        self,
        action_type: RoleActionType,
        application: ProjectApplication,
        actor: User,
        **kwargs
    ) -> Optional[ApplicationStatus]:
        """
        Универсальный метод для применения действий по ролям.
        
        Args:
            action_type: Тип действия
            application: Заявка
            actor: Пользователь
            **kwargs: Дополнительные параметры (reason, comment и т.д.)
            
        Returns:
            ApplicationStatus: Новый статус, если действие было применено, иначе None
        """
        try:
            role_code = getattr(getattr(actor, 'role', None), 'code', None)
            if not role_code:
                return None
            
            # Получаем конфигурацию для действия и роли
            config = get_action_config(action_type, role_code)
            if not config:
                return None
            
            # Проверяем дополнительные условия
            if config.get('requires_department', False):
                has_department = getattr(actor, 'department', None) is not None
                if not has_department:
                    return None
            
            # Получаем статус из БД
            status_code = config.get('status_code')
            if not status_code:
                return None
                
            new_status = ApplicationStatus.objects.get(code=status_code)
            
            # Подготавливаем комментарии
            comments = self._prepare_comments(config, **kwargs)
            
            # Применяем переход статуса
            self.status_manager.change_status(
                application=application,
                new_status=new_status,
                actor=actor,
                comments=comments
            )
            return new_status
                
        except ApplicationStatus.DoesNotExist:
            # Если статус не найден в справочнике, ничего не делаем
            pass
        except Exception:
            # Логируем ошибку, но не прерываем процесс
            pass
            
        return None
    
    def _prepare_comments(self, config: Dict[str, Any], **kwargs) -> list[Dict[str, str]]:
        """
        Подготавливает комментарии на основе конфигурации.
        
        Args:
            config: Конфигурация действия
            **kwargs: Дополнительные параметры (включая comments)
            
        Returns:
            List комментариев для лога
        """
        comments = []
        
        # Добавляем комментарии из конфигурации (например, rejection_reason)
        comment_template = config.get('comment_template', '')
        if comment_template:
            comment_field = config.get('comment_field', 'general')
            
            # Форматируем шаблон с переданными параметрами
            try:
                formatted_text = comment_template.format(**kwargs)
            except (KeyError, ValueError):
                # Если не удалось отформатировать, используем шаблон как есть
                formatted_text = comment_template
            
            comments.append({
                'field': comment_field,
                'text': formatted_text
            })
        
        # Добавляем переданные комментарии из запроса
        additional_comments = kwargs.get('comments', [])
        if isinstance(additional_comments, list):
            for comment in additional_comments:
                if isinstance(comment, dict) and 'field' in comment and 'text' in comment:
                    comments.append({
                        'field': comment['field'],
                        'text': comment['text']
                    })
        
        return comments
    
    def get_available_actions_for_role(
        self,
        role_code: str
    ) -> Dict[RoleActionType, Dict[str, Any]]:
        """
        Возвращает все доступные действия для роли.
        
        Args:
            role_code: Код роли
            
        Returns:
            Dict с доступными действиями и их конфигурациями
        """
        return get_available_actions_for_role(role_code)
    
    def can_user_perform_action(
        self,
        action_type: RoleActionType,
        application: ProjectApplication,
        user: User
    ) -> bool:
        """
        Проверяет, может ли пользователь выполнить действие.
        
        Args:
            action_type: Тип действия
            application: Заявка
            user: Пользователь
            
        Returns:
            bool: True если пользователь может выполнить действие
        """
        # TODO: Реализовать логику проверки прав доступа
        # Пока возвращаем True для всех пользователей
        return True
    
    # DEPRECATED METHODS - для обратной совместимости
    
    def apply_role_based_transition(
        self,
        application: ProjectApplication,
        actor: User
    ) -> Optional[ApplicationStatus]:
        """
        DEPRECATED: используйте apply_action_by_role(RoleActionType.CREATE, ...)
        
        Применяет переход статуса на основе роли пользователя.
        """
        return self.apply_action_by_role(
            RoleActionType.CREATE,
            application,
            actor
        )
    
    def get_available_transitions_for_role(self, role_code: Optional[str]) -> list[str]:
        """
        DEPRECATED: используйте get_available_actions_for_role()
        
        Возвращает список доступных переходов для роли.
        """
        # Для обратной совместимости возвращаем только CREATE действия
        available_actions = self.get_available_actions_for_role(role_code)
        create_config = available_actions.get(RoleActionType.CREATE)
        if create_config and 'status_code' in create_config:
            return [create_config['status_code']]
        return []
    
    def apply_rejection_by_role(
        self,
        application: ProjectApplication,
        actor: User,
        reason: Optional[str] = None
    ) -> Optional[ApplicationStatus]:
        """
        DEPRECATED: используйте apply_action_by_role(RoleActionType.REJECT, ...)
        
        Применяет отклонение заявки на основе роли пользователя.
        """
        return self.apply_action_by_role(
            RoleActionType.REJECT,
            application,
            actor,
            reason=reason
        )
    
    def can_user_reject_application(
        self,
        application: ProjectApplication,
        user: User
    ) -> bool:
        """
        DEPRECATED: используйте can_user_perform_action(RoleActionType.REJECT, ...)
        
        Проверяет, может ли пользователь отклонить заявку.
        """
        return self.can_user_perform_action(
            RoleActionType.REJECT,
            application,
            user
        )
    

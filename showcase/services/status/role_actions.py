"""
Конфигурация действий по ролям пользователей.

Содержит enum для типов действий и маппинг ролей к статусам.
Реализует принцип OCP - новые действия добавляются через конфигурацию.
"""

from enum import Enum
from typing import Dict, Any


class RoleActionType(Enum):
    """Типы действий с заявками по ролям."""
    CREATE = 'create'
    REJECT = 'reject'
    APPROVE = 'approve'  # для будущего использования
    REQUEST_REVISION = 'request_revision'  # для будущего использования


# Конфигурация маппинга ролей к действиям и статусам
ROLE_ACTION_MAPPING: Dict[RoleActionType, Dict[str, Dict[str, Any]]] = {
    RoleActionType.CREATE: {
        'mentor': {
            'status_code': 'await_department',
            'requires_department': True,
            'comment_template': 'Заявка создана ментором и направлена в департамент'
        },
        'department_validator': {
            'status_code': 'await_institute',
            'comment_template': 'Заявка создана валидатором департамента'
        },
        'institute_validator': {
            'status_code': 'await_cpds',
            'comment_template': 'Заявка создана валидатором института'
        },
    },
    RoleActionType.REJECT: {
        'department_validator': {
            'status_code': 'rejected_department',
            'comment_field': 'rejection_reason',
            'comment_template': 'Причина отклонения: {reason}'
        },
        'institute_validator': {
            'status_code': 'rejected_institute',
            'comment_field': 'rejection_reason',
            'comment_template': 'Причина отклонения: {reason}'
        },
        'cpds': {
            'status_code': 'rejected_cpds',
            'comment_field': 'rejection_reason',
            'comment_template': 'Причина отклонения: {reason}'
        },
    },
    # Заготовки для будущих действий
    RoleActionType.APPROVE: {
        'department_validator': {
            'status_code': 'approved_department',
            'comment_template': 'Заявка одобрена департаментом'
        },
        'institute_validator': {
            'status_code': 'approved_institute',
            'comment_template': 'Заявка одобрена институтом'
        },
        'cpds': {
            'status_code': 'approved_cpds',
            'comment_template': 'Заявка одобрена ЦПДС'
        },
    },
    RoleActionType.REQUEST_REVISION: {
        'department_validator': {
            'status_code': 'revision_required_department',
            'comment_field': 'revision_reason',
            'comment_template': 'Требуется доработка: {reason}'
        },
        'institute_validator': {
            'status_code': 'revision_required_institute',
            'comment_field': 'revision_reason',
            'comment_template': 'Требуется доработка: {reason}'
        },
        'cpds': {
            'status_code': 'revision_required_cpds',
            'comment_field': 'revision_reason',
            'comment_template': 'Требуется доработка: {reason}'
        },
    },
}


def get_action_config(action_type: RoleActionType, role_code: str) -> Dict[str, Any]:
    """
    Получить конфигурацию для конкретного действия и роли.
    
    Args:
        action_type: Тип действия
        role_code: Код роли
        
    Returns:
        Dict с конфигурацией или пустой dict, если не найдено
    """
    return ROLE_ACTION_MAPPING.get(action_type, {}).get(role_code, {})


def get_available_actions_for_role(role_code: str) -> Dict[RoleActionType, Dict[str, Any]]:
    """
    Получить все доступные действия для роли.
    
    Args:
        role_code: Код роли
        
    Returns:
        Dict с доступными действиями и их конфигурациями
    """
    available_actions = {}
    for action_type, role_configs in ROLE_ACTION_MAPPING.items():
        if role_code in role_configs:
            available_actions[action_type] = role_configs[role_code]
    return available_actions


def get_available_roles_for_action(action_type: RoleActionType) -> list[str]:
    """
    Получить все роли, которые могут выполнить действие.
    
    Args:
        action_type: Тип действия
        
    Returns:
        List кодов ролей
    """
    return list(ROLE_ACTION_MAPPING.get(action_type, {}).keys())

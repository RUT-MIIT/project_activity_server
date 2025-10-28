"""
Тесты для действия "отправить на доработку".

Проверяет логику отправки заявок на доработку и доступность этого действия.
"""

import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import Mock, patch

from showcase.services.application_service import ProjectApplicationService
from showcase.domain.application import ProjectApplicationDomain

User = get_user_model()


class TestRevisionAction(TestCase):
    """Тесты для действия отправки на доработку."""
    
    def setUp(self):
        """Настройка тестов."""
        self.service = ProjectApplicationService()
        
        # Создаем моки
        self.mock_application = Mock()
        self.mock_user = Mock()
        self.mock_status = Mock()
    
    def test_revision_permissions_different_statuses(self):
        """Тест прав на отправку на доработку для разных статусов."""
        test_cases = [
            # (статус, роль, ожидаемый_результат)
            ('created', 'department_validator', False),  # Нельзя отправлять на доработку уже созданные
            ('await_department', 'department_validator', True),  # Можно отправлять на доработку
            ('await_institute', 'institute_validator', True),  # Можно отправлять на доработку
            ('await_cpds', 'department_validator', False),  # Валидатор подразделения не может для статуса await_cpds
            ('approved', 'department_validator', False),  # Нельзя отправлять одобренные
            ('rejected', 'institute_validator', False),  # Нельзя отправлять отклоненные
        ]
        
        for status_code, user_role, expected_has_permission in test_cases:
            with self.subTest(status=status_code, role=user_role):
                # Настраиваем моки
                self.mock_application.status.code = status_code
                self.mock_user.role.code = user_role
                self.mock_user.department = Mock()
                self.mock_user.department.id = 1
                
                # Мокаем причастные подразделения
                mock_involved_departments = Mock()
                mock_involved_departments.filter.return_value.exists.return_value = True
                self.mock_application.involved_departments.all.return_value = mock_involved_departments
                
                # Проверяем права
                has_permission = self.service._has_manage_permissions(
                    self.mock_application,
                    self.mock_user,
                    status_code,
                    user_role
                )
                
                self.assertEqual(has_permission, expected_has_permission,
                               f"Статус {status_code}, роль {user_role}: ожидалось {expected_has_permission}, получено {has_permission}")
    
    def test_revision_permissions_different_roles(self):
        """Тест прав на отправку на доработку для разных ролей."""
        test_cases = [
            # (роль, ожидаемый_результат)
            ('department_validator', True),  # Валидатор подразделения может
            ('institute_validator', True),   # Валидатор института может
            ('admin', True),                 # Админ может управлять заявкой
            ('cpds', True),                  # CPDS может управлять заявкой
            ('user', False),                 # Обычный пользователь не может
            ('moderator', False),            # Модератор не может
        ]
        
        for user_role, expected_has_permission in test_cases:
            with self.subTest(role=user_role):
                # Настраиваем моки
                self.mock_application.status.code = 'await_department'
                self.mock_user.role.code = user_role
                self.mock_user.department = Mock()
                self.mock_user.department.id = 1
                
                # Мокаем причастные подразделения
                mock_involved_departments = Mock()
                mock_involved_departments.filter.return_value.exists.return_value = True
                self.mock_application.involved_departments.all.return_value = mock_involved_departments
                
                # Проверяем права
                has_permission = self.service._has_manage_permissions(
                    self.mock_application,
                    self.mock_user,
                    'await_department',
                    user_role
                )
                
                self.assertEqual(has_permission, expected_has_permission,
                               f"Роль {user_role}: ожидалось {expected_has_permission}, получено {has_permission}")
    
    def test_revision_permissions_without_involved_department(self):
        """Тест прав на отправку на доработку без причастного подразделения."""
        # Настраиваем моки
        self.mock_application.status.code = 'await_department'
        self.mock_user.role.code = 'department_validator'
        self.mock_user.department = Mock()
        self.mock_user.department.id = 1
        
        # Мокаем причастные подразделения (пустые)
        mock_involved_departments = Mock()
        mock_involved_departments.filter.return_value.exists.return_value = False
        self.mock_application.involved_departments.all.return_value = mock_involved_departments
        
        # Проверяем права
        has_permission = self.service._has_manage_permissions(
            self.mock_application,
            self.mock_user,
            'await_department',
            'department_validator'
        )
        
        self.assertFalse(has_permission, "Валидатор без причастного подразделения не должен иметь права на отправку на доработку")
    
    def test_available_actions_includes_revision(self):
        """Тест включения действия отправки на доработку в доступные действия."""
        # Настраиваем моки
        self.mock_application.status.code = 'await_department'
        self.mock_user.role.code = 'department_validator'
        self.mock_user.department = Mock()
        self.mock_user.department.id = 1
        
        # Мокаем причастные подразделения
        mock_involved_departments = Mock()
        mock_involved_departments.filter.return_value.exists.return_value = True
        self.mock_application.involved_departments.all.return_value = mock_involved_departments
        
        with patch.object(self.service.repository, 'get_by_id_simple', return_value=self.mock_application):
            # Получаем доступные действия
            actions_dto = self.service.get_available_actions(1, self.mock_user)
            
            # Проверяем, что действие отправки на доработку включено
            action_names = [action.action for action in actions_dto.actions]
            self.assertIn('request_revision', action_names, 
                         "Действие 'request_revision' должно быть в доступных действиях")
            
            # Проверяем конфигурацию действия
            revision_action = next((action for action in actions_dto.actions if action.action == 'request_revision'), None)
            self.assertIsNotNone(revision_action, "Действие отправки на доработку должно быть найдено")
            self.assertEqual(revision_action.label, "Отправить на доработку")
            self.assertEqual(revision_action.config['status_code'], 'created')
    
    @patch('showcase.services.application_service.ApplicationStatus.objects.get')
    @patch('showcase.services.application_service.ApplicationLoggingService.log_status_change')
    def test_request_revision_execution(self, mock_log_status, mock_status_get):
        """Тест выполнения отправки на доработку."""
        # Настраиваем моки
        mock_application = Mock()
        mock_application.status.code = 'await_department'
        mock_application.status = Mock()
        
        mock_user = Mock()
        mock_user.role.code = 'department_validator'
        mock_user.department = Mock()
        mock_user.department.id = 1
        
        # Мокаем причастные подразделения
        mock_involved_departments = Mock()
        mock_involved_departments.filter.return_value.exists.return_value = True
        mock_application.involved_departments.all.return_value = mock_involved_departments
        
        mock_new_status = Mock()
        mock_status_get.return_value = mock_new_status
        
        with patch.object(self.service.repository, 'get_by_id_simple', return_value=mock_application):
            with patch.object(self.service, '_has_manage_permissions', return_value=True):
                with patch.object(ProjectApplicationDomain, 'can_change_status', return_value=(True, "")):
                    # Выполняем отправку на доработку
                    result = self.service.request_revision(1, mock_user, [{'field': 'status', 'text': 'Нужна доработка'}])
                    
                    # Проверяем результат
                    self.assertEqual(result, mock_application)
                    
                    # Проверяем, что статус был изменен
                    self.assertEqual(mock_application.status, mock_new_status)
                    mock_application.save.assert_called_once()
                    
                    # Проверяем, что изменение было залогировано
                    mock_log_status.assert_called_once()
    
    def test_debug_revision_flow(self):
        """Отладочный тест для потока отправки на доработку."""
        print("\n=== Отладка действия 'отправить на доработку' ===")
        
        roles_to_test = ['department_validator', 'institute_validator', 'admin', 'cpds', 'user']
        statuses_to_test = ['await_department', 'await_institute', 'await_cpds', 'created', 'approved', 'rejected']
        
        for role in roles_to_test:
            print(f"\nРоль: {role}")
            for status in statuses_to_test:
                # Симулируем проверку прав
                can_revision = (
                    status in ['await_department', 'await_institute', 'await_cpds'] and
                    role in ['department_validator', 'institute_validator']
                )
                
                print(f"  Статус {status:15} -> {'[OK]' if can_revision else '[NO]'}")
        
        print("\n=== Резюме ===")
        print("• Только валидаторы (department_validator, institute_validator) могут отправлять на доработку")
        print("• Можно отправлять только заявки в статусах: await_department, await_institute, await_cpds")
        print("• Нельзя отправлять одобренные (approved) или отклоненные (rejected) заявки")
        print("• Валидатор должен иметь причастное подразделение к заявке")


if __name__ == '__main__':
    print("Запуск тестов действия 'отправить на доработку'...")
    print("Проверяет логику отправки заявок на доработку.")
    print()
    
    import unittest
    unittest.main(verbosity=2)

"""
Тесты для действия "Сохранить изменение".

Проверяет логику показа действия "Сохранить изменение" для различных статусов и ролей.
"""

import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import Mock, patch

from showcase.services.application_service import ProjectApplicationService

User = get_user_model()


class TestSaveChangesAction(TestCase):
    """Тесты для действия 'Сохранить изменение'."""
    
    def setUp(self):
        """Настройка тестов."""
        self.service = ProjectApplicationService()
        
        # Создаем моки
        self.mock_application = Mock()
        self.mock_user = Mock()
        self.mock_status = Mock()
    
    def test_save_changes_for_returned_statuses(self):
        """Тест показа действия 'Сохранить изменение' для статусов возврата."""
        test_cases = [
            # (статус, роль, ожидаемый_результат)
            ('returned_department', 'user', True),  # Пользователь может сохранить изменения
            ('returned_institute', 'user', True),  # Пользователь может сохранить изменения
            ('returned_cpds', 'user', True),       # Пользователь может сохранить изменения
            ('created', 'user', False),            # Обычный статус - не показываем
            ('await_department', 'user', False),  # Обычный статус - не показываем
        ]
        
        for status_code, user_role, expected_show in test_cases:
            with self.subTest(status=status_code, role=user_role):
                # Настраиваем моки
                self.mock_application.status.code = status_code
                self.mock_user.role.code = user_role
                self.mock_user.department = None
                
                # Проверяем, нужно ли показывать действие
                should_show = self.service._should_show_save_changes_action(
                    self.mock_application,
                    self.mock_user,
                    status_code,
                    user_role
                )
                
                self.assertEqual(should_show, expected_show,
                               f"Статус {status_code}, роль {user_role}: ожидалось {expected_show}, получено {should_show}")
    
    def test_save_changes_for_manage_permissions(self):
        """Тест показа действия 'Сохранить изменение' при наличии прав на управление."""
        test_cases = [
            # (статус, роль, ожидаемый_результат)
            ('await_department', 'admin', True),           # Админ может управлять
            ('await_institute', 'cpds', True),            # CPDS может управлять
            ('await_cpds', 'department_validator', False), # Валидатор подразделения не может для статуса await_cpds
            ('created', 'user', False),                   # Обычный пользователь не может
            ('approved', 'admin', False),                 # Одобренные заявки не показываем
        ]
        
        for status_code, user_role, expected_show in test_cases:
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
                
                # Проверяем, нужно ли показывать действие
                should_show = self.service._should_show_save_changes_action(
                    self.mock_application,
                    self.mock_user,
                    status_code,
                    user_role
                )
                
                self.assertEqual(should_show, expected_show,
                               f"Статус {status_code}, роль {user_role}: ожидалось {expected_show}, получено {should_show}")
    
    def test_available_actions_includes_save_changes(self):
        """Тест включения действия 'Сохранить изменение' в доступные действия."""
        # Настраиваем моки для статуса возврата
        self.mock_application.status.code = 'returned_department'
        self.mock_user.role.code = 'user'
        self.mock_user.department = None
        
        with patch.object(self.service.repository, 'get_by_id_simple', return_value=self.mock_application):
            # Получаем доступные действия
            actions_dto = self.service.get_available_actions(1, self.mock_user)
            
            # Проверяем, что действие "Сохранить изменение" включено
            action_names = [action.action for action in actions_dto.actions]
            self.assertIn('save_changes', action_names, 
                         "Действие 'save_changes' должно быть в доступных действиях")
            
            # Проверяем конфигурацию действия
            save_action = next((action for action in actions_dto.actions if action.action == 'save_changes'), None)
            self.assertIsNotNone(save_action, "Действие 'Сохранить изменение' должно быть найдено")
            self.assertEqual(save_action.label, "Сохранить изменение")
            self.assertEqual(save_action.config['status_code'], 'returned_department')
    
    def test_available_actions_for_manage_permissions(self):
        """Тест доступных действий для пользователей с правами на управление."""
        # Настраиваем моки
        self.mock_application.status.code = 'await_department'
        self.mock_user.role.code = 'admin'
        self.mock_user.department = None
        
        with patch.object(self.service.repository, 'get_by_id_simple', return_value=self.mock_application):
            # Получаем доступные действия
            actions_dto = self.service.get_available_actions(1, self.mock_user)
            
            # Проверяем, что есть все действия управления
            action_names = [action.action for action in actions_dto.actions]
            expected_actions = ['approve', 'reject', 'request_revision', 'save_changes']
            
            for expected_action in expected_actions:
                self.assertIn(expected_action, action_names, 
                             f"Действие '{expected_action}' должно быть в доступных действиях")
    
    def test_debug_save_changes_flow(self):
        """Отладочный тест для потока действия 'Сохранить изменение'."""
        print("\n=== Отладка действия 'Сохранить изменение' ===")
        
        statuses_to_test = [
            'returned_department', 'returned_institute', 'returned_cpds',
            'await_department', 'await_institute', 'await_cpds',
            'created', 'approved', 'rejected'
        ]
        roles_to_test = ['admin', 'cpds', 'department_validator', 'institute_validator', 'user']
        
        for status in statuses_to_test:
            print(f"\nСтатус: {status}")
            for role in roles_to_test:
                # Симулируем проверку
                is_returned_status = status in ['returned_department', 'returned_institute', 'returned_cpds']
                has_manage_permissions = role in ['admin', 'cpds'] or (
                    role in ['department_validator', 'institute_validator'] and 
                    status in ['await_department', 'await_institute', 'await_cpds']
                )
                
                should_show = is_returned_status or has_manage_permissions
                print(f"  Роль {role:20} -> {'[OK]' if should_show else '[NO]'}")
        
        print("\n=== Резюме ===")
        print("• Действие 'Сохранить изменение' показывается для статусов возврата: returned_department, returned_institute, returned_cpds")
        print("• Действие также показывается при наличии прав на управление заявкой")
        print("• Это позволяет пользователям сохранять изменения в заявках")


if __name__ == '__main__':
    print("Запуск тестов действия 'Сохранить изменение'...")
    print("Проверяет логику показа действия для различных статусов и ролей.")
    print()
    
    import unittest
    unittest.main(verbosity=2)

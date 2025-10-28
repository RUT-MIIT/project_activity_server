"""
Тесты для диагностики проблемы с available_actions.

Проверяет логику определения доступных действий для заявок
и выявляет причины возврата пустого массива.
"""

import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import Mock, patch

from showcase.services.application_service import ProjectApplicationService

User = get_user_model()


class TestAvailableActionsDebug(TestCase):
    """Тесты для диагностики available_actions."""
    
    def setUp(self):
        """Настройка тестов."""
        self.service = ProjectApplicationService()
        
        # Создаем моки
        self.mock_application = Mock()
        self.mock_user = Mock()
        self.mock_status = Mock()
    
    def test_available_actions_with_different_statuses(self):
        """Тест доступных действий для разных статусов."""
        # Тестируем различные статусы
        test_cases = [
            ('created', 'user', False),  # Обычный пользователь, статус created
            ('created', 'admin', False),  # Админ, статус created
            ('await_department', 'user', False),  # Обычный пользователь, статус await_department
            ('await_department', 'admin', True),  # Админ, статус await_department
            ('await_department', 'cpds', True),  # CPDS, статус await_department
            ('await_department', 'department_validator', False),  # Валидатор без причастного подразделения
            ('await_institute', 'user', False),  # Обычный пользователь, статус await_institute
            ('await_institute', 'admin', True),  # Админ, статус await_institute
            ('await_institute', 'cpds', True),  # CPDS, статус await_institute
            ('await_institute', 'institute_validator', False),  # Валидатор без причастного подразделения
            ('approved', 'admin', False),  # Админ, статус approved
            ('rejected', 'admin', False),  # Админ, статус rejected
        ]
        
        for status_code, user_role, expected_has_actions in test_cases:
            with self.subTest(status=status_code, role=user_role):
                # Настраиваем моки
                self.mock_application.status.code = status_code
                self.mock_user.role.code = user_role
                self.mock_user.department = None  # Нет подразделения
                
                # Проверяем права
                has_actions = self.service._has_approve_reject_permissions(
                    self.mock_application,
                    self.mock_user,
                    status_code,
                    user_role
                )
                
                self.assertEqual(has_actions, expected_has_actions,
                               f"Статус {status_code}, роль {user_role}: ожидалось {expected_has_actions}, получено {has_actions}")
    
    def test_available_actions_with_involved_departments(self):
        """Тест доступных действий с причастными подразделениями."""
        # Создаем мок подразделения
        mock_department = Mock()
        mock_department.id = 1
        
        # Создаем мок причастных подразделений
        mock_involved_departments = Mock()
        mock_involved_departments.filter.return_value.exists.return_value = True
        
        self.mock_application.involved_departments.all.return_value = mock_involved_departments
        self.mock_user.department = mock_department
        
        # Тестируем валидатора с причастным подразделением
        has_actions = self.service._has_approve_reject_permissions(
            self.mock_application,
            self.mock_user,
            'await_department',
            'department_validator'
        )
        
        self.assertTrue(has_actions, "Валидатор с причастным подразделением должен иметь права")
    
    def test_available_actions_without_involved_departments(self):
        """Тест доступных действий без причастных подразделений."""
        # Создаем мок подразделения
        mock_department = Mock()
        mock_department.id = 1
        
        # Создаем мок причастных подразделений (пустой)
        mock_involved_departments = Mock()
        mock_involved_departments.filter.return_value.exists.return_value = False
        
        self.mock_application.involved_departments.all.return_value = mock_involved_departments
        self.mock_user.department = mock_department
        
        # Тестируем валидатора без причастного подразделения
        has_actions = self.service._has_approve_reject_permissions(
            self.mock_application,
            self.mock_user,
            'await_department',
            'department_validator'
        )
        
        self.assertFalse(has_actions, "Валидатор без причастного подразделения не должен иметь права")
    
    def test_available_actions_user_without_department(self):
        """Тест доступных действий для пользователя без подразделения."""
        # Пользователь без подразделения
        self.mock_user.department = None
        
        # Тестируем валидатора без подразделения
        has_actions = self.service._has_approve_reject_permissions(
            self.mock_application,
            self.mock_user,
            'await_department',
            'department_validator'
        )
        
        self.assertFalse(has_actions, "Валидатор без подразделения не должен иметь права")
    
    def test_get_available_actions_integration(self):
        """Интеграционный тест получения доступных действий."""
        # Настраиваем моки
        self.mock_application.status.code = 'await_department'
        self.mock_user.role.code = 'admin'
        
        with patch.object(self.service.repository, 'get_by_id_simple', return_value=self.mock_application):
            # Получаем доступные действия
            actions_dto = self.service.get_available_actions(180, self.mock_user)
            
            # Проверяем, что действия есть
            self.assertIsNotNone(actions_dto)
            self.assertIsInstance(actions_dto.actions, list)
            
            # Для админа с статусом await_department должны быть действия
            if self.mock_application.status.code == 'await_department' and self.mock_user.role.code == 'admin':
                self.assertGreater(len(actions_dto.actions), 0, 
                                 "Админ должен иметь доступные действия для статуса await_department")
    
    def test_debug_specific_case(self):
        """Тест для конкретного случая из запроса (ID 180)."""
        # Симулируем реальный случай
        application_id = 180
        
        # Создаем мок заявки
        mock_application = Mock()
        mock_application.status.code = 'created'  # Предполагаем статус created
        
        # Создаем мок пользователя
        mock_user = Mock()
        mock_user.role.code = 'user'  # Предполагаем обычного пользователя
        
        with patch.object(self.service.repository, 'get_by_id_simple', return_value=mock_application):
            # Получаем доступные действия
            actions_dto = self.service.get_available_actions(application_id, mock_user)
            
            # Для обычного пользователя со статусом created не должно быть действий
            self.assertEqual(len(actions_dto.actions), 0, 
                           "Обычный пользователь со статусом created не должен иметь доступных действий")
            
            # Выводим отладочную информацию
            print(f"\nОтладка для заявки {application_id}:")
            print(f"Статус заявки: {mock_application.status.code}")
            print(f"Роль пользователя: {mock_user.role.code}")
            print(f"Доступные действия: {len(actions_dto.actions)}")
            
            if len(actions_dto.actions) == 0:
                print("Причина: Обычные пользователи не имеют прав на approve/reject")
                print("Требуются роли: admin, cpds, department_validator, institute_validator")
                print("Или статус должен быть: await_department, await_institute")


if __name__ == '__main__':
    print("Запуск тестов диагностики available_actions...")
    print("Эти тесты помогут выявить причины пустого массива available_actions.")
    print()
    
    import unittest
    unittest.main(verbosity=2)


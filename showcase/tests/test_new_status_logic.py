"""
Тесты для новой логики определения статусов.

Проверяет обновленную логику calculate_initial_status и доступных действий
согласно новым бизнес-правилам.
"""

import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import Mock, patch

from showcase.domain.application import ProjectApplicationDomain
from showcase.services.application_service import ProjectApplicationService

User = get_user_model()


class TestNewStatusLogic(TestCase):
    """Тесты для новой логики статусов."""
    
    def setUp(self):
        """Настройка тестов."""
        self.service = ProjectApplicationService()
    
    def test_calculate_initial_status_new_logic(self):
        """Тест новой логики определения начального статуса."""
        test_cases = [
            ('admin', 'approved'),
            ('cpds', 'approved'),
            ('department_validator', 'await_institute'),
            ('institute_validator', 'await_cpds'),
            ('user', 'await_department'),
            ('moderator', 'await_department'),
            ('unknown_role', 'await_department'),
        ]
        
        for user_role, expected_status in test_cases:
            with self.subTest(role=user_role):
                result = ProjectApplicationDomain.calculate_initial_status(user_role)
                self.assertEqual(result, expected_status,
                               f"Роль {user_role}: ожидался статус {expected_status}, получен {result}")
    
    def test_available_actions_with_new_statuses(self):
        """Тест доступных действий для новых статусов."""
        # Тестируем различные статусы с новыми правилами
        test_cases = [
            # (статус, роль, ожидаемый_результат)
            ('await_department', 'user', False),
            ('await_department', 'admin', True),
            ('await_department', 'cpds', True),
            ('await_department', 'department_validator', False),  # Без причастного подразделения
            ('await_department', 'institute_validator', False),  # Без причастного подразделения
            
            ('await_institute', 'user', False),
            ('await_institute', 'admin', True),
            ('await_institute', 'cpds', True),
            ('await_institute', 'department_validator', False),  # Неправильная роль для статуса
            ('await_institute', 'institute_validator', False),  # Без причастного подразделения
            
            ('await_cpds', 'user', False),
            ('await_cpds', 'admin', True),
            ('await_cpds', 'cpds', True),
            ('await_cpds', 'department_validator', False),  # Неправильная роль для статуса
            ('await_cpds', 'institute_validator', False),  # Неправильная роль для статуса
            
            ('approved', 'admin', False),  # Одобренные заявки не имеют действий
            ('rejected', 'admin', False),  # Отклоненные заявки не имеют действий
        ]
        
        for status_code, user_role, expected_has_actions in test_cases:
            with self.subTest(status=status_code, role=user_role):
                # Настраиваем моки
                mock_application = Mock()
                mock_application.status.code = status_code
                mock_user = Mock()
                mock_user.role.code = user_role
                mock_user.department = None  # Нет подразделения
                
                # Проверяем права
                has_actions = self.service._has_approve_reject_permissions(
                    mock_application,
                    mock_user,
                    status_code,
                    user_role
                )
                
                self.assertEqual(has_actions, expected_has_actions,
                               f"Статус {status_code}, роль {user_role}: ожидалось {expected_has_actions}, получено {has_actions}")
    
    def test_available_actions_with_involved_departments_new_logic(self):
        """Тест доступных действий с причастными подразделениями для новых статусов."""
        # Создаем мок подразделения
        mock_department = Mock()
        mock_department.id = 1
        
        # Создаем мок причастных подразделений
        mock_involved_departments = Mock()
        mock_involved_departments.filter.return_value.exists.return_value = True
        
        mock_application = Mock()
        mock_application.involved_departments.all.return_value = mock_involved_departments
        mock_user = Mock()
        mock_user.department = mock_department
        
        # Тестируем валидатора института с причастным подразделением для статуса await_institute
        has_actions = self.service._has_approve_reject_permissions(
            mock_application,
            mock_user,
            'await_institute',
            'institute_validator'
        )
        
        self.assertTrue(has_actions, "Валидатор института с причастным подразделением должен иметь права для статуса await_institute")
    
    def test_submit_application_with_new_status_logic(self):
        """Тест создания заявки с новой логикой статусов."""
        test_cases = [
            ('admin', 'approved'),  # Админ создает одобренную заявку
            ('cpds', 'approved'),   # CPDS создает одобренную заявку
            ('department_validator', 'await_institute'),  # Валидатор подразделения создает заявку в статусе await_institute
            ('institute_validator', 'await_cpds'),      # Валидатор института создает заявку в статусе await_cpds
            ('user', 'await_department'),               # Обычный пользователь создает заявку в статусе await_department
        ]
        
        for user_role, expected_final_status in test_cases:
            with self.subTest(role=user_role):
                # Проверяем логику определения статуса
                initial_status = ProjectApplicationDomain.calculate_initial_status(user_role)
                
                # Для новых ролей статус должен измениться с 'created' на финальный
                if user_role in ['admin', 'cpds', 'department_validator', 'institute_validator']:
                    self.assertNotEqual(initial_status, 'created', 
                                     f"Роль {user_role} не должна создавать заявки со статусом 'created'")
                    self.assertEqual(initial_status, expected_final_status,
                                   f"Роль {user_role}: ожидался статус {expected_final_status}, получен {initial_status}")
                else:
                    # Обычные пользователи создают заявки со статусом 'created', который затем меняется на 'await_department'
                    self.assertEqual(initial_status, 'await_department',
                                   f"Роль {user_role}: ожидался статус await_department, получен {initial_status}")
    
    def test_debug_new_status_flow(self):
        """Отладочный тест для нового потока статусов."""
        print("\n=== Отладка новой логики статусов ===")
        
        roles_to_test = ['admin', 'cpds', 'department_validator', 'institute_validator', 'user', 'moderator']
        
        for role in roles_to_test:
            status = ProjectApplicationDomain.calculate_initial_status(role)
            print(f"Роль: {role:20} -> Статус: {status}")
            
            # Проверяем, будут ли доступны действия для этого статуса
            if status in ['await_department', 'await_institute', 'await_cpds']:
                print(f"  [OK] Статус {status} поддерживает действия approve/reject")
            else:
                print(f"  [NO] Статус {status} НЕ поддерживает действия approve/reject")
        
        print("\n=== Резюме ===")
        print("• admin/cpds -> approved (сразу одобрены)")
        print("• department_validator -> await_institute (ожидает институт)")
        print("• institute_validator -> await_cpds (ожидает CPDS)")
        print("• остальные -> await_department (ожидает подразделения)")


if __name__ == '__main__':
    print("Запуск тестов новой логики статусов...")
    print("Проверяет обновленные бизнес-правила для определения статусов.")
    print()
    
    import unittest
    unittest.main(verbosity=2)

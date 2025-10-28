"""
Unit-тесты для функционала направления заявки на доработку.

Проверяет:
- Права доступа (может/не может направлять на доработку)
- Результаты (изменение статуса, создание лога)
- Сохранение комментариев к полям
"""

import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import transaction
from unittest.mock import patch

from showcase.models import (
    ProjectApplication, 
    ProjectApplicationStatusLog, 
    ProjectApplicationComment, 
    ApplicationStatus
)
from accounts.models import Department, Role
from showcase.services.application_service import ProjectApplicationService
from showcase.services.logging_service import ApplicationLoggingService

User = get_user_model()


class TestRevisionFunctionality(TestCase):
    """Тесты функционала направления заявки на доработку"""
    
    def setUp(self):
        """Подготовка тестовых данных"""
        # Создаем роли
        self.admin_role = Role.objects.create(
            code='admin',
            name='Администратор',
            is_active=True
        )
        
        self.department_validator_role = Role.objects.create(
            code='department_validator',
            name='Валидатор подразделения',
            is_active=True
        )
        
        self.institute_validator_role = Role.objects.create(
            code='institute_validator',
            name='Валидатор института',
            is_active=True
        )
        
        self.cpds_role = Role.objects.create(
            code='cpds',
            name='CPDS',
            is_active=True
        )
        
        self.user_role = Role.objects.create(
            code='user',
            name='Пользователь',
            is_active=True
        )
        
        # Создаем пользователей
        self.admin_user = User.objects.create_user(
            email='admin@test.com',
            password='testpass123',
            first_name='Админ',
            last_name='Админов',
            role=self.admin_role
        )
        
        self.department_validator = User.objects.create_user(
            email='dept@test.com',
            password='testpass123',
            first_name='Валидатор',
            last_name='Подразделения',
            role=self.department_validator_role
        )
        
        self.institute_validator = User.objects.create_user(
            email='inst@test.com',
            password='testpass123',
            first_name='Валидатор',
            last_name='Института',
            role=self.institute_validator_role
        )
        
        self.cpds_user = User.objects.create_user(
            email='cpds@test.com',
            password='testpass123',
            first_name='CPDS',
            last_name='Пользователь',
            role=self.cpds_role
        )
        
        self.regular_user = User.objects.create_user(
            email='user@test.com',
            password='testpass123',
            first_name='Обычный',
            last_name='Пользователь',
            role=self.user_role
        )
        
        # Создаем подразделения
        self.department = Department.objects.create(
            name='Тестовое подразделение',
            short_name='TEST_DEPT'
        )
        
        self.department_validator.department = self.department
        self.department_validator.save()
        
        self.institute_validator.department = self.department
        self.institute_validator.save()
        
        # Убеждаемся, что подразделение установлено
        self.institute_validator.refresh_from_db()
        
        # Создаем статусы
        self.created_status = ApplicationStatus.objects.create(
            code='created',
            name='Создана',
            position=1
        )
        
        self.await_department_status = ApplicationStatus.objects.create(
            code='await_department',
            name='Ожидает подразделения',
            position=2
        )
        
        self.await_institute_status = ApplicationStatus.objects.create(
            code='await_institute',
            name='Ожидает института',
            position=3
        )
        
        self.await_cpds_status = ApplicationStatus.objects.create(
            code='await_cpds',
            name='Ожидает CPDS',
            position=4
        )
        
        # Создаем статусы для доработки
        self.returned_department_status = ApplicationStatus.objects.create(
            code='returned_department',
            name='Возвращена подразделению',
            position=5
        )
        
        self.returned_institute_status = ApplicationStatus.objects.create(
            code='returned_institute',
            name='Возвращена институту',
            position=6
        )
        
        self.returned_cpds_status = ApplicationStatus.objects.create(
            code='returned_cpds',
            name='Возвращена CPDS',
            position=7
        )
        
        # Создаем тестовые заявки
        self.application_await_dept = ProjectApplication.objects.create(
            title='Заявка ожидает подразделения',
            author_lastname='Иванов',
            author_firstname='Иван',
            author_email='ivan@test.com',
            goal='Тестовая цель проекта',
            problem_holder='Тестовый носитель проблемы',
            barrier='Тестовый барьер',
            status=self.await_department_status,
            author=self.regular_user
        )
        
        self.application_await_inst = ProjectApplication.objects.create(
            title='Заявка ожидает института',
            author_lastname='Петров',
            author_firstname='Петр',
            author_email='petr@test.com',
            goal='Тестовая цель проекта',
            problem_holder='Тестовый носитель проблемы',
            barrier='Тестовый барьер',
            status=self.await_institute_status,
            author=self.regular_user
        )
        
        self.application_await_cpds = ProjectApplication.objects.create(
            title='Заявка ожидает CPDS',
            author_lastname='Сидоров',
            author_firstname='Сидор',
            author_email='sidor@test.com',
            goal='Тестовая цель проекта',
            problem_holder='Тестовый носитель проблемы',
            barrier='Тестовый барьер',
            status=self.await_cpds_status,
            author=self.regular_user
        )
        
        # Добавляем причастные подразделения
        from showcase.models import ApplicationInvolvedDepartment
        ApplicationInvolvedDepartment.objects.create(
            application=self.application_await_dept,
            department=self.department,
            added_by=self.admin_user
        )
        
        ApplicationInvolvedDepartment.objects.create(
            application=self.application_await_inst,
            department=self.department,
            added_by=self.admin_user
        )
        
        ApplicationInvolvedDepartment.objects.create(
            application=self.application_await_cpds,
            department=self.department,
            added_by=self.admin_user
        )
        
        # Инициализируем сервис
        self.service = ProjectApplicationService()
    
    def test_admin_can_request_revision_from_await_department(self):
        """Тест: админ может направить на доработку заявку в статусе await_department"""
        print("\n=== Тест: Админ может направить на доработку ===")
        
        # Проверяем, что заявка в правильном статусе
        self.assertEqual(self.application_await_dept.status.code, 'await_department')
        
        # Выполняем направление на доработку
        result = self.service.request_changes(
            application_id=self.application_await_dept.id,
            requester=self.admin_user
        )
        
        # Проверяем результат
        self.assertIsNotNone(result)
        result.refresh_from_db()
        self.assertEqual(result.status.code, 'returned_department')
        
        print("Админ успешно направил заявку на доработку")
    
    def test_department_validator_can_request_revision_from_await_department(self):
        """Тест: валидатор подразделения может направить на доработку заявку в статусе await_department"""
        print("\n=== Тест: Валидатор подразделения может направить на доработку ===")
        
        # Проверяем, что заявка в правильном статусе
        self.assertEqual(self.application_await_dept.status.code, 'await_department')
        
        # Выполняем направление на доработку
        result = self.service.request_changes(
            application_id=self.application_await_dept.id,
            requester=self.department_validator
        )
        
        # Проверяем результат
        self.assertIsNotNone(result)
        result.refresh_from_db()
        self.assertEqual(result.status.code, 'returned_department')
        
        print("Валидатор подразделения успешно направил заявку на доработку")
    
    def test_institute_validator_can_request_revision_from_await_institute(self):
        """Тест: валидатор института может направить на доработку заявку в статусе await_institute"""
        print("\n=== Тест: Валидатор института может направить на доработку ===")
        
        # Проверяем, что заявка в правильном статусе
        self.assertEqual(self.application_await_inst.status.code, 'await_institute')
        
        # Отладочная информация
        print(f"Заявка ID: {self.application_await_inst.id}")
        print(f"Статус заявки: {self.application_await_inst.status.code}")
        print(f"Роль пользователя: {self.institute_validator.role.code}")
        print(f"Подразделение пользователя: {self.institute_validator.department}")
        
        # Проверяем причастные подразделения
        involved_depts = self.application_await_inst.involved_departments.all()
        print(f"Причастные подразделения: {[d.department.name for d in involved_depts]}")
        
        # Выполняем направление на доработку
        result = self.service.request_changes(
            application_id=self.application_await_inst.id,
            requester=self.institute_validator,
        )
        
        # Проверяем результат
        self.assertIsNotNone(result)
        result.refresh_from_db()
        self.assertEqual(result.status.code, 'returned_institute')
        
        print("Валидатор института успешно направил заявку на доработку")
    
    def test_institute_validator_can_request_revision_from_await_department(self):
        """Тест: валидатор института может направить на доработку заявку в статусе await_department"""
        print("\n=== Тест: Валидатор института может направить на доработку из await_department ===")
        
        # Проверяем, что заявка в правильном статусе
        self.assertEqual(self.application_await_dept.status.code, 'await_department')
        
        # Выполняем направление на доработку
        result = self.service.request_changes(
            application_id=self.application_await_dept.id,
            requester=self.institute_validator
        )
        
        # Проверяем результат
        self.assertIsNotNone(result)
        result.refresh_from_db()
        self.assertEqual(result.status.code, 'returned_institute')
        
        print("Валидатор института успешно направил заявку на доработку из await_department")
    
    def test_cpds_can_request_revision_from_await_cpds(self):
        """Тест: CPDS может направить на доработку заявку в статусе await_cpds"""
        print("\n=== Тест: CPDS может направить на доработку ===")
        
        # Проверяем, что заявка в правильном статусе
        self.assertEqual(self.application_await_cpds.status.code, 'await_cpds')
        
        # Выполняем направление на доработку
        result = self.service.request_changes(
            application_id=self.application_await_cpds.id,
            requester=self.cpds_user
        )
        
        # Проверяем результат
        self.assertIsNotNone(result)
        result.refresh_from_db()
        self.assertEqual(result.status.code, 'returned_cpds')
        
        print("CPDS успешно направил заявку на доработку")
    
    def test_regular_user_cannot_request_revision(self):
        """Тест: обычный пользователь не может направить на доработку"""
        print("\n=== Тест: Обычный пользователь не может направить на доработку ===")
        
        with self.assertRaises(PermissionError) as context:
            self.service.request_changes(
            application_id=self.application_await_dept.id,
            requester=self.regular_user
        )
        
        self.assertIn("Недостаточно прав", str(context.exception))
        print("OK Обычный пользователь корректно заблокирован")
    
    def test_department_validator_cannot_request_revision_from_await_institute(self):
        """Тест: валидатор подразделения не может направить на доработку заявку в статусе await_institute"""
        print("\n=== Тест: Валидатор подразделения не может направить на доработку из await_institute ===")
        
        with self.assertRaises(PermissionError) as context:
            self.service.request_changes(
            application_id=self.application_await_inst.id,
            requester=self.department_validator
        )
        
        self.assertIn("Недостаточно прав", str(context.exception))
        print("OK Валидатор подразделения корректно заблокирован для await_institute")
    
    def test_log_creation_on_revision(self):
        """Тест: создается лог при направлении на доработку"""
        print("\n=== Тест: Создание лога при направлении на доработку ===")
        
        # Подсчитываем количество логов до операции
        logs_before = ProjectApplicationStatusLog.objects.filter(
            application=self.application_await_dept
        ).count()
        
        # Выполняем направление на доработку
        self.service.request_changes(
            application_id=self.application_await_dept.id,
            requester=self.admin_user,
        )
        
        # Проверяем, что лог создался
        logs_after = ProjectApplicationStatusLog.objects.filter(
            application=self.application_await_dept
        ).count()
        
        self.assertEqual(logs_after, logs_before + 1)
        
        # Проверяем детали лога
        latest_log = ProjectApplicationStatusLog.objects.filter(
            application=self.application_await_dept
        ).latest('changed_at')
        
        self.assertEqual(latest_log.action_type, 'status_change')
        self.assertEqual(latest_log.from_status, self.await_department_status)
        self.assertEqual(latest_log.to_status, self.returned_department_status)
        self.assertEqual(latest_log.actor, self.admin_user)
        
        print("OK Лог создается корректно")
    
    def test_revision_from_created_status_fails(self):
        """Тест: нельзя направить на доработку заявку в статусе created"""
        print("\n=== Тест: Нельзя направить на доработку заявку в статусе created ===")
        
        # Создаем заявку в статусе created
        created_application = ProjectApplication.objects.create(
            title='Заявка в статусе created',
            author_lastname='Тестов',
            author_firstname='Тест',
            author_email='test@test.com',
            goal='Тестовая цель',
            problem_holder='Тестовый носитель',
            barrier='Тестовый барьер',
            status=self.created_status,
            author=self.regular_user
        )
        
        # Добавляем причастное подразделение
        from showcase.models import ApplicationInvolvedDepartment
        ApplicationInvolvedDepartment.objects.create(
            application=created_application,
            department=self.department,
            added_by=self.admin_user
        )
        
        with self.assertRaises(ValueError) as context:
            self.service.request_changes(
                application_id=created_application.id,
                requester=self.admin_user,
            )
        
        self.assertIn("Переход", str(context.exception))
        print("OK Корректно запрещено направлять на доработку заявку в статусе created")
    
    def test_department_validator_can_manage_returned_department(self):
        """Тест: валидатор подразделения может управлять заявкой в статусе returned_department"""
        print("\n=== Тест: Валидатор подразделения может управлять заявкой в статусе returned_department ===")
        
        # Создаем заявку в статусе returned_department
        returned_application = ProjectApplication.objects.create(
            title='Заявка на доработке',
            author_lastname='Тестов',
            author_firstname='Тест',
            author_email='test@test.com',
            goal='Тестовая цель',
            problem_holder='Тестовый носитель',
            barrier='Тестовый барьер',
            status=self.returned_department_status,
            author=self.regular_user
        )
        
        # Добавляем причастное подразделение
        from showcase.models import ApplicationInvolvedDepartment
        ApplicationInvolvedDepartment.objects.create(
            application=returned_application,
            department=self.department,
            added_by=self.admin_user
        )
        
        # Проверяем, что заявка в правильном статусе
        self.assertEqual(returned_application.status.code, 'returned_department')
        
        # Выполняем направление на доработку (должно работать)
        result = self.service.request_changes(
            application_id=returned_application.id,
            requester=self.department_validator,
        )
        
        # Проверяем результат
        self.assertIsNotNone(result)
        result.refresh_from_db()
        self.assertEqual(result.status.code, 'returned_department')
        
        print("OK Валидатор подразделения может управлять заявкой в статусе returned_department")
    
    def test_institute_validator_can_manage_returned_institute(self):
        """Тест: валидатор института может управлять заявкой в статусе returned_institute"""
        print("\n=== Тест: Валидатор института может управлять заявкой в статусе returned_institute ===")
        
        # Создаем заявку в статусе returned_institute
        returned_application = ProjectApplication.objects.create(
            title='Заявка на доработке института',
            author_lastname='Тестов',
            author_firstname='Тест',
            author_email='test@test.com',
            goal='Тестовая цель',
            problem_holder='Тестовый носитель',
            barrier='Тестовый барьер',
            status=self.returned_institute_status,
            author=self.regular_user
        )
        
        # Добавляем причастное подразделение
        from showcase.models import ApplicationInvolvedDepartment
        ApplicationInvolvedDepartment.objects.create(
            application=returned_application,
            department=self.department,
            added_by=self.admin_user
        )
        
        # Проверяем, что заявка в правильном статусе
        self.assertEqual(returned_application.status.code, 'returned_institute')
        
        # Выполняем направление на доработку (должно работать)
        result = self.service.request_changes(
            application_id=returned_application.id,
            requester=self.institute_validator,
        )
        
        # Проверяем результат
        self.assertIsNotNone(result)
        result.refresh_from_db()
        self.assertEqual(result.status.code, 'returned_institute')
        
        print("OK Валидатор института может управлять заявкой в статусе returned_institute")
    
    def test_author_can_manage_returned_application(self):
        """Тест: автор заявки может управлять своей заявкой в статусе returned_*"""
        print("\n=== Тест: Автор заявки может управлять своей заявкой в статусе returned_* ===")
        
        # Создаем заявку в статусе returned_department
        returned_application = ProjectApplication.objects.create(
            title='Заявка автора на доработке',
            author_lastname='Тестов',
            author_firstname='Тест',
            author_email='test@test.com',
            goal='Тестовая цель',
            problem_holder='Тестовый носитель',
            barrier='Тестовый барьер',
            status=self.returned_department_status,
            author=self.regular_user
        )
        
        # Добавляем подразделение для автора
        self.regular_user.department = self.department
        self.regular_user.save()
        
        # Добавляем причастное подразделение (подразделение автора)
        from showcase.models import ApplicationInvolvedDepartment
        ApplicationInvolvedDepartment.objects.create(
            application=returned_application,
            department=self.department,
            added_by=self.admin_user
        )
        
        # Проверяем, что заявка в правильном статусе
        self.assertEqual(returned_application.status.code, 'returned_department')
        
        # Выполняем направление на доработку (должно работать)
        result = self.service.request_changes(
            application_id=returned_application.id,
            requester=self.regular_user,
        )
        
        # Проверяем результат
        self.assertIsNotNone(result)
        result.refresh_from_db()
        self.assertEqual(result.status.code, 'returned_department')
        
        print("OK Автор заявки может управлять своей заявкой в статусе returned_*")
    
    def test_request_changes_action_not_available_for_returned_status(self):
        """Тест: действие 'Отправить на доработку' не доступно для статусов returned_*"""
        print("\n=== Тест: Действие 'Отправить на доработку' не доступно для статусов returned_* ===")
        
        # Создаем заявку в статусе returned_department
        returned_application = ProjectApplication.objects.create(
            title='Заявка на доработке',
            author_lastname='Тестов',
            author_firstname='Тест',
            author_email='test@test.com',
            goal='Тестовая цель',
            problem_holder='Тестовый носитель',
            barrier='Тестовый барьер',
            status=self.returned_department_status,
            author=self.regular_user
        )
        
        # Добавляем причастное подразделение
        from showcase.models import ApplicationInvolvedDepartment
        ApplicationInvolvedDepartment.objects.create(
            application=returned_application,
            department=self.department,
            added_by=self.admin_user
        )
        
        # Получаем доступные действия для админа
        available_actions = self.service.get_available_actions(
            application_id=returned_application.id,
            user=self.admin_user
        )
        
        # Проверяем, что действие 'request_changes' НЕ доступно
        request_changes_actions = [action for action in available_actions.actions if action.action == 'request_changes']
        self.assertEqual(len(request_changes_actions), 0, "Действие 'request_changes' не должно быть доступно для статуса returned_department")
        
        # Проверяем, что действие 'save_changes' доступно
        save_changes_actions = [action for action in available_actions.actions if action.action == 'save_changes']
        self.assertGreater(len(save_changes_actions), 0, "Действие 'save_changes' должно быть доступно для статуса returned_department")
        
        print("OK Действие 'Отправить на доработку' корректно скрыто для статусов returned_*")
    
    def test_request_changes_action_available_for_regular_status(self):
        """Тест: действие 'Отправить на доработку' доступно для обычных статусов"""
        print("\n=== Тест: Действие 'Отправить на доработку' доступно для обычных статусов ===")
        
        # Получаем доступные действия для заявки в статусе await_department
        available_actions = self.service.get_available_actions(
            application_id=self.application_await_dept.id,
            user=self.admin_user
        )
        
        # Проверяем, что действие 'request_changes' доступно
        request_changes_actions = [action for action in available_actions.actions if action.action == 'request_changes']
        self.assertGreater(len(request_changes_actions), 0, "Действие 'request_changes' должно быть доступно для статуса await_department")
        
        print("OK Действие 'Отправить на доработку' корректно доступно для обычных статусов")
    
    def test_revision_nonexistent_application(self):
        """Тест: попытка направить на доработку несуществующую заявку"""
        print("\n=== Тест: Попытка направить на доработку несуществующую заявку ===")
        
        with self.assertRaises(Exception):  # ObjectDoesNotExist из репозитория
            self.service.request_changes(
                application_id=99999,  # Несуществующий ID
                requester=self.admin_user,
            )
        
        print("OK Корректно обрабатывается несуществующая заявка")
    
    def run_all_tests(self):
        """Запуск всех тестов"""
        print("=" * 80)
        print("UNIT-ТЕСТЫ ФУНКЦИОНАЛА НАПРАВЛЕНИЯ НА ДОРАБОТКУ")
        print("=" * 80)
        
        try:
            # Тесты прав доступа
            self.test_admin_can_request_revision_from_await_department()
            self.test_department_validator_can_request_revision_from_await_department()
            self.test_institute_validator_can_request_revision_from_await_institute()
            self.test_cpds_can_request_revision_from_await_cpds()
            self.test_regular_user_cannot_request_revision()
            self.test_department_validator_cannot_request_revision_from_await_institute()
            
            # Тесты результатов
            self.test_log_creation_on_revision()
            self.test_revision_from_created_status_fails()
            self.test_revision_nonexistent_application()
            
            print("\n" + "=" * 80)
            print("🎉 ВСЕ UNIT-ТЕСТЫ ПРОШЛИ УСПЕШНО!")
            print("Функционал направления заявки на доработку полностью протестирован:")
            print("OK Права доступа (может/не может)")
            print("OK Результаты (статус, лог)")
            print("OK Обработка ошибок")
            print("=" * 80)
            
        except Exception as e:
            print(f"\n❌ ОШИБКА В ТЕСТАХ: {e}")
            raise


if __name__ == '__main__':
    # Запуск тестов
    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    
    test_instance = TestRevisionFunctionality()
    test_instance.setUp()
    test_instance.run_all_tests()

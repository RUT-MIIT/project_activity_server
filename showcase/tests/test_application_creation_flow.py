"""
Тесты для новой логики создания заявок.

Проверяет последовательность: создание → логирование → причастные → статус → логирование.
"""

import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import Mock, patch

from showcase.services.application_service import ProjectApplicationService
from showcase.services.involved_service import InvolvedManagementService
from showcase.services.logging_service import ApplicationLoggingService
from showcase.dto.application import ProjectApplicationCreateDTO

User = get_user_model()


class TestApplicationCreationFlow(TestCase):
    """Тесты для нового процесса создания заявок."""
    
    def setUp(self):
        """Настройка тестов."""
        self.service = ProjectApplicationService()
        self.involved_service = InvolvedManagementService()
        self.logging_service = ApplicationLoggingService()
    
    def test_services_initialization(self):
        """Тест инициализации всех сервисов."""
        # Проверяем, что все сервисы инициализированы
        self.assertIsInstance(self.service.logging_service, ApplicationLoggingService)
        self.assertIsInstance(self.service.involved_service, InvolvedManagementService)
        self.assertIsInstance(self.involved_service, InvolvedManagementService)
        self.assertIsInstance(self.logging_service, ApplicationLoggingService)
    
    def test_involved_service_add_user_and_departments_validation(self):
        """Тест валидации входных данных для add_user_and_departments."""
        mock_application = Mock()
        mock_user = Mock()
        mock_actor = Mock()
        
        # Тест с None значениями
        with self.assertRaises(ValueError):
            self.involved_service.add_user_and_departments(
                application=None,
                user=mock_user,
                actor=mock_actor
            )
        
        with self.assertRaises(ValueError):
            self.involved_service.add_user_and_departments(
                application=mock_application,
                user=None,
                actor=mock_actor
            )
        
        with self.assertRaises(ValueError):
            self.involved_service.add_user_and_departments(
                application=mock_application,
                user=mock_user,
                actor=None
            )
    
    def test_logging_service_validation(self):
        """Тест валидации ApplicationLoggingService."""
        mock_application = Mock()
        mock_user = Mock()
        mock_status = Mock()
        
        # Тест log_status_change с None значениями
        with self.assertRaises(ValueError):
            self.logging_service.log_status_change(
                application=None,
                from_status=mock_status,
                to_status=mock_status,
                actor=mock_user
            )
        
        with self.assertRaises(ValueError):
            self.logging_service.log_status_change(
                application=mock_application,
                from_status=mock_status,
                to_status=None,
                actor=mock_user
            )
    
    @patch('showcase.services.application_service.ApplicationCapabilities.submit_application')
    @patch('showcase.services.application_service.ProjectApplicationDomain.should_require_consultation')
    @patch('showcase.services.application_service.ProjectApplicationRepository.create')
    @patch('showcase.services.application_service.ApplicationLoggingService.log_status_change')
    @patch('showcase.services.application_service.InvolvedManagementService.add_user_and_departments')
    @patch('showcase.services.application_service.ProjectApplicationDomain.calculate_initial_status')
    @patch('showcase.services.application_service.ApplicationStatus.objects.get')
    def test_submit_application_flow_mock(
        self,
        mock_status_get,
        mock_calculate_status,
        mock_add_involved,
        mock_log_status,
        mock_repo_create,
        mock_consultation,
        mock_validation
    ):
        """Тест полного процесса создания заявки с моками."""
        # Настройка моков
        mock_validation.return_value.is_valid = True
        mock_consultation.return_value = False
        mock_application = Mock()
        mock_application.status = Mock()
        mock_repo_create.return_value = mock_application
        mock_calculate_status.return_value = 'created'  # Статус не изменится
        
        # Создаем тестовые данные
        dto = ProjectApplicationCreateDTO.from_dict({
            'company': 'Test Company',
            'goal': 'Test goal'
        })
        user = Mock()
        user.role = Mock()
        user.role.code = 'user'
        
        # Выполняем метод
        result = self.service.submit_application(dto, user)
        
        # Проверяем, что все методы были вызваны
        mock_validation.assert_called_once()
        mock_consultation.assert_called_once()
        mock_repo_create.assert_called_once()
        mock_log_status.assert_called_once()
        mock_add_involved.assert_called_once()
        mock_calculate_status.assert_called_once()
        
        # Проверяем результат
        self.assertEqual(result, mock_application)
    
    @patch('showcase.services.application_service.ApplicationCapabilities.submit_application')
    @patch('showcase.services.application_service.ProjectApplicationDomain.should_require_consultation')
    @patch('showcase.services.application_service.ProjectApplicationRepository.create')
    @patch('showcase.services.application_service.ApplicationLoggingService.log_status_change')
    @patch('showcase.services.application_service.InvolvedManagementService.add_user_and_departments')
    @patch('showcase.services.application_service.ProjectApplicationDomain.calculate_initial_status')
    @patch('showcase.services.application_service.ApplicationStatus.objects.get')
    def test_submit_application_with_status_change_mock(
        self,
        mock_status_get,
        mock_calculate_status,
        mock_add_involved,
        mock_log_status,
        mock_repo_create,
        mock_consultation,
        mock_validation
    ):
        """Тест создания заявки с изменением статуса (admin -> approved)."""
        # Настройка моков
        mock_validation.return_value.is_valid = True
        mock_consultation.return_value = False
        mock_application = Mock()
        mock_application.status = Mock()
        mock_repo_create.return_value = mock_application
        mock_calculate_status.return_value = 'approved'  # Статус изменится
        mock_new_status = Mock()
        mock_status_get.return_value = mock_new_status
        
        # Создаем тестовые данные
        dto = ProjectApplicationCreateDTO.from_dict({
            'company': 'Test Company',
            'goal': 'Test goal'
        })
        user = Mock()
        user.role = Mock()
        user.role.code = 'admin'  # Админ создает заявку со статусом approved
        
        # Выполняем метод
        result = self.service.submit_application(dto, user)
        
        # Проверяем, что все методы были вызваны
        mock_validation.assert_called_once()
        mock_consultation.assert_called_once()
        mock_repo_create.assert_called_once()
        # Логирование должно быть вызвано дважды: создание + изменение статуса
        self.assertEqual(mock_log_status.call_count, 2)
        mock_add_involved.assert_called_once()
        mock_calculate_status.assert_called_once()
        mock_status_get.assert_called_once_with(code='approved')
        
        # Проверяем результат
        self.assertEqual(result, mock_application)


if __name__ == '__main__':
    print("Запуск тестов нового процесса создания заявок...")
    print("Примечание: Тесты используют моки для изоляции логики.")
    print()
    
    import unittest
    unittest.main(verbosity=2)


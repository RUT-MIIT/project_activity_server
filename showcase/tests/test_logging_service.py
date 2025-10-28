"""
Unit тесты для ApplicationLoggingService.

Тестирует валидацию входных данных и базовую функциональность сервиса.
"""

import pytest
from unittest.mock import Mock, patch
from django.test import TestCase
from django.contrib.auth import get_user_model

from showcase.services.logging_service import ApplicationLoggingService

User = get_user_model()


class TestApplicationLoggingService(TestCase):
    """Unit тесты для ApplicationLoggingService."""
    
    def setUp(self):
        """Настройка тестов."""
        self.logging_service = ApplicationLoggingService()
        
        # Мокаем модели
        self.mock_application = Mock()
        self.mock_user = Mock()
        self.mock_status = Mock()
        self.mock_department = Mock()
    
    def test_logging_service_initialization(self):
        """Тест инициализации сервиса."""
        self.assertIsInstance(self.logging_service, ApplicationLoggingService)
    
    def test_log_status_change_validation(self):
        """Тест валидации входных данных для log_status_change."""
        # Тест с None значениями
        with self.assertRaises(ValueError):
            self.logging_service.log_status_change(
                application=None,
                from_status=self.mock_status,
                to_status=self.mock_status,
                actor=self.mock_user
            )
        
        with self.assertRaises(ValueError):
            self.logging_service.log_status_change(
                application=self.mock_application,
                from_status=self.mock_status,
                to_status=None,
                actor=self.mock_user
            )
        
        with self.assertRaises(ValueError):
            self.logging_service.log_status_change(
                application=self.mock_application,
                from_status=self.mock_status,
                to_status=self.mock_status,
                actor=None
            )
    
    def test_log_involved_user_added_validation(self):
        """Тест валидации входных данных для log_involved_user_added."""
        with self.assertRaises(ValueError):
            self.logging_service.log_involved_user_added(
                application=None,
                user=self.mock_user,
                actor=self.mock_user
            )
        
        with self.assertRaises(ValueError):
            self.logging_service.log_involved_user_added(
                application=self.mock_application,
                user=None,
                actor=self.mock_user
            )
    
    def test_log_involved_department_added_validation(self):
        """Тест валидации входных данных для log_involved_department_added."""
        with self.assertRaises(ValueError):
            self.logging_service.log_involved_department_added(
                application=None,
                department=self.mock_department,
                actor=self.mock_user
            )
    
    def test_get_application_logs_validation(self):
        """Тест валидации входных данных для get_application_logs."""
        with self.assertRaises(ValueError):
            self.logging_service.get_application_logs(application=None)
    
    def test_get_logs_by_action_type_validation(self):
        """Тест валидации входных данных для get_logs_by_action_type."""
        with self.assertRaises(ValueError):
            self.logging_service.get_logs_by_action_type(
                application=None,
                action_type='status_change'
            )
        
        with self.assertRaises(ValueError):
            self.logging_service.get_logs_by_action_type(
                application=self.mock_application,
                action_type=''
            )
    
    def test_get_logs_by_actor_validation(self):
        """Тест валидации входных данных для get_logs_by_actor."""
        with self.assertRaises(ValueError):
            self.logging_service.get_logs_by_actor(
                application=None,
                actor=self.mock_user
            )
        
        with self.assertRaises(ValueError):
            self.logging_service.get_logs_by_actor(
                application=self.mock_application,
                actor=None
            )


"""
Тесты для обработки ошибок в зависимости от режима DEBUG.

Проверяет, что при DEBUG=True показывается текст ошибки,
а при DEBUG=False - общее сообщение.
"""

import pytest
from django.test import TestCase, override_settings
from unittest.mock import Mock, patch

from showcase.entities.ProjectApplication import get_error_message


class TestDebugErrorHandling(TestCase):
    """Тесты для обработки ошибок в зависимости от DEBUG."""
    
    def test_get_error_message_debug_true(self):
        """Тест получения сообщения об ошибке при DEBUG=True."""
        with override_settings(DEBUG=True):
            # Создаем тестовое исключение
            test_exception = ValueError("Тестовая ошибка для DEBUG=True")
            
            # Получаем сообщение об ошибке
            error_message = get_error_message(test_exception)
            
            # Проверяем, что возвращается текст ошибки
            self.assertEqual(error_message, "Тестовая ошибка для DEBUG=True")
    
    def test_get_error_message_debug_false(self):
        """Тест получения сообщения об ошибке при DEBUG=False."""
        with override_settings(DEBUG=False):
            # Создаем тестовое исключение
            test_exception = ValueError("Тестовая ошибка для DEBUG=False")
            
            # Получаем сообщение об ошибке
            error_message = get_error_message(test_exception)
            
            # Проверяем, что возвращается общее сообщение
            self.assertEqual(error_message, "Внутренняя ошибка сервера")
    
    def test_get_error_message_different_exceptions_debug_true(self):
        """Тест различных типов исключений при DEBUG=True."""
        with override_settings(DEBUG=True):
            test_cases = [
                (ValueError("Ошибка валидации"), "Ошибка валидации"),
                (PermissionError("Ошибка прав доступа"), "Ошибка прав доступа"),
                (KeyError("Ключ не найден"), "'Ключ не найден'"),
                (Exception("Общая ошибка"), "Общая ошибка"),
            ]
            
            for exception, expected_message in test_cases:
                with self.subTest(exception=type(exception).__name__):
                    error_message = get_error_message(exception)
                    self.assertEqual(error_message, expected_message)
    
    def test_get_error_message_different_exceptions_debug_false(self):
        """Тест различных типов исключений при DEBUG=False."""
        with override_settings(DEBUG=False):
            test_cases = [
                ValueError("Ошибка валидации"),
                PermissionError("Ошибка прав доступа"),
                KeyError("Ключ не найден"),
                Exception("Общая ошибка"),
            ]
            
            for exception in test_cases:
                with self.subTest(exception=type(exception).__name__):
                    error_message = get_error_message(exception)
                    self.assertEqual(error_message, "Внутренняя ошибка сервера")
    
    def test_get_error_message_empty_exception(self):
        """Тест обработки исключения без сообщения."""
        with override_settings(DEBUG=True):
            # Исключение без сообщения
            empty_exception = ValueError()
            error_message = get_error_message(empty_exception)
            
            # Проверяем, что возвращается пустая строка или имя исключения
            self.assertIsInstance(error_message, str)
    
    def test_debug_error_handling_integration(self):
        """Интеграционный тест обработки ошибок в ViewSet."""
        print("\n=== Интеграционный тест обработки ошибок ===")
        
        # Тест с DEBUG=True
        with override_settings(DEBUG=True):
            test_exception = ValueError("Тестовая ошибка в DEBUG режиме")
            error_message = get_error_message(test_exception)
            print(f"DEBUG=True: {error_message}")
            self.assertIn("Тестовая ошибка в DEBUG режиме", error_message)
        
        # Тест с DEBUG=False
        with override_settings(DEBUG=False):
            test_exception = ValueError("Тестовая ошибка в PRODUCTION режиме")
            error_message = get_error_message(test_exception)
            print(f"DEBUG=False: {error_message}")
            self.assertEqual(error_message, "Внутренняя ошибка сервера")
        
        print("[OK] Обработка ошибок работает корректно в зависимости от режима DEBUG")


if __name__ == '__main__':
    print("Запуск тестов обработки ошибок в зависимости от DEBUG...")
    print("Проверяет, что при DEBUG=True показывается текст ошибки.")
    print()
    
    import unittest
    unittest.main(verbosity=2)

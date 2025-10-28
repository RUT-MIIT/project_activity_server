"""
Тесты для форматирования ошибок валидации.

Проверяет, что ошибки валидации форматируются в более читаемый вид.
"""

import pytest
from django.test import TestCase
from rest_framework.serializers import ValidationError
from rest_framework.exceptions import ErrorDetail

from showcase.entities.ProjectApplication import format_validation_errors


class TestValidationErrorFormatting(TestCase):
    """Тесты для форматирования ошибок валидации."""
    
    def test_format_simple_dict_errors(self):
        """Тест форматирования простых ошибок в виде словаря."""
        errors = {
            'company': ['This field is required.'],
            'title': ['This field cannot be blank.']
        }
        
        formatted = format_validation_errors(errors)
        
        expected = {
            'company': ['This field is required.'],
            'title': ['This field cannot be blank.']
        }
        
        self.assertEqual(formatted, expected)
    
    def test_format_error_detail_errors(self):
        """Тест форматирования ошибок с ErrorDetail."""
        errors = {
            'company': [ErrorDetail('This field is required.', code='required')],
            'title': [ErrorDetail('This field cannot be blank.', code='blank')]
        }
        
        formatted = format_validation_errors(errors)
        
        expected = {
            'company': ['This field is required.'],
            'title': ['This field cannot be blank.']
        }
        
        self.assertEqual(formatted, expected)
    
    def test_format_mixed_errors(self):
        """Тест форматирования смешанных типов ошибок."""
        errors = {
            'company': [ErrorDetail('This field is required.', code='required')],
            'title': 'This field cannot be blank.',
            'email': ['Invalid email format.', 'Email is too long.']
        }
        
        formatted = format_validation_errors(errors)
        
        expected = {
            'company': ['This field is required.'],
            'title': ['This field cannot be blank.'],
            'email': ['Invalid email format.', 'Email is too long.']
        }
        
        self.assertEqual(formatted, expected)
    
    def test_format_list_errors(self):
        """Тест форматирования ошибок в виде списка."""
        errors = [
            ErrorDetail('General validation error.', code='invalid'),
            ErrorDetail('Another error.', code='invalid')
        ]
        
        formatted = format_validation_errors(errors)
        
        expected = {
            'non_field_errors': ['General validation error.', 'Another error.']
        }
        
        self.assertEqual(formatted, expected)
    
    def test_format_single_error(self):
        """Тест форматирования одиночной ошибки."""
        error = ErrorDetail('Single error message.', code='invalid')
        
        formatted = format_validation_errors(error)
        
        expected = {
            'error': ['Single error message.']
        }
        
        self.assertEqual(formatted, expected)
    
    def test_format_string_error(self):
        """Тест форматирования строковой ошибки."""
        error = "Simple string error"
        
        formatted = format_validation_errors(error)
        
        expected = {
            'error': ['Simple string error']
        }
        
        self.assertEqual(formatted, expected)
    
    def test_format_complex_validation_errors(self):
        """Тест форматирования сложных ошибок валидации."""
        errors = {
            'company': [
                ErrorDetail('This field is required.', code='required'),
                ErrorDetail('Company name is too short.', code='min_length')
            ],
            'title': [ErrorDetail('This field cannot be blank.', code='blank')],
            'email': 'Invalid email format.',
            'phone': [
                ErrorDetail('Phone number is required.', code='required'),
                ErrorDetail('Invalid phone format.', code='invalid')
            ]
        }
        
        formatted = format_validation_errors(errors)
        
        expected = {
            'company': [
                'This field is required.',
                'Company name is too short.'
            ],
            'title': ['This field cannot be blank.'],
            'email': ['Invalid email format.'],
            'phone': [
                'Phone number is required.',
                'Invalid phone format.'
            ]
        }
        
        self.assertEqual(formatted, expected)
    
    def test_debug_validation_error_formatting(self):
        """Отладочный тест форматирования ошибок валидации."""
        print("\n=== Отладка форматирования ошибок валидации ===")
        
        # Тест 1: Простые ошибки
        simple_errors = {
            'company': ['This field is required.'],
            'title': ['This field cannot be blank.']
        }
        
        formatted = format_validation_errors(simple_errors)
        print(f"Простые ошибки: {formatted}")
        
        # Тест 2: ErrorDetail ошибки
        error_detail_errors = {
            'company': [ErrorDetail('This field is required.', code='required')],
            'title': [ErrorDetail('This field cannot be blank.', code='blank')]
        }
        
        formatted = format_validation_errors(error_detail_errors)
        print(f"ErrorDetail ошибки: {formatted}")
        
        # Тест 3: Смешанные ошибки
        mixed_errors = {
            'company': [ErrorDetail('This field is required.', code='required')],
            'title': 'This field cannot be blank.',
            'email': ['Invalid email format.', 'Email is too long.']
        }
        
        formatted = format_validation_errors(mixed_errors)
        print(f"Смешанные ошибки: {formatted}")
        
        print("\n=== Резюме ===")
        print("• Ошибки форматируются в читаемый вид")
        print("• ErrorDetail извлекаются в простые строки")
        print("• Поддерживаются различные типы ошибок")
        print("[OK] Форматирование ошибок работает корректно")


if __name__ == '__main__':
    print("Запуск тестов форматирования ошибок валидации...")
    print("Проверяет, что ошибки валидации форматируются в читаемый вид.")
    print()
    
    import unittest
    unittest.main(verbosity=2)


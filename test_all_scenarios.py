#!/usr/bin/env python
"""
Тест для проверки всех возможных сценариев ошибок.
"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from rest_framework.exceptions import ErrorDetail
from showcase.entities.ProjectApplication import format_validation_errors

def test_all_scenarios():
    """Тест для проверки всех возможных сценариев ошибок."""
    print("=== Тест для проверки всех возможных сценариев ошибок ===")
    
    # Тест 1: Обычный словарь
    print("\n1. Тест обычного словаря:")
    errors_dict = {'company': 'This field is required.'}
    formatted = format_validation_errors(errors_dict)
    print(f"   Исходные ошибки: {errors_dict}")
    print(f"   Отформатированные: {formatted}")
    
    # Тест 2: Словарь с ErrorDetail
    print("\n2. Тест словаря с ErrorDetail:")
    errors_with_detail = {
        'company': [ErrorDetail('This field is required.', code='required')]
    }
    formatted = format_validation_errors(errors_with_detail)
    print(f"   Исходные ошибки: {errors_with_detail}")
    print(f"   Отформатированные: {formatted}")
    
    # Тест 3: ValueError с обычным словарем
    print("\n3. Тест ValueError с обычным словарем:")
    try:
        raise ValueError({'company': 'This field is required.'})
    except ValueError as e:
        formatted = format_validation_errors(e)
        print(f"   ValueError: {e}")
        print(f"   Отформатированные: {formatted}")
    
    # Тест 4: ValueError с ErrorDetail
    print("\n4. Тест ValueError с ErrorDetail:")
    try:
        raise ValueError({'company': [ErrorDetail('This field is required.', code='required')]})
    except ValueError as e:
        formatted = format_validation_errors(e)
        print(f"   ValueError: {e}")
        print(f"   Отформатированные: {formatted}")
    
    # Тест 5: Строковое представление
    print("\n5. Тест строкового представления:")
    error_string = "{'company': [ErrorDetail(string='This field is required.', code='required')]}"
    formatted = format_validation_errors(error_string)
    print(f"   Исходная строка: {error_string}")
    print(f"   Отформатированные: {formatted}")
    
    # Тест 6: Сложная строка
    print("\n6. Тест сложной строки:")
    complex_string = "{'company': [ErrorDetail(string='This field is required.', code='required')], 'title': [ErrorDetail(string='This field cannot be blank.', code='blank')]}"
    formatted = format_validation_errors(complex_string)
    print(f"   Исходная строка: {complex_string}")
    print(f"   Отформатированные: {formatted}")
    
    print("\n=== Тест завершен ===")

if __name__ == '__main__':
    test_all_scenarios()


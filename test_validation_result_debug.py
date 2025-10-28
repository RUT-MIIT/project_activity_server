#!/usr/bin/env python
"""
Тест для отладки ValidationResult и ValueError.
"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from showcase.dto.validation import ValidationResult
from showcase.entities.ProjectApplication import format_validation_errors

def test_validation_result_debug():
    """Тест для отладки ValidationResult и ValueError."""
    print("=== Тест для отладки ValidationResult и ValueError ===")
    
    # Тест 1: Создаем ValidationResult с ошибками
    print("\n1. Тест ValidationResult:")
    validation = ValidationResult()
    validation.add_error('company', 'This field is required.')
    validation.add_error('title', 'This field cannot be blank.')
    
    print(f"   validation.errors: {validation.errors}")
    print(f"   type(validation.errors): {type(validation.errors)}")
    print(f"   validation.is_valid: {validation.is_valid}")
    
    # Тест 2: Создаем ValueError с validation.errors
    print("\n2. Тест ValueError с validation.errors:")
    try:
        raise ValueError(validation.errors)
    except ValueError as e:
        print(f"   ValueError: {e}")
        print(f"   type(e): {type(e)}")
        print(f"   str(e): {str(e)}")
        print(f"   e.args: {e.args}")
        print(f"   type(e.args[0]): {type(e.args[0])}")
        
        # Тест 3: Форматируем ошибки
        print("\n3. Тест форматирования ошибок:")
        formatted = format_validation_errors(e)
        print(f"   formatted: {formatted}")
        
        # Проверяем результат
        if 'company' in formatted and 'title' in formatted:
            print("   [OK] Ошибки отформатированы корректно")
        else:
            print("   [NO] Ошибки не отформатированы")
    
    # Тест 4: Прямая передача словаря
    print("\n4. Тест прямой передачи словаря:")
    errors_dict = {'company': 'This field is required.', 'title': 'This field cannot be blank.'}
    formatted = format_validation_errors(errors_dict)
    print(f"   errors_dict: {errors_dict}")
    print(f"   formatted: {formatted}")
    
    # Проверяем результат
    if 'company' in formatted and 'title' in formatted:
        print("   [OK] Словарь отформатирован корректно")
    else:
        print("   [NO] Словарь не отформатирован")
    
    print("\n=== Тест завершен ===")

if __name__ == '__main__':
    test_validation_result_debug()


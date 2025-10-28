#!/usr/bin/env python
"""
Тест для симуляции реального сценария с ошибками валидации.
"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from rest_framework.exceptions import ErrorDetail
from showcase.entities.ProjectApplication import format_validation_errors

def test_real_scenario():
    """Тест для симуляции реального сценария."""
    print("=== Тест для симуляции реального сценария ===")
    
    # Тест 1: Симулируем ошибку, которую вы видите
    print("\n1. Тест ошибки, которую вы видите:")
    error_string = "{'company': [ErrorDetail(string='This field is required.', code='required')]}"
    
    formatted = format_validation_errors(error_string)
    print(f"   Исходная ошибка: {error_string}")
    print(f"   Отформатированная: {formatted}")
    
    # Проверяем результат
    if 'company' in formatted and isinstance(formatted['company'], list):
        print("   [OK] Ошибка отформатирована корректно")
    else:
        print("   [NO] Ошибка не отформатирована")
    
    # Тест 2: Симулируем ValueError с ErrorDetail
    print("\n2. Тест ValueError с ErrorDetail:")
    errors_with_detail = {
        'company': [ErrorDetail('This field is required.', code='required')]
    }
    
    try:
        raise ValueError(errors_with_detail)
    except ValueError as e:
        formatted = format_validation_errors(e)
        print(f"   ValueError: {e}")
        print(f"   Отформатированная: {formatted}")
        
        # Проверяем результат
        if 'company' in formatted and isinstance(formatted['company'], list):
            print("   [OK] ValueError с ErrorDetail отформатирован корректно")
        else:
            print("   [NO] ValueError с ErrorDetail не отформатирован")
    
    # Тест 3: Симулируем строковое представление ValueError
    print("\n3. Тест строкового представления ValueError:")
    try:
        raise ValueError(errors_with_detail)
    except ValueError as e:
        error_string = str(e)
        formatted = format_validation_errors(error_string)
        print(f"   str(ValueError): {error_string}")
        print(f"   Отформатированная: {formatted}")
        
        # Проверяем результат
        if 'company' in formatted and isinstance(formatted['company'], list):
            print("   [OK] Строковое представление ValueError отформатировано корректно")
        else:
            print("   [NO] Строковое представление ValueError не отформатировано")
    
    print("\n=== Тест завершен ===")

if __name__ == '__main__':
    test_real_scenario()


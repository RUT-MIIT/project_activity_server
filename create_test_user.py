#!/usr/bin/env python
"""
Создание тестового пользователя для проверки пагинации.
"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User, Role, Department
from django.contrib.auth.hashers import make_password

def create_test_user():
    """Создаем тестового пользователя"""
    
    # Создаем роль, если её нет
    role, created = Role.objects.get_or_create(
        code='user',
        defaults={
            'name': 'Пользователь',
            'is_active': True
        }
    )
    
    # Создаем отдел, если его нет
    department, created = Department.objects.get_or_create(
        name='Тестовый отдел',
        defaults={
            'short_name': 'TEST'
        }
    )
    
    # Создаем пользователя
    user, created = User.objects.get_or_create(
        email='test@example.com',
        defaults={
            'first_name': 'Тест',
            'last_name': 'Пользователь',
            'password': make_password('test123'),
            'role': role,
            'department': department,
            'is_active': True
        }
    )
    
    if created:
        print(f"Создан пользователь: {user.email}")
    else:
        print(f"Пользователь уже существует: {user.email}")
    
    print(f"Email: {user.email}")
    print(f"Пароль: test123")
    print(f"ID: {user.id}")

if __name__ == "__main__":
    create_test_user()

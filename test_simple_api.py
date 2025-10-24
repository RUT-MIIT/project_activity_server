#!/usr/bin/env python
"""
Простой тест API без пагинации.
"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User
from rest_framework.test import APIClient
from rest_framework import status

def test_simple_api():
    """Тестируем простой API без пагинации"""
    
    # Создаем тестового клиента
    client = APIClient()
    
    # Получаем пользователя
    user = User.objects.get(email='test@example.com')
    
    # Аутентифицируемся
    login_data = {
        'email': 'test@example.com',
        'password': 'test123'
    }
    
    # Логинимся
    response = client.post('/api/accounts/login/', login_data, format='json')
    print(f"Статус логина: {response.status_code}")
    
    if response.status_code == 200:
        token = response.data['access']
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Тестируем API без пагинации
        print("\nТестируем API без пагинации...")
        
        response = client.get('/api/showcase/project-applications/')
        print(f"Статус API: {response.status_code}")
        
        if response.status_code == 200:
            data = response.data
            print(f"Тип ответа: {type(data)}")
            print(f"Количество заявок: {len(data) if isinstance(data, list) else 'не список'}")
            print("API работает!")
        else:
            print(f"Ошибка API: {response.status_code}")
            print(f"Ответ: {response.data}")
    else:
        print(f"Ошибка аутентификации: {response.status_code}")
        print(f"Ответ: {response.data}")

if __name__ == "__main__":
    test_simple_api()

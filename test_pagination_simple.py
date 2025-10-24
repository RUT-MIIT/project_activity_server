#!/usr/bin/env python
"""
Простой тест пагинации без внешних зависимостей.
"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User
from showcase.services.application_service import ProjectApplicationService
from rest_framework.test import APIClient
from rest_framework import status

def test_pagination():
    """Тестируем пагинацию через Django test client"""
    
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
        
        # Тестируем пагинацию
        print("\nТестируем пагинацию...")
        
        # Первая страница
        response = client.get('/api/showcase/project-applications/?page=1')
        print(f"Статус первой страницы: {response.status_code}")
        
        if response.status_code == 200:
            data = response.data
            print(f"Тип ответа: {type(data)}")
            print(f"Содержимое ответа: {data}")
            
            if isinstance(data, dict) and 'results' in data:
                print("Пагинация работает!")
                print(f"Количество заявок на странице: {len(data['results'])}")
                print(f"Общее количество: {data.get('count', 'неизвестно')}")
                print(f"Следующая страница: {data.get('next', 'нет')}")
                print(f"Предыдущая страница: {data.get('previous', 'нет')}")
                
                # Тестируем вторую страницу
                if data.get('next'):
                    print("\nТестируем вторую страницу...")
                    response2 = client.get('/api/showcase/project-applications/?page=2')
                    print(f"Статус второй страницы: {response2.status_code}")
                    
                    if response2.status_code == 200:
                        data2 = response2.data
                        print(f"Количество заявок на второй странице: {len(data2['results'])}")
                        print("Вторая страница работает!")
                    else:
                        print(f"Ошибка второй страницы: {response2.status_code}")
            else:
                print("Пагинация не работает - возвращается обычный список")
                print(f"Количество заявок: {len(data) if isinstance(data, list) else 'не список'}")
        else:
            print(f"Ошибка API: {response.status_code}")
            print(f"Ответ: {response.data}")
    else:
        print(f"Ошибка аутентификации: {response.status_code}")
        print(f"Ответ: {response.data}")

if __name__ == "__main__":
    test_pagination()

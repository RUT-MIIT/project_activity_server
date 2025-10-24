#!/usr/bin/env python
"""
Простой тест для проверки пагинации API заявок.
"""

import requests
import json

# Базовый URL API
BASE_URL = "http://localhost:8000/api"

def test_pagination():
    """Тестируем пагинацию списка заявок"""
    
    # Сначала нужно получить токен аутентификации
    # Для тестирования используем существующего пользователя
    login_data = {
        "email": "test@example.com",  # email пользователя
        "password": "test123"  # пароль
    }
    
    try:
        # Получаем токен
        response = requests.post(f"{BASE_URL}/accounts/login/", json=login_data)
        if response.status_code != 200:
            print(f"Ошибка аутентификации: {response.status_code}")
            print(f"Ответ: {response.text}")
            return
        
        token_data = response.json()
        access_token = token_data.get('access')
        
        if not access_token:
            print("Не удалось получить токен доступа")
            return
        
        # Заголовки с токеном
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        # Тестируем пагинацию
        print("Тестируем пагинацию списка заявок...")
        
        # Первая страница
        response = requests.get(f"{BASE_URL}/project-applications/?page=1", headers=headers)
        print(f"Статус первой страницы: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Тип ответа: {type(data)}")
            
            if isinstance(data, dict) and 'results' in data:
                print("✅ Пагинация работает!")
                print(f"Количество заявок на странице: {len(data['results'])}")
                print(f"Общее количество: {data.get('count', 'неизвестно')}")
                print(f"Следующая страница: {data.get('next', 'нет')}")
                print(f"Предыдущая страница: {data.get('previous', 'нет')}")
            else:
                print("❌ Пагинация не работает - возвращается обычный список")
                print(f"Количество заявок: {len(data) if isinstance(data, list) else 'не список'}")
        else:
            print(f"❌ Ошибка API: {response.status_code}")
            print(f"Ответ: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Не удалось подключиться к серверу. Убедитесь, что сервер запущен на localhost:8000")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    test_pagination()

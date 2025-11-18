#!/usr/bin/env python
"""Проверка пользователя и создание нового с правильным паролем."""

import os

import django

# Настройка Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


from accounts.models import User


def check_and_fix_user():
    """Проверяем и исправляем пользователя"""
    try:
        user = User.objects.get(email="test@example.com")
        print(f"Пользователь найден: {user.email}")
        print(f"Активен: {user.is_active}")

        # Проверяем пароль
        if user.check_password("test123"):
            print("Пароль правильный")
        else:
            print("Пароль неправильный, устанавливаем новый")
            user.set_password("test123")
            user.save()
            print("Пароль обновлен")

    except User.DoesNotExist:
        print("Пользователь не найден, создаем нового")
        user = User.objects.create_user(
            email="test@example.com",
            password="test123",
            first_name="Тест",
            last_name="Пользователь",
        )
        print(f"Создан пользователь: {user.email}")


if __name__ == "__main__":
    check_and_fix_user()

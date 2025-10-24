#!/usr/bin/env python
"""
Создание тестовых заявок для проверки пагинации.
"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User
from showcase.models import ProjectApplication, ApplicationStatus, Institute
from showcase.services.application_service import ProjectApplicationService
from showcase.dto.application import ProjectApplicationCreateDTO

def create_test_applications():
    """Создаем тестовые заявки"""
    
    # Получаем пользователя
    user = User.objects.get(email='test@example.com')
    
    # Получаем статус
    status = ApplicationStatus.objects.first()
    if not status:
        print("Нет статусов в системе")
        return
    
    # Получаем институт
    institute = Institute.objects.first()
    if not institute:
        print("Нет институтов в системе")
        return
    
    # Создаем несколько заявок
    for i in range(25):  # Создаем 25 заявок для тестирования пагинации
        dto = ProjectApplicationCreateDTO(
            title=f"Тестовая заявка {i+1}",
            company=f"Компания {i+1}",
            author_lastname="Тестов",
            author_firstname="Пользователь",
            author_email="test@example.com",
            author_phone="+7-999-999-99-99",
            author_role="Тестер",
            author_division="Тестовый отдел",
            company_contacts="test@company.com",
            project_level="local",
            problem_holder="Тестовый держатель проблемы",
            goal="Тестовая цель",
            barrier="Тестовое препятствие",
            existing_solutions="Тестовые решения",
            context="Тестовый контекст",
            stakeholders="Тестовые заинтересованные стороны",
            recommended_tools="Тестовые инструменты",
            experts="Тестовые эксперты",
            additional_materials="Тестовые материалы",
            target_institutes=[institute.code] if institute else []
        )
        
        # Создаем заявку через сервис
        service = ProjectApplicationService()
        try:
            application, status_log = service.submit_application(dto, user)
            print(f"Создана заявка {i+1}: {application.title}")
        except Exception as e:
            print(f"Ошибка создания заявки {i+1}: {e}")

if __name__ == "__main__":
    create_test_applications()

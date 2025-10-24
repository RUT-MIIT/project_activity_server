"""
Общие фикстуры для тестов сервисов статусов.

Содержит создание справочных сущностей (статусы, институты), базовых ролей/пользователей
и минимальной заявки. Эти фикстуры переиспользуются в тестах каждого сервиса.
"""

import pytest
from django.contrib.auth import get_user_model

from showcase.models import ApplicationStatus, Institute, ProjectApplication
from accounts.models import Role, Department


User = get_user_model()


@pytest.fixture
def statuses(db):
    created, _ = ApplicationStatus.objects.get_or_create(
        code='created', defaults={'name': 'Создана', 'position': 1, 'is_active': True}
    )
    rejected, _ = ApplicationStatus.objects.get_or_create(
        code='rejected', defaults={'name': 'Отклонена', 'position': 99, 'is_active': True}
    )
    rejected_dept, _ = ApplicationStatus.objects.get_or_create(
        code='rejected_department', defaults={'name': 'Отклонена департаментом', 'position': 50, 'is_active': True}
    )
    rejected_inst, _ = ApplicationStatus.objects.get_or_create(
        code='rejected_institute', defaults={'name': 'Отклонена институтом', 'position': 51, 'is_active': True}
    )
    rejected_cpds, _ = ApplicationStatus.objects.get_or_create(
        code='rejected_cpds', defaults={'name': 'Отклонена ЦПДС', 'position': 52, 'is_active': True}
    )
    await_dept, _ = ApplicationStatus.objects.get_or_create(
        code='await_department', defaults={'name': 'Ожидает департамент', 'position': 10, 'is_active': True}
    )
    await_inst, _ = ApplicationStatus.objects.get_or_create(
        code='await_institute', defaults={'name': 'Ожидает институт', 'position': 20, 'is_active': True}
    )
    await_cpds, _ = ApplicationStatus.objects.get_or_create(
        code='await_cpds', defaults={'name': 'Ожидает ЦПДС', 'position': 30, 'is_active': True}
    )
    return {
        'created': created,
        'rejected': rejected,
        'rejected_department': rejected_dept,
        'rejected_institute': rejected_inst,
        'rejected_cpds': rejected_cpds,
        'await_department': await_dept,
        'await_institute': await_inst,
        'await_cpds': await_cpds,
    }


@pytest.fixture
def institute(db):
    inst, _ = Institute.objects.get_or_create(
        code='ti',
        defaults={'name': 'Тестовый институт', 'position': 1, 'is_active': True},
    )
    return inst


@pytest.fixture
def dept(db):
    dept, _ = Department.objects.get_or_create(
        name='Департамент 1',
        defaults={'short_name': 'D1'}
    )
    return dept


@pytest.fixture
def user_department_validator(db, dept):
    role, _ = Role.objects.get_or_create(
        code='department_validator',
        defaults={'name': 'Валидатор департамента', 'is_active': True},
    )
    user, _ = User.objects.get_or_create(
        email='dept@test.local',
        defaults={'first_name': 'Dept', 'last_name': 'Validator'},
    )
    user.role = role
    user.department = dept
    user.save()
    return user


@pytest.fixture
def user_mentor(db, dept):
    role, _ = Role.objects.get_or_create(
        code='mentor', defaults={'name': 'Ментор', 'is_active': True}
    )
    user, _ = User.objects.get_or_create(
        email='mentor@test.local',
        defaults={'first_name': 'Mentor', 'last_name': 'User'},
    )
    user.role = role
    user.department = dept
    user.save()
    return user


@pytest.fixture
def application(db, statuses, institute, user_department_validator):
    app = ProjectApplication.objects.create(
        author=user_department_validator,
        status=statuses['created'],
        author_firstname='Имя',
        author_lastname='Фамилия',
        author_email='a@b.c',
        author_phone='+100000000',
        company='Компания',
        company_contacts='contact@company',
    )
    app.target_institutes.add(institute)
    return app



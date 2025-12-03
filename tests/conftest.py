from itertools import count

from django.contrib.auth import get_user_model
import pytest

from accounts.models import Department, Role
from showcase.models import ApplicationStatus


@pytest.fixture
def user_model():
    """Возвращает класс модели пользователя для удобства."""
    return get_user_model()


@pytest.fixture
def roles(db):
    """Создаёт набор ролей, используемых в тестах.

    Возвращает dict: code -> Role
    """
    codes = [
        "user",
        "admin",
        "moderator",
        "cpds",
        "department_validator",
        "institute_validator",
        "mentor",
    ]
    roles_map = {}
    for code in codes:
        roles_map[code] = Role.objects.create(code=code, name=code)
    return roles_map


@pytest.fixture
def departments(db):
    """Создаёт иерархию подразделений: parent -> child."""
    parent = Department.objects.create(name="Parent Dept", short_name="PD")
    child = Department.objects.create(name="Child Dept", short_name="CD", parent=parent)
    return {"parent": parent, "child": child}


@pytest.fixture
def statuses(db):
    """Создаёт все необходимые статусы для сценариев сервисов."""
    codes = [
        ("created", 1),
        ("require_assignment", 2),
        ("await_department", 3),
        ("await_institute", 4),
        ("await_cpds", 5),
        ("returned_department", 6),
        ("returned_institute", 7),
        ("returned_cpds", 8),
        ("approved_department", 9),
        ("approved_institute", 10),
        ("approved", 11),
        ("rejected_department", 12),
        ("rejected_institute", 13),
        ("rejected_cpds", 14),
        ("rejected", 15),
    ]
    for code, pos in codes:
        ApplicationStatus.objects.get_or_create(
            code=code, defaults={"name": code, "position": pos}
        )
    return {s.code: s for s in ApplicationStatus.objects.all()}


@pytest.fixture
def make_user(db, user_model, roles, departments):
    """Фабрика пользователей: создаёт пользователя с заданной ролью и департаментом.

    Пример: user = make_user(role_code="department_validator", with_department=True)
    """
    seq = count(1)

    def _make(
        role_code: str = "user", with_department: bool = False, email: str | None = None
    ):
        department = departments["child"] if with_department else None
        role = roles[role_code]
        idx = next(seq)
        user = user_model.objects.create_user(
            email=email or f"u{idx}@example.com",
            password="pass",
            first_name="Ivan",
            last_name="Ivanov",
            role=role,
            department=department,
        )
        return user

    return _make

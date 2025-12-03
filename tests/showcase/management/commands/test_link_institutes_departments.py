from typing import Any

import pytest
from django.core.management import call_command

from accounts.models import Department
from showcase.models import Institute


@pytest.mark.django_db
def test_link_institutes_by_name_simple(db: Any) -> None:
    """Простейший сценарий: для каждого института есть одноимённое подразделение."""
    dep1 = Department.objects.create(name="Институт 1", short_name="I1")
    dep2 = Department.objects.create(name="Институт 2", short_name="I2")

    inst1 = Institute.objects.create(
        code="I1",
        name="Институт 1",
        position=1,
        is_active=True,
    )
    inst2 = Institute.objects.create(
        code="I2",
        name="Институт 2",
        position=2,
        is_active=True,
    )

    assert inst1.department is None
    assert inst2.department is None

    call_command("link_institutes_departments")

    inst1.refresh_from_db()
    inst2.refresh_from_db()

    assert inst1.department == dep1
    assert inst2.department == dep2


@pytest.mark.django_db
def test_link_institutes_without_matching_department(db: Any) -> None:
    """Институты без одноимённого подразделения остаются без связанного подразделения."""
    Department.objects.create(name="Стороннее подразделение", short_name="OTHER")

    inst = Institute.objects.create(
        code="NO_MATCH",
        name="Институт без соответствия",
        position=1,
        is_active=True,
    )

    call_command("link_institutes_departments")

    inst.refresh_from_db()
    assert inst.department is None

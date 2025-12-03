import os
from typing import Any

from django.core.management import call_command
import pandas as pd
import pytest

from accounts.models import Department
from showcase.models import Institute


@pytest.mark.django_db
def test_export_import_departments_roundtrip(tmp_path: Any) -> None:
    """Экспорт и последующий импорт подразделений восстанавливают данные."""
    parent = Department.objects.create(
        name="Родитель",
        short_name="PARENT",
        can_save_project_applications=True,
    )
    child = Department.objects.create(
        name="Дочернее",
        short_name="CHILD",
        parent=parent,
        can_save_project_applications=False,
    )

    file_path = tmp_path / "departments.xlsx"

    call_command(
        "sync_departments_institutes",
        "--mode",
        "export",
        "--entity",
        "departments",
        "--file",
        str(file_path),
    )

    # Удаляем все и импортируем обратно
    Department.objects.all().delete()
    assert Department.objects.count() == 0

    call_command(
        "sync_departments_institutes",
        "--mode",
        "import",
        "--entity",
        "departments",
        "--file",
        str(file_path),
    )

    assert Department.objects.count() == 2
    parent_db = Department.objects.get(name="Родитель")
    child_db = Department.objects.get(name="Дочернее")

    assert parent_db.short_name == "PARENT"
    assert parent_db.can_save_project_applications is True
    assert child_db.short_name == "CHILD"
    assert child_db.parent == parent_db


@pytest.mark.django_db
def test_import_departments_deletes_missing(tmp_path: Any) -> None:
    """Импорт подразделений удаляет те, которых нет в файле."""
    Department.objects.create(
        name="Останется",
        short_name="KEEP",
        can_save_project_applications=False,
    )
    Department.objects.create(
        name="Удалится",
        short_name="REMOVE",
        can_save_project_applications=False,
    )

    file_path = tmp_path / "departments.xlsx"
    df = pd.DataFrame(
        [
            {
                "name": "Останется",
                "short_name": "KEEP",
                "parent_name": None,
                "can_save_project_applications": False,
            }
        ]
    )
    df.to_excel(file_path, index=False)

    call_command(
        "sync_departments_institutes",
        "--mode",
        "import",
        "--entity",
        "departments",
        "--file",
        str(file_path),
    )

    names = set(Department.objects.values_list("name", flat=True))
    assert names == {"Останется"}


@pytest.mark.django_db
def test_export_import_institutes_roundtrip(tmp_path: Any) -> None:
    """Экспорт и последующий импорт институтов восстанавливают данные."""
    dep = Department.objects.create(
        name="Подразделение",
        short_name="DEP",
        can_save_project_applications=False,
    )
    inst1 = Institute.objects.create(
        code="I1",
        name="Институт 1",
        position=1,
        is_active=True,
        department=dep,
    )
    inst2 = Institute.objects.create(
        code="I2",
        name="Институт 2",
        position=2,
        is_active=False,
    )

    file_path = tmp_path / "institutes.xlsx"

    call_command(
        "sync_departments_institutes",
        "--mode",
        "export",
        "--entity",
        "institutes",
        "--file",
        str(file_path),
    )

    # Удаляем все и импортируем обратно
    Institute.objects.all().delete()
    assert Institute.objects.count() == 0

    call_command(
        "sync_departments_institutes",
        "--mode",
        "import",
        "--entity",
        "institutes",
        "--file",
        str(file_path),
    )

    assert Institute.objects.count() == 2
    inst1_db = Institute.objects.get(code="I1")
    inst2_db = Institute.objects.get(code="I2")

    assert inst1_db.name == "Институт 1"
    assert inst1_db.position == 1
    assert inst1_db.is_active is True
    assert inst1_db.department == dep

    assert inst2_db.name == "Институт 2"
    assert inst2_db.position == 2
    assert inst2_db.is_active is False
    assert inst2_db.department is None


@pytest.mark.django_db
def test_import_institutes_deletes_missing(tmp_path: Any) -> None:
    """Импорт институтов удаляет те, которых нет в файле."""
    Institute.objects.create(
        code="KEEP",
        name="Останется",
        position=1,
        is_active=True,
    )
    Institute.objects.create(
        code="REMOVE",
        name="Удалится",
        position=2,
        is_active=True,
    )

    file_path = tmp_path / "institutes.xlsx"
    df = pd.DataFrame(
        [
            {
                "code": "KEEP",
                "name": "Останется",
                "position": 1,
                "is_active": True,
                "department_name": None,
            }
        ]
    )
    df.to_excel(file_path, index=False)

    call_command(
        "sync_departments_institutes",
        "--mode",
        "import",
        "--entity",
        "institutes",
        "--file",
        str(file_path),
    )

    codes = set(Institute.objects.values_list("code", flat=True))
    assert codes == {"KEEP"}

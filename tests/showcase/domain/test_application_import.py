"""Тесты доменной логики импорта заявок из Excel."""

from __future__ import annotations

import pytest

from accounts.models import Department
from showcase.domain.application_import import (
    find_existing_imported_application,
    get_or_create_institute_tag,
)
from showcase.models import ProjectApplication, Tag


@pytest.mark.django_db
def test_find_existing_imported_application_matches_author_title_company(
    make_user, statuses
):
    """Повторный импорт находит заявку по автору, названию и заказчику."""
    author = make_user(role_code="institute_validator", with_department=True)
    application = ProjectApplication.objects.create(
        title="Птицелогистика",
        company='ООО "Черкизово"',
        author=author,
        status=statuses["await_cpds"],
        author_lastname=author.last_name,
        author_firstname=author.first_name,
        author_email=author.email,
    )

    found = find_existing_imported_application(
        author_id=author.id,
        title="  Птицелогистика ",
        company='ООО "Черкизово"',
    )

    assert found is not None
    assert found.id == application.id


@pytest.mark.django_db
def test_get_or_create_institute_tag_returns_base_tag(make_user):
    """Если есть базовый тег с таким именем, создавать институтский не нужно."""
    department = Department.objects.create(name="ИМТК", short_name="ИМТК")
    base_tag = Tag.objects.create(
        name="Логистика",
        category="Транспорт и логистика",
        is_base=True,
    )

    tag, created = get_or_create_institute_tag(
        "Логистика",
        department_id=department.id,
        institute_name="ИМТК",
    )

    assert created is False
    assert tag.id == base_tag.id


@pytest.mark.django_db
def test_get_or_create_institute_tag_creates_department_tag(make_user):
    """Отсутствующий тег создаётся как институтский и привязывается к подразделению."""
    department = Department.objects.create(name="ИМТК", short_name="ИМТК")

    tag, created = get_or_create_institute_tag(
        "Цифровизация",
        department_id=department.id,
        institute_name="ИМТК",
    )

    assert created is True
    assert tag.name == "Цифровизация"
    assert tag.category == "ИМТК"
    assert tag.is_base is False
    assert list(tag.departments.values_list("id", flat=True)) == [department.id]

    same_tag, created_again = get_or_create_institute_tag(
        "Цифровизация",
        department_id=department.id,
        institute_name="ИМТК",
    )
    assert created_again is False
    assert same_tag.id == tag.id

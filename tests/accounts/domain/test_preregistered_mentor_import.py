"""Тесты domain-логики импорта предрегистрации наставников."""

from __future__ import annotations

import pytest

from accounts.domain.preregistered_mentor_import import (
    build_preregistered_mentor_import_row,
    build_user_name_indexes,
    find_user_by_full_name,
    normalize_user_name,
    resolve_department_by_name,
)
from accounts.models import Department


@pytest.mark.django_db
class TestPreRegisteredMentorImport:
    def test_build_row_parses_full_name(self) -> None:
        row = build_preregistered_mentor_import_row(
            department_name="Кафедра информатики",
            full_name="Иванов Иван Иванович",
            personnel_number="1347607",
        )

        assert row.last_name == "Иванов"
        assert row.first_name == "Иван"
        assert row.middle_name == "Иванович"
        assert row.personnel_number == "1347607"
        assert row.department_name == "Кафедра информатики"

    def test_build_row_requires_personnel_number(self) -> None:
        with pytest.raises(ValueError, match="табельный номер"):
            build_preregistered_mentor_import_row(
                department_name="Кафедра",
                full_name="Иванов Иван",
                personnel_number="",
            )

    def test_resolve_department_by_name_case_insensitive(self) -> None:
        Department.objects.create(name="Кафедра информатики", short_name="КИ")

        department = resolve_department_by_name("кафедра информатики")

        assert department is not None
        assert department.name == "Кафедра информатики"

    def test_resolve_department_returns_none_when_missing(self) -> None:
        assert resolve_department_by_name("Несуществующая кафедра") is None

    def test_find_user_by_full_name(self, make_user, roles) -> None:
        user = make_user(
            role_code="mentor",
            email="mentor@example.com",
        )
        user.first_name = "Иван"
        user.last_name = "Иванов"
        user.middle_name = "Иванович"
        user.save(update_fields=["first_name", "last_name", "middle_name"])
        by_name, by_tokens = build_user_name_indexes([user])

        found = find_user_by_full_name(
            "Иванов Иван Иванович",
            by_name=by_name,
            by_tokens=by_tokens,
        )

        assert found is not None
        assert found.pk == user.pk

    def test_normalize_user_name_ignores_case_and_yo(self) -> None:
        assert normalize_user_name("Ёлкин Пётр") == normalize_user_name("елкин петр")

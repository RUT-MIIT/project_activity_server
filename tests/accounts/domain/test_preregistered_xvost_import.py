"""Тесты доменной логики импорта предрегистрации из prerigistered_xvost.xlsx."""

from __future__ import annotations

import pytest

from accounts.domain.preregistered_xvost_import import (
    build_preregistered_xvost_import_row,
    resolve_department_by_institute_label,
    resolve_institute_code,
)
from showcase.models import Institute


class TestResolveInstituteCode:
    def test_resolves_short_russian_name(self) -> None:
        assert resolve_institute_code("ИСТИ") == "ISTI"

    def test_resolves_vish_alias(self) -> None:
        assert resolve_institute_code("ВИШ") == "VISH"

    def test_accepts_latin_code(self) -> None:
        assert resolve_institute_code("IMTK") == "IMTK"

    def test_unknown_institute_raises(self) -> None:
        with pytest.raises(ValueError, match="Неизвестный институт"):
            resolve_institute_code("UNKNOWN")

    def test_empty_institute_raises(self) -> None:
        with pytest.raises(ValueError, match="Пустой институт"):
            resolve_institute_code("")


class TestBuildPreregisteredXvostImportRow:
    def test_builds_row(self) -> None:
        row = build_preregistered_xvost_import_row(
            last_name="Иванов",
            first_name="Иван",
            middle_name="Иванович",
            personnel_number="2026-ИСТИ-1",
        )
        assert row.last_name == "Иванов"
        assert row.first_name == "Иван"
        assert row.middle_name == "Иванович"
        assert row.personnel_number == "2026-ИСТИ-1"
        assert row.department_name == ""

    def test_empty_personnel_number_raises(self) -> None:
        with pytest.raises(ValueError, match="Пустой табельный номер"):
            build_preregistered_xvost_import_row(
                last_name="Иванов",
                first_name="Иван",
                middle_name="",
                personnel_number="",
            )

    def test_empty_last_name_raises(self) -> None:
        with pytest.raises(ValueError, match="Пустая фамилия"):
            build_preregistered_xvost_import_row(
                last_name="",
                first_name="Иван",
                middle_name="",
                personnel_number="2026-ИСТИ-1",
            )


@pytest.mark.django_db
class TestResolveDepartmentByInstituteLabel:
    def test_returns_department_for_institute(self, departments) -> None:
        Institute.objects.create(
            code="ISTI",
            name="ИСТИ",
            position=1,
            department=departments["parent"],
        )

        department = resolve_department_by_institute_label("ИСТИ")

        assert department == departments["parent"]

    def test_returns_none_when_institute_has_no_department(self) -> None:
        Institute.objects.create(
            code="VISH",
            name="ВИШ",
            position=2,
        )

        department = resolve_department_by_institute_label("ВИШ")

        assert department is None

    def test_raises_when_institute_missing_in_db(self) -> None:
        with pytest.raises(ValueError, match="не найден в БД"):
            resolve_department_by_institute_label("ИСТИ")

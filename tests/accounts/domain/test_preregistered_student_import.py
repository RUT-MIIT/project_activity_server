"""Тесты доменной логики импорта предрегистрации студентов."""

from __future__ import annotations

import pytest

from accounts.domain.preregistered_student_import import (
    build_preregistered_student_import_row,
    last_names_match,
    normalize_snils,
    parse_full_name,
)


class TestPreRegisteredStudentImportDomain:
    def test_parse_full_name_with_middle_name(self) -> None:
        last_name, first_name, middle_name = parse_full_name("Иванов Иван Иванович")
        assert last_name == "Иванов"
        assert first_name == "Иван"
        assert middle_name == "Иванович"

    def test_parse_full_name_without_middle_name(self) -> None:
        last_name, first_name, middle_name = parse_full_name("Петров Пётр")
        assert last_name == "Петров"
        assert first_name == "Пётр"
        assert middle_name == ""

    def test_normalize_snils_from_formatted_value(self) -> None:
        assert normalize_snils("184-573-628 06") == "18457362806"

    def test_normalize_snils_empty(self) -> None:
        assert normalize_snils("") == ""

    def test_normalize_snils_invalid_length(self) -> None:
        with pytest.raises(ValueError, match="Некорректный СНИЛС"):
            normalize_snils("123")

    def test_build_import_row(self) -> None:
        row = build_preregistered_student_import_row(
            full_name="Студент 1",
            student_card="25011884",
            snils="18457362806",
            personnel_number="1335090",
            permanent_group_code="АМБ-2025-11",
        )
        assert row.last_name == "Студент"
        assert row.first_name == "1"
        assert row.student_card == "25011884"
        assert row.snils == "18457362806"
        assert row.personnel_number == "1335090"
        assert row.group_code == "АМБ-2025-11"

    def test_last_names_match_case_insensitive(self) -> None:
        assert last_names_match("Иванов", "иванов") is True

    def test_last_names_match_trims_whitespace(self) -> None:
        assert last_names_match("  Иванов  ", "Иванов") is True

    def test_last_names_match_different_names(self) -> None:
        assert last_names_match("Иванов", "Петров") is False

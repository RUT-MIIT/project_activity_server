"""Тесты доменной логики импорта предрегистрации студентов."""

from __future__ import annotations

import pytest

from accounts.domain.preregistered_student_import import (
    PreRegisteredStudentImportRow,
    StudyGroupLookup,
    StudyGroupRef,
    build_preregistered_student_import_row,
    last_names_match,
    normalize_snils,
    parse_full_name,
    resolve_study_group_for_student,
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


class TestStudyGroupResolver:
    @pytest.fixture
    def lookup(self) -> StudyGroupLookup:
        return StudyGroupLookup.from_groups(
            [
                StudyGroupRef(
                    pk=1,
                    code="ТПВг-2024-41",
                    name="ТПВг-341",
                    external_group_id="ext-341",
                ),
                StudyGroupRef(
                    pk=2,
                    code="ТПВг-2023-99",
                    name="ТПВг-241",
                    external_group_id="ext-241",
                ),
            ]
        )

    def test_resolve_by_external_group_id(self, lookup: StudyGroupLookup) -> None:
        row = PreRegisteredStudentImportRow(
            last_name="Иванов",
            first_name="Иван",
            middle_name="",
            student_card="1",
            snils="",
            personnel_number="1",
            group_code="ТПВг-2024-41",
            teaching_group_name="ТПВг-241",
            external_group_id="ext-241",
            course_from_file="2",
        )
        result = resolve_study_group_for_student(
            row,
            lookup,
            current_year=2026,
            semester="autumn",
        )
        assert result.group is not None
        assert result.group.pk == 2

    def test_resolve_convergent_by_code(self, lookup: StudyGroupLookup) -> None:
        row = PreRegisteredStudentImportRow(
            last_name="Иванов",
            first_name="Иван",
            middle_name="",
            student_card="1",
            snils="",
            personnel_number="1",
            group_code="ТПВг-2024-41",
            teaching_group_name="ТПВг-341",
            external_group_id="",
            course_from_file="3",
        )
        result = resolve_study_group_for_student(
            row,
            lookup,
            current_year=2026,
            semester="autumn",
        )
        assert result.group is not None
        assert result.group.pk == 1

    def test_resolve_lagging_by_name(self, lookup: StudyGroupLookup) -> None:
        row = PreRegisteredStudentImportRow(
            last_name="Петров",
            first_name="Пётр",
            middle_name="",
            student_card="2",
            snils="",
            personnel_number="2",
            group_code="ТПВг-2024-41",
            teaching_group_name="ТПВг-241",
            external_group_id="",
            course_from_file="2",
        )
        result = resolve_study_group_for_student(
            row,
            lookup,
            current_year=2026,
            semester="autumn",
        )
        assert result.group is not None
        assert result.group.pk == 2

    def test_resolve_ambiguous_name(self) -> None:
        lookup = StudyGroupLookup.from_groups(
            [
                StudyGroupRef(pk=1, code="A", name="Одинаковая", external_group_id=""),
                StudyGroupRef(pk=2, code="B", name="Одинаковая", external_group_id=""),
            ]
        )
        row = PreRegisteredStudentImportRow(
            last_name="Петров",
            first_name="Пётр",
            middle_name="",
            student_card="2",
            snils="",
            personnel_number="2",
            group_code="X-2020-01",
            teaching_group_name="Одинаковая",
            external_group_id="",
            course_from_file="1",
        )
        result = resolve_study_group_for_student(
            row,
            lookup,
            current_year=2026,
            semester="autumn",
        )
        assert result.group is None
        assert result.reason is not None
        assert "неоднозначное" in result.reason

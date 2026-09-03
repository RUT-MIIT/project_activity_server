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
            external_group_id="197175",
        )
        assert row.last_name == "Студент"
        assert row.first_name == "1"
        assert row.student_card == "25011884"
        assert row.snils == "18457362806"
        assert row.personnel_number == "1335090"
        assert row.group_code == "АМБ-2025-11"
        assert row.external_group_id == "197175"

    def test_build_import_row_requires_external_group_id(self) -> None:
        with pytest.raises(ValueError, match="Пустой ID группы"):
            build_preregistered_student_import_row(
                full_name="Студент 1",
                student_card="25011884",
                snils="",
                personnel_number="1335090",
                permanent_group_code="АМБ-2025-11",
            )

    def test_build_import_row_remaps_merged_external_group_id(self) -> None:
        row = build_preregistered_student_import_row(
            full_name="Иванов Иван",
            student_card="25000001",
            snils="",
            personnel_number="100",
            permanent_group_code="ТСТ-2023-42",
            teaching_group_name="ТСТ-442",
            external_group_id=193902.0,
        )
        assert row.external_group_id == "193901"

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
        result = resolve_study_group_for_student(row, lookup)
        assert result.group is not None
        assert result.group.pk == 2

    def test_resolve_ended_group(self, lookup: StudyGroupLookup) -> None:
        lookup = StudyGroupLookup.from_groups(
            [
                StudyGroupRef(
                    pk=3,
                    code="X",
                    name="X-211",
                    external_group_id="ended-1",
                    is_end=True,
                )
            ]
        )
        row = PreRegisteredStudentImportRow(
            last_name="Иванов",
            first_name="Иван",
            middle_name="",
            student_card="1",
            snils="",
            personnel_number="1",
            group_code="X-2025-11",
            teaching_group_name="X-211",
            external_group_id="ended-1",
            course_from_file="2",
        )
        result = resolve_study_group_for_student(row, lookup)
        assert result.group is None
        assert result.reason is not None
        assert "завершила обучение" in result.reason

    def test_resolve_remapped_tst_442_uses_tst_441_group(self) -> None:
        lookup = StudyGroupLookup.from_groups(
            [
                StudyGroupRef(
                    pk=441,
                    code="ТСТ-2023-41",
                    name="ТСТ-441",
                    external_group_id="193901",
                ),
            ]
        )
        row = build_preregistered_student_import_row(
            full_name="Петров Пётр",
            student_card="2",
            snils="",
            personnel_number="2",
            permanent_group_code="ТСТ-2023-42",
            teaching_group_name="ТСТ-442",
            external_group_id="193902",
            course_from_file="4",
        )
        assert row.external_group_id == "193901"
        result = resolve_study_group_for_student(row, lookup)
        assert result.group is not None
        assert result.group.pk == 441
        assert result.group.name == "ТСТ-441"

    def test_resolve_gorachev_path_by_tki_241_id(self) -> None:
        lookup = StudyGroupLookup.from_groups(
            [
                StudyGroupRef(
                    pk=722,
                    code="ТКИ-2024-41",
                    name="ТКИ-241",
                    external_group_id="193722",
                ),
                StudyGroupRef(
                    pk=714,
                    code="ТКИ-2024-41",
                    name="ТКИ-341",
                    external_group_id="193714",
                ),
            ]
        )
        row = build_preregistered_student_import_row(
            full_name="Горячев Денис",
            student_card="25002390",
            snils="",
            personnel_number="1330764",
            permanent_group_code="ТКИ-2024-41",
            teaching_group_name="ТКИ-241",
            external_group_id="193722",
            course_from_file=2,
        )
        result = resolve_study_group_for_student(row, lookup)
        assert result.group is not None
        assert result.group.pk == 722
        assert result.group.external_group_id == "193722"

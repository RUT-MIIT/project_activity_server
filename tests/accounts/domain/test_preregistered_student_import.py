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

    def test_build_import_row_overrides_group_by_personnel_number(self) -> None:
        row = build_preregistered_student_import_row(
            full_name="Зеленин Роман Дмитриевич",
            student_card="24101428",
            snils="",
            personnel_number="1293713",
            permanent_group_code="СЖД-2025-42",
            teaching_group_name="СЖД-242",
            external_group_id="193685",
        )
        assert row.external_group_id == "193611"

    def test_build_import_row_overrides_akimochkin_to_szhd_241(self) -> None:
        row = build_preregistered_student_import_row(
            full_name="Акимочкин Артур Оганесович",
            student_card="24101844",
            snils="",
            personnel_number="1302227",
            permanent_group_code="СЖД-2025-42",
            teaching_group_name="СТП-242",
            external_group_id="193685",
        )
        assert row.external_group_id == "193611"

    def test_build_import_row_overrides_firsanova_to_umb_211(self) -> None:
        row = build_preregistered_student_import_row(
            full_name="Фирсанова Мария Павловна",
            student_card="25012448",
            snils="",
            personnel_number="1333226",
            permanent_group_code="ОМНк-2025-12-1",
            teaching_group_name="ОМНк-212",
            external_group_id="208102",
        )
        assert row.external_group_id == "210487"

    def test_build_import_row_overrides_golubev_to_utn_211(self) -> None:
        row = build_preregistered_student_import_row(
            full_name="Голубев Дмитрий Алексеевич",
            student_card="23000684",
            snils="",
            personnel_number="1224376",
            permanent_group_code="УВВ-2024-11",
            teaching_group_name="УВВ-311",
            external_group_id="177868",
        )
        assert row.external_group_id == "194698"

    def test_build_import_row_overrides_vavilin_to_smt_341(self) -> None:
        row = build_preregistered_student_import_row(
            full_name="Вавилин Константин Станиславович",
            student_card="24101931",
            snils="",
            personnel_number="1292128",
            permanent_group_code="СЖД-2024-41",
            teaching_group_name="СЖД-341",
            external_group_id="193600",
        )
        assert row.external_group_id == "194336"

    def test_build_import_row_overrides_bulaeva_to_omkk_311(self) -> None:
        row = build_preregistered_student_import_row(
            full_name="Булаева Анастасия Олеговна",
            student_card="24105355",
            snils="16473327881",
            personnel_number="1289627",
            permanent_group_code="ОМКк-2024-12",
            teaching_group_name="ОМКк-312",
            external_group_id="194430",
        )
        assert row.external_group_id == "182576"

    def test_build_import_row_overrides_molchanov_to_smt_441(self) -> None:
        row = build_preregistered_student_import_row(
            full_name="Молчанов Владимир Денисович",
            student_card="23005015",
            snils="18786597463",
            personnel_number="1246216",
            permanent_group_code="СЖД-2023-43",
            teaching_group_name="СЖД-443",
            external_group_id="193598",
        )
        assert row.external_group_id == "194335"

    def test_build_import_row_overrides_shebarshin_to_tpe_241(self) -> None:
        row = build_preregistered_student_import_row(
            full_name="Шебаршин Никита Андреевич",
            student_card="25005260",
            snils="19532328986",
            personnel_number="1330633",
            permanent_group_code="ТПЛ-2025-41",
            teaching_group_name="ТПЛ-241",
            external_group_id="193797",
        )
        assert row.external_group_id == "193851"

    def test_build_import_row_overrides_compound_name_santana(self) -> None:
        row = build_preregistered_student_import_row(
            full_name="Сантана Фернандес Ральди Энрике",
            student_card="22000448",
            snils="",
            personnel_number="1158617",
            permanent_group_code="ТСА-2021-41",
            teaching_group_name="ТСА-541",
            external_group_id="193863",
        )
        assert row.last_name == "Сантана Фернандес"
        assert row.first_name == "Ральди Энрике"
        assert row.middle_name == ""

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

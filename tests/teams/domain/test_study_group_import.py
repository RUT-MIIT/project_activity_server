"""Тесты доменной логики импорта учебных групп из контингента."""

from __future__ import annotations

from teams.domain.study_group_import import (
    ContingentRowForExternalIds,
    build_group_import_row,
    collect_external_ids_for_group,
    is_convergent_contingent_row,
    is_skipped_permanent_group,
    map_teaching_group_name_for_lookup,
    parse_course_from_teaching_group_name,
    resolve_study_group_display_name,
)


class TestStudyGroupExternalIdsDomain:
    def test_parse_course_from_teaching_group_name(self) -> None:
        assert parse_course_from_teaching_group_name("ТПВг-341") == 3
        assert parse_course_from_teaching_group_name("АМБ-211") == 2

    def test_parse_course_from_teaching_group_name_invalid(self) -> None:
        assert parse_course_from_teaching_group_name("") is None
        assert parse_course_from_teaching_group_name("invalid") is None

    def test_is_convergent_contingent_row_matching(self) -> None:
        assert is_convergent_contingent_row(
            "АМБ-2025-11",
            "АМБ-211",
            2,
            current_year=2026,
            semester="autumn",
        )

    def test_is_convergent_contingent_row_lagging(self) -> None:
        assert not is_convergent_contingent_row(
            "ТПВг-2024-41",
            "ТПВг-241",
            2,
            current_year=2026,
            semester="autumn",
        )

    def test_is_convergent_contingent_row_empty_teaching_group(self) -> None:
        assert is_convergent_contingent_row(
            "АМБ-2025-11",
            "",
            2,
            current_year=2026,
            semester="autumn",
        )

    def test_collect_external_ids_for_group_success(self) -> None:
        rows = [
            ContingentRowForExternalIds(
                teaching_group_name="АМБ-211",
                course_from_file="2",
                external_group_id="197175",
                external_permanent_group_id="309371",
            ),
            ContingentRowForExternalIds(
                teaching_group_name="АМБ-211",
                course_from_file="2",
                external_group_id="197175",
                external_permanent_group_id="309371",
            ),
        ]
        result = collect_external_ids_for_group(
            rows,
            permanent_code="АМБ-2025-11",
            current_year=2026,
            semester="autumn",
        )
        assert result.ids is not None
        assert result.ids.external_group_id == "197175"
        assert result.ids.external_permanent_group_id == "309371"

    def test_collect_external_ids_for_group_conflict(self) -> None:
        rows = [
            ContingentRowForExternalIds(
                teaching_group_name="АМБ-211",
                course_from_file="2",
                external_group_id="111",
                external_permanent_group_id="309371",
            ),
            ContingentRowForExternalIds(
                teaching_group_name="АМБ-211",
                course_from_file="2",
                external_group_id="222",
                external_permanent_group_id="309371",
            ),
        ]
        result = collect_external_ids_for_group(
            rows,
            permanent_code="АМБ-2025-11",
            current_year=2026,
            semester="autumn",
        )
        assert result.ids is None
        assert result.conflict_reason is not None
        assert "конфликт" in result.conflict_reason

    def test_collect_external_ids_ignores_lagging_rows(self) -> None:
        rows = [
            ContingentRowForExternalIds(
                teaching_group_name="ТПВг-241",
                course_from_file="2",
                external_group_id="999",
                external_permanent_group_id="888",
            ),
            ContingentRowForExternalIds(
                teaching_group_name="ТПВг-341",
                course_from_file="3",
                external_group_id="197175",
                external_permanent_group_id="309371",
            ),
        ]
        result = collect_external_ids_for_group(
            rows,
            permanent_code="ТПВг-2024-41",
            current_year=2026,
            semester="autumn",
        )
        assert result.ids is not None
        assert result.ids.external_group_id == "197175"


class TestStudyGroupImportOverrides:
    def test_is_skipped_permanent_group(self, monkeypatch) -> None:
        monkeypatch.setattr(
            "teams.domain.study_group_import.SKIPPED_PERMANENT_GROUP_CODES",
            frozenset({"SKIP-2024-01"}),
        )
        assert is_skipped_permanent_group("SKIP-2024-01")
        assert not is_skipped_permanent_group("АМБ-2025-11")

    def test_resolve_study_group_display_name_by_calculated_name(
        self, monkeypatch
    ) -> None:
        monkeypatch.setattr(
            "teams.domain.study_group_import.STUDY_GROUP_NAME_OVERRIDES",
            {"АМБ-211": "АМБ-211А"},
        )
        monkeypatch.setattr(
            "teams.domain.study_group_import.STUDY_GROUP_NAME_OVERRIDES_BY_CODE",
            {},
        )
        assert (
            resolve_study_group_display_name(
                calculated_name="АМБ-211",
                permanent_group_code="АМБ-2025-11",
            )
            == "АМБ-211А"
        )

    def test_resolve_study_group_display_name_by_code(self, monkeypatch) -> None:
        monkeypatch.setattr(
            "teams.domain.study_group_import.STUDY_GROUP_NAME_OVERRIDES",
            {"АМБ-211": "АМБ-211А"},
        )
        monkeypatch.setattr(
            "teams.domain.study_group_import.STUDY_GROUP_NAME_OVERRIDES_BY_CODE",
            {"АМБ-2025-11": "АМБ-211Б"},
        )
        assert (
            resolve_study_group_display_name(
                calculated_name="АМБ-211",
                permanent_group_code="АМБ-2025-11",
            )
            == "АМБ-211Б"
        )

    def test_map_teaching_group_name_for_lookup(self, monkeypatch) -> None:
        monkeypatch.setattr(
            "teams.domain.study_group_import.STUDY_GROUP_NAME_OVERRIDES",
            {"ТПВг-241": "ТПВг-241А"},
        )
        assert map_teaching_group_name_for_lookup("ТПВг-241") == "ТПВг-241А"

    def test_build_group_import_row_applies_name_override(self, monkeypatch) -> None:
        monkeypatch.setattr(
            "teams.domain.study_group_import.STUDY_GROUP_NAME_OVERRIDES_BY_CODE",
            {"АМБ-2025-11": "АМБ-211Н"},
        )
        row = build_group_import_row(
            permanent_group_code="АМБ-2025-11",
            institute_name="Академия гражданской авиации",
            direction_code="25.03.03",
            direction_name="Аэронавигация",
            direction_level="бакалавриат",
            profile="Профиль",
            form="очная",
            current_year=2026,
            semester="autumn",
        )
        assert row.name == "АМБ-211Н"

    def test_apply_group_abbrev_rename_ebp_to_ept(self) -> None:
        assert (
            resolve_study_group_display_name(
                calculated_name="ЭБП-211",
                permanent_group_code="ЭБП-2025-11",
            )
            == "ЭПТ-211"
        )
        assert map_teaching_group_name_for_lookup("ЭБП-311") == "ЭПТ-311"

    def test_is_skipped_permanent_group_by_prefix(self) -> None:
        assert is_skipped_permanent_group("ТУП-2024-11")
        assert not is_skipped_permanent_group("ТПВг-2024-41")

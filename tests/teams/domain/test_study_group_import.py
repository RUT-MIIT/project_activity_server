"""Тесты доменной логики импорта учебных групп из контингента."""

from __future__ import annotations

from teams.domain.study_group_import import (
    ContingentRowForExternalIds,
    collect_external_ids_for_group,
    is_convergent_contingent_row,
    parse_course_from_teaching_group_name,
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

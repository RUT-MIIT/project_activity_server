"""Тесты парсинга импорта преподавателей проектной деятельности."""

from __future__ import annotations

import pytest

from teams.domain.project_teacher_import import (
    build_project_teacher_import_row,
    parse_semester_code,
)


class TestParseSemesterCode:
    def test_first_semester(self) -> None:
        assert parse_semester_code("1-й семестр 2026-2027") == "26-27-1"

    def test_second_semester(self) -> None:
        assert parse_semester_code("2-й семестр 2025-2026") == "25-26-2"

    def test_invalid_format_raises(self) -> None:
        with pytest.raises(ValueError, match="Некорректный формат семестра"):
            parse_semester_code("Осень 26/27")

    def test_empty_raises(self) -> None:
        with pytest.raises(ValueError, match="Пустое название семестра"):
            parse_semester_code("")


class TestBuildProjectTeacherImportRow:
    def test_builds_valid_row(self) -> None:
        row = build_project_teacher_import_row(
            group_name="ВГТ-111",
            semester_label="1-й семестр 2026-2027",
            mentor_full_name="Иванов Иван Иванович",
            external_teacher_id="1054855",
            external_group_id="215959",
            mentor_short_name="Иванов И.И.",
            lesson_count=2,
            import_status="найдено",
            pd_user_id=13,
        )

        assert row.group_name == "ВГТ-111"
        assert row.semester_code == "26-27-1"
        assert row.external_teacher_id == "1054855"
        assert row.external_group_id == "215959"
        assert row.lesson_count == 2
        assert row.pd_user_id == 13

    def test_requires_teacher_id(self) -> None:
        with pytest.raises(ValueError, match="Пустой ID преподавателя"):
            build_project_teacher_import_row(
                group_name="ВГТ-111",
                semester_label="1-й семестр 2026-2027",
                mentor_full_name="Иванов Иван Иванович",
                external_teacher_id="",
            )

    def test_normalizes_float_teacher_id(self) -> None:
        row = build_project_teacher_import_row(
            group_name="ВГТ-111",
            semester_label="1-й семестр 2026-2027",
            mentor_full_name="Иванов Иван Иванович",
            external_teacher_id="1054855.0",
        )
        assert row.external_teacher_id == "1054855"

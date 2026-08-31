"""Тесты команды import_project_teachers_from_excel."""

from __future__ import annotations

from io import StringIO
from pathlib import Path
from typing import Any

from django.core.management import call_command
from django.core.management.base import CommandError
import pandas as pd
import pytest

from accounts.models import Semester
from teams.models import (
    Direction,
    StudyGroup,
    StudyGroupProjectTeacher,
    StudyGroupSemester,
)

COLUMNS = [
    "Институт",
    "Аббр. института",
    "Курс",
    "Специальность",
    "Аббр. специальности",
    "Группа",
    "ID группы",
    "Семестр",
    "Преподаватель (ФИО)",
    "Преподаватель (кратко)",
    "ID преподавателя",
    "Кол-во пар",
    "Статус",
    "В системе PD",
    "ID в PD",
    "Email в PD",
]


def _write_sample_excel(path: Path, rows: list[list[Any]]) -> None:
    """Создаёт минимальный Excel для тестов импорта."""
    path.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame([COLUMNS] + rows)
    df.to_excel(path, index=False, header=False)


@pytest.fixture
def semester(db) -> Semester:
    return Semester.objects.create(
        code="26-27-1",
        name="Осень 26/27",
        position=1,
    )


@pytest.fixture
def study_group(direction, institute) -> StudyGroup:
    return StudyGroup.objects.create(
        name="ВГТ-111",
        code="ВГТ-2025-11",
        direction=direction,
        institute=institute,
    )


@pytest.fixture
def direction(db) -> Direction:
    return Direction.objects.create(
        code="26.05.06",
        name="Эксплуатация судов",
        level=Direction.Level.SPECIALITET,
    )


@pytest.fixture
def sample_excel_file(tmp_path: Path) -> Path:
    path = tmp_path / "project_teachers.xlsx"
    return path


def _base_row(
    *,
    group_name: str = "ВГТ-111",
    mentor_full_name: str = "Иванов Иван Иванович",
    mentor_short_name: str = "Иванов И.И.",
    external_teacher_id: int = 1054855,
    pd_user_id: int | str = "",
    in_pd: str = "нет",
) -> list[Any]:
    return [
        "Академия водного транспорта",
        "АВТ",
        1,
        "Специальность",
        "ВГТ",
        group_name,
        215959,
        "1-й семестр 2026-2027",
        mentor_full_name,
        mentor_short_name,
        external_teacher_id,
        2,
        "найдено",
        in_pd,
        pd_user_id,
        "ivanov@example.com" if in_pd == "да" else "",
    ]


@pytest.mark.django_db
class TestImportProjectTeachersFromExcel:
    def test_import_creates_and_syncs_mentor(
        self,
        sample_excel_file: Path,
        semester: Semester,
        study_group: StudyGroup,
        roles,
        make_user,
    ) -> None:
        mentor = make_user(role_code="mentor", with_department=True)
        mentor.first_name = "Иван"
        mentor.last_name = "Иванов"
        mentor.middle_name = "Иванович"
        mentor.save(update_fields=["first_name", "last_name", "middle_name"])

        _write_sample_excel(
            sample_excel_file,
            [
                _base_row(
                    pd_user_id=mentor.pk,
                    in_pd="да",
                ),
                _base_row(
                    mentor_full_name="Петров Пётр Петрович",
                    mentor_short_name="Петров П.П.",
                    external_teacher_id=1054856,
                ),
                [
                    "Академия водного транспорта",
                    "АВТ",
                    1,
                    "Специальность",
                    "ВГТ",
                    "ВГТ-999",
                    999999,
                    "1-й семестр 2026-2027",
                    "",
                    "",
                    "",
                    0,
                    "нет занятий",
                    "",
                    "",
                    "",
                ],
            ],
        )

        out = StringIO()
        call_command(
            "import_project_teachers_from_excel",
            f"--file={sample_excel_file}",
            stdout=out,
        )

        assert StudyGroupProjectTeacher.objects.count() == 2
        first = StudyGroupProjectTeacher.objects.get(external_teacher_id="1054855")
        assert first.tutor_id == mentor.pk
        assert first.mentor_full_name == "Иванов Иван Иванович"
        assert first.lesson_count == 2

        second = StudyGroupProjectTeacher.objects.get(external_teacher_id="1054856")
        assert second.tutor_id is None

        enrollment = StudyGroupSemester.objects.get(
            study_group=study_group,
            semester=semester,
        )
        assert list(enrollment.mentors.values_list("id", flat=True)) == [mentor.pk]

    def test_import_is_idempotent_and_updates_fio(
        self,
        sample_excel_file: Path,
        semester: Semester,
        study_group: StudyGroup,
        roles,
        make_user,
    ) -> None:
        mentor = make_user(role_code="mentor", with_department=True)
        mentor.first_name = "Иван"
        mentor.last_name = "Иванов"
        mentor.middle_name = "Иванович"
        mentor.save(update_fields=["first_name", "last_name", "middle_name"])

        _write_sample_excel(
            sample_excel_file,
            [
                _base_row(
                    pd_user_id=mentor.pk,
                    in_pd="да",
                ),
            ],
        )

        call_command(
            "import_project_teachers_from_excel",
            f"--file={sample_excel_file}",
            stdout=StringIO(),
        )
        assert StudyGroupProjectTeacher.objects.count() == 1

        _write_sample_excel(
            sample_excel_file,
            [
                _base_row(
                    mentor_full_name="Иванов Иван Петрович",
                    mentor_short_name="Иванов И.П.",
                    pd_user_id=mentor.pk,
                    in_pd="да",
                ),
            ],
        )

        out = StringIO()
        call_command(
            "import_project_teachers_from_excel",
            f"--file={sample_excel_file}",
            stdout=out,
        )

        assert StudyGroupProjectTeacher.objects.count() == 1
        record = StudyGroupProjectTeacher.objects.get(external_teacher_id="1054855")
        assert record.mentor_full_name == "Иванов Иван Петрович"
        assert record.lesson_count == 2
        assert "обновлено 1" in out.getvalue()

    def test_missing_group_is_logged_and_skipped(
        self,
        tmp_path: Path,
        semester: Semester,
        study_group: StudyGroup,
    ) -> None:
        path = tmp_path / "missing_group.xlsx"
        _write_sample_excel(
            path,
            [
                [
                    "Академия водного транспорта",
                    "АВТ",
                    1,
                    "Специальность",
                    "ВГТ",
                    "НЕТ-ТАКОЙ",
                    1,
                    "1-й семестр 2026-2027",
                    "Иванов Иван Иванович",
                    "Иванов И.И.",
                    1054855,
                    1,
                    "найдено",
                    "нет",
                    "",
                    "",
                ],
            ],
        )

        out = StringIO()
        call_command(
            "import_project_teachers_from_excel",
            f"--file={path}",
            stdout=out,
        )

        assert StudyGroupProjectTeacher.objects.count() == 0
        output = out.getvalue()
        assert "группа «НЕТ-ТАКОЙ» не найдена" in output
        assert "групп не найдено 1" in output

    def test_missing_required_columns_raises(
        self,
        tmp_path: Path,
    ) -> None:
        path = tmp_path / "bad.xlsx"
        pd.DataFrame([["Группа"], ["ВГТ-111"]]).to_excel(
            path, index=False, header=False
        )

        with pytest.raises(CommandError, match="обязательные колонки"):
            call_command(
                "import_project_teachers_from_excel",
                f"--file={path}",
                stdout=StringIO(),
            )

    def test_missing_file_raises(self, tmp_path: Path) -> None:
        with pytest.raises(CommandError, match="Файл не найден"):
            call_command(
                "import_project_teachers_from_excel",
                f"--file={tmp_path / 'missing.xlsx'}",
                stdout=StringIO(),
            )

"""Тесты команды import_preregistered_mentors."""

from __future__ import annotations

from io import StringIO
from pathlib import Path
from typing import Any

from django.core.management import call_command
from django.core.management.base import CommandError
import pandas as pd
import pytest

from accounts.models import Department, PreRegisteredStudent

MENTOR_COLUMNS = [
    "Подразделение",
    "ФИО",
    "Должность",
    "Дата рождения",
    "Вид приема",
    "Ставка",
    "Планируемая дата увольнения",
    "Приказ о приеме на работу",
    "Дата последнего ПК",
    "Количество лет с последнего ПК",
    "ID Подразделения",
    "ID Должности",
    "ID Человека",
    "ID Вида приема",
    "ID Параграфа приказа о приеме на работу",
]


def _write_sample_teachers(path: Path, rows: list[list[Any]]) -> None:
    """Создаёт минимальный отчёт преподавателей для тестов."""
    path.parent.mkdir(parents=True, exist_ok=True)
    title_row = ["Заголовок отчёта"] + [""] * (len(MENTOR_COLUMNS) - 1)
    header_row = MENTOR_COLUMNS
    df = pd.DataFrame([title_row, header_row] + rows)
    df.to_excel(path, index=False, header=False)


@pytest.fixture
def sample_teachers_file(tmp_path: Path) -> Path:
    path = tmp_path / "teachers.xls"
    _write_sample_teachers(
        path,
        [
            [
                "Кафедра информатики",
                "Иванов Иван Иванович",
                "доцент",
                "1980-01-01",
                "штатный",
                "1",
                "",
                "приказ",
                "2020-01-01",
                "5",
                "100",
                "10",
                "900001",
                "1",
                "1",
            ],
            [
                "Кафедра информатики",
                "Петров Пётр Петрович",
                "профессор",
                "1975-01-01",
                "штатный",
                "1",
                "",
                "приказ",
                "2019-01-01",
                "6",
                "100",
                "11",
                "900002",
                "1",
                "2",
            ],
        ],
    )
    return path


@pytest.mark.django_db
class TestImportPreRegisteredMentors:
    def test_import_creates_mentor_preregistrations(
        self, sample_teachers_file: Path
    ) -> None:
        Department.objects.create(name="Кафедра информатики", short_name="КИ")

        call_command(
            "import_preregistered_mentors",
            file=str(sample_teachers_file),
            non_interactive=True,
        )

        mentors = PreRegisteredStudent.objects.filter(role_id="mentor").order_by(
            "personnel_number"
        )
        assert mentors.count() == 2
        first = mentors.first()
        assert first is not None
        assert first.personnel_number == "900001"
        assert first.department is not None
        assert first.department.name == "Кафедра информатики"
        assert first.group_id is None
        assert first.student_card == ""

    def test_import_links_existing_user_without_changing_role(
        self,
        sample_teachers_file: Path,
        roles: dict[str, Any],
        make_user,
    ) -> None:
        Department.objects.create(name="Кафедра информатики", short_name="КИ")
        user = make_user(
            role_code="institute_validator",
            email="ivanov@example.com",
        )
        user.first_name = "Иван"
        user.last_name = "Иванов"
        user.middle_name = "Иванович"
        user.save(update_fields=["first_name", "last_name", "middle_name"])

        call_command(
            "import_preregistered_mentors",
            file=str(sample_teachers_file),
            non_interactive=True,
        )

        pre_registered = PreRegisteredStudent.objects.get(personnel_number="900001")
        assert pre_registered.user_id == user.pk
        user.refresh_from_db()
        assert user.role_id == "institute_validator"

    def test_import_logs_missing_department(self, sample_teachers_file: Path) -> None:
        out = StringIO()

        call_command(
            "import_preregistered_mentors",
            file=str(sample_teachers_file),
            non_interactive=True,
            stdout=out,
        )

        pre_registered = PreRegisteredStudent.objects.get(personnel_number="900001")
        assert pre_registered.department_id is None
        assert "не найдено в БД" in out.getvalue()

    def test_import_skips_link_on_department_conflict_in_non_interactive_mode(
        self,
        sample_teachers_file: Path,
        roles: dict[str, Any],
        make_user,
        departments,
    ) -> None:
        import_dept = Department.objects.create(
            name="Кафедра информатики", short_name="КИ"
        )
        other_dept = Department.objects.create(name="Другая кафедра", short_name="ДК")
        user = make_user(
            role_code="mentor",
            email="ivanov@example.com",
            with_department=True,
        )
        user.first_name = "Иван"
        user.last_name = "Иванов"
        user.middle_name = "Иванович"
        user.first_name = "Иван"
        user.last_name = "Иванов"
        user.middle_name = "Иванович"
        user.save(update_fields=["first_name", "last_name", "middle_name"])
        user.department = other_dept
        user.save(update_fields=["department"])

        call_command(
            "import_preregistered_mentors",
            file=str(sample_teachers_file),
            non_interactive=True,
        )

        pre_registered = PreRegisteredStudent.objects.get(personnel_number="900001")
        assert pre_registered.department_id == import_dept.pk
        assert pre_registered.user_id is None

    def test_import_is_idempotent(self, sample_teachers_file: Path) -> None:
        Department.objects.create(name="Кафедра информатики", short_name="КИ")

        call_command(
            "import_preregistered_mentors",
            file=str(sample_teachers_file),
            non_interactive=True,
        )
        call_command(
            "import_preregistered_mentors",
            file=str(sample_teachers_file),
            non_interactive=True,
        )

        assert PreRegisteredStudent.objects.filter(role_id="mentor").count() == 2

    def test_import_skips_duplicate_personnel_numbers(self, tmp_path: Path) -> None:
        path = tmp_path / "dup.xls"
        Department.objects.create(name="Кафедра информатики", short_name="КИ")
        _write_sample_teachers(
            path,
            [
                [
                    "Кафедра информатики",
                    "Иванов Иван",
                    "доцент",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "900001",
                    "",
                    "",
                ],
                [
                    "Кафедра информатики",
                    "Иванов Иван Другой",
                    "доцент",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "900001",
                    "",
                    "",
                ],
            ],
        )
        out = StringIO()

        call_command(
            "import_preregistered_mentors",
            file=str(path),
            non_interactive=True,
            stdout=out,
        )

        assert (
            PreRegisteredStudent.objects.filter(personnel_number="900001").count() == 1
        )
        assert "дубликат" in out.getvalue().lower()

    def test_import_fails_without_required_columns(self, tmp_path: Path) -> None:
        path = tmp_path / "bad.xls"
        df = pd.DataFrame([["title"], ["ФИО"], ["Иванов Иван"]])
        df.to_excel(path, index=False, header=False)

        with pytest.raises(CommandError, match="обязательные колонки"):
            call_command("import_preregistered_mentors", file=str(path))

    def test_import_skips_invalid_full_name_row(self, tmp_path: Path) -> None:
        path = tmp_path / "invalid-fio.xls"
        Department.objects.create(name="Кафедра информатики", short_name="КИ")
        _write_sample_teachers(
            path,
            [
                [
                    "Кафедра информатики",
                    "Иванов Иван",
                    "доцент",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "900001",
                    "",
                    "",
                ],
                [
                    "Кафедра информатики",
                    "1567",
                    "доцент",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "900002",
                    "",
                    "",
                ],
            ],
        )
        out = StringIO()

        call_command(
            "import_preregistered_mentors",
            file=str(path),
            non_interactive=True,
            stdout=out,
        )

        assert PreRegisteredStudent.objects.filter(role_id="mentor").count() == 1
        assert "Некорректное ФИО" in out.getvalue()

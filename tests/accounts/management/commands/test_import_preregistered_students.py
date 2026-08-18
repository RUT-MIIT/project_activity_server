"""Тесты команды import_preregistered_students."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError
import pandas as pd
import pytest

from accounts.models import PreRegisteredStudent
from showcase.models import Institute
from teams.models import Direction, StudyGroup

COLUMNS = [
    "Форма обучения",
    "Код специальности",
    "ФИО (полное)",
    "Институт",
    "Специальность",
    "Профиль/специализация/программа",
    "Студенческий билет",
    "Начало обучения в группе",
    "Вид уровня образования",
    "Курс",
    "Пол",
    "Телефон",
    "Электронная почта",
    "Дата планового окончания",
    "СНИЛС",
    "ID_E человека",
    "ID студента",
    "ID группы",
    "Постоянная группа",
    "ID постоянной группы",
]


def _write_sample_contingent(path: Path) -> None:
    """Создаёт минимальный отчёт контингента для тестов."""
    path.parent.mkdir(parents=True, exist_ok=True)
    title_row = ["Заголовок отчёта"] + [""] * (len(COLUMNS) - 1)
    data_rows = [
        [
            "очная",
            "25.03.03",
            "Иванов Иван Иванович",
            "Академия гражданской авиации",
            "Аэронавигация",
            "Организация бизнес-процессов",
            "25011884",
            "01.09.2025",
            "бакалавриат",
            1,
            "м",
            "79161384053",
            "test@mail.ru",
            "31.08.2029",
            "18457362806",
            "1335090",
            "6054707",
            "197175",
            "АМБ-2025-11",
            "309371",
        ],
        [
            "очная",
            "25.03.03",
            "Петров Пётр",
            "Академия гражданской авиации",
            "Аэронавигация",
            "Организация бизнес-процессов",
            "25005843",
            "01.09.2025",
            "бакалавриат",
            1,
            "м",
            "79920040184",
            "test2@mail.ru",
            "31.08.2029",
            "20064882942",
            "1330766",
            "6048844",
            "205393",
            "АМБ-2025-11",
            "309835",
        ],
        [
            "очная",
            "25.03.03",
            "",
            "Академия гражданской авиации",
            "Аэронавигация",
            "Организация бизнес-процессов",
            "",
            "01.09.2025",
            "бакалавриат",
            1,
            "м",
            "",
            "",
            "31.08.2029",
            "",
            "",
            "",
            "",
            "АМБ-2025-11",
            "",
        ],
    ]
    df = pd.DataFrame([title_row, COLUMNS, *data_rows])
    df.to_excel(path, index=False, header=False)


@pytest.fixture
def sample_contingent_file(tmp_path: Path) -> Path:
    path = tmp_path / "contingent_sample.xlsx"
    _write_sample_contingent(path)
    return path


@pytest.fixture
def aga_institute(db: Any) -> Institute:
    return Institute.objects.create(
        code="AGA",
        name="Академия гражданской авиации",
        position=1,
        is_active=True,
    )


@pytest.fixture
def study_group(db: Any, aga_institute: Institute) -> StudyGroup:
    direction = Direction.objects.create(
        code="25.03.03",
        name="Аэронавигация",
        level=Direction.Level.BAKALAVRIAT,
    )
    return StudyGroup.objects.create(
        name="АМБ-211",
        code="АМБ-2025-11",
        enrollment_year=2025,
        course_number=2,
        direction=direction,
        institute=aga_institute,
        profile="Организация бизнес-процессов",
        form="очная",
    )


@pytest.mark.django_db
class TestImportPreRegisteredStudentsCommand:
    def test_import_creates_students(
        self, sample_contingent_file: Path, study_group: StudyGroup
    ) -> None:
        call_command("import_preregistered_students", file=str(sample_contingent_file))

        assert PreRegisteredStudent.objects.count() == 2
        student = PreRegisteredStudent.objects.get(personnel_number="1335090")
        assert student.last_name == "Иванов"
        assert student.first_name == "Иван"
        assert student.middle_name == "Иванович"
        assert student.student_card == "25011884"
        assert student.snils == "18457362806"
        assert student.group_id == study_group.pk

    def test_import_is_idempotent(
        self, sample_contingent_file: Path, study_group: StudyGroup
    ) -> None:
        call_command("import_preregistered_students", file=str(sample_contingent_file))
        call_command("import_preregistered_students", file=str(sample_contingent_file))

        assert PreRegisteredStudent.objects.count() == 2

    def test_import_updates_existing_record(
        self, sample_contingent_file: Path, study_group: StudyGroup
    ) -> None:
        call_command("import_preregistered_students", file=str(sample_contingent_file))
        student = PreRegisteredStudent.objects.get(personnel_number="1335090")
        student.first_name = "Старое имя"
        student.save(update_fields=["first_name"])

        call_command("import_preregistered_students", file=str(sample_contingent_file))

        student.refresh_from_db()
        assert student.first_name == "Иван"

    def test_import_clear_keeps_registered(
        self,
        sample_contingent_file: Path,
        study_group: StudyGroup,
        roles: dict[str, Any],
        make_user,
    ) -> None:
        call_command("import_preregistered_students", file=str(sample_contingent_file))
        registered = PreRegisteredStudent.objects.get(personnel_number="1335090")
        user = make_user(role_code="user", email="registered@example.com")
        registered.student = user
        registered.save(update_fields=["student"])

        call_command(
            "import_preregistered_students",
            file=str(sample_contingent_file),
            clear=True,
        )

        registered.refresh_from_db()
        assert registered.student_id == user.pk
        assert PreRegisteredStudent.objects.filter(student__isnull=True).count() == 1
        assert PreRegisteredStudent.objects.count() == 2

    def test_import_fails_without_groups(self, sample_contingent_file: Path) -> None:
        with pytest.raises(CommandError, match="отсутствуют группы"):
            call_command(
                "import_preregistered_students", file=str(sample_contingent_file)
            )

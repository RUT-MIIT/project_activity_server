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
    "Группа",
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
            2,
            "АМБ-211",
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
            2,
            "АМБ-211",
            "м",
            "79920040184",
            "test2@mail.ru",
            "31.08.2029",
            "20064882942",
            "1330766",
            "6048844",
            "197175",
            "АМБ-2025-11",
            "309371",
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
            2,
            "АМБ-211",
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
        external_group_id="197175",
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
        registered.user = user
        registered.save(update_fields=["user"])

        call_command(
            "import_preregistered_students",
            file=str(sample_contingent_file),
            clear=True,
        )

        registered.refresh_from_db()
        assert registered.user_id == user.pk
        assert PreRegisteredStudent.objects.filter(user__isnull=True).count() == 1
        assert PreRegisteredStudent.objects.count() == 2

    def test_import_fails_without_groups(self, sample_contingent_file: Path) -> None:
        with pytest.raises(CommandError, match="отсутствуют группы"):
            call_command(
                "import_preregistered_students", file=str(sample_contingent_file)
            )

    def test_import_deletes_unregistered_missing_from_file(
        self, sample_contingent_file: Path, study_group: StudyGroup
    ) -> None:
        PreRegisteredStudent.objects.create(
            personnel_number="9999999",
            last_name="Сидоров",
            first_name="Сидор",
            middle_name="",
            student_card="25009999",
            snils="",
            group=study_group,
        )

        call_command("import_preregistered_students", file=str(sample_contingent_file))

        assert (
            PreRegisteredStudent.objects.filter(personnel_number="9999999").count() == 0
        )
        assert PreRegisteredStudent.objects.count() == 2

    def test_import_keeps_registered_missing_from_file(
        self,
        sample_contingent_file: Path,
        study_group: StudyGroup,
        roles: dict[str, Any],
        make_user,
    ) -> None:
        user = make_user(role_code="user", email="old@example.com")
        registered = PreRegisteredStudent.objects.create(
            personnel_number="9999999",
            last_name="Сидоров",
            first_name="Сидор",
            middle_name="",
            student_card="25009999",
            snils="",
            group=study_group,
            user=user,
        )

        call_command("import_preregistered_students", file=str(sample_contingent_file))

        registered.refresh_from_db()
        assert registered.pk is not None
        assert registered.user_id == user.pk
        assert PreRegisteredStudent.objects.count() == 3

    def test_import_assigns_students_by_external_group_id(
        self, tmp_path: Path, aga_institute: Institute
    ) -> None:
        direction = Direction.objects.create(
            code="09.03.01",
            name="Информатика",
            level=Direction.Level.BAKALAVRIAT,
        )
        group_241 = StudyGroup.objects.create(
            name="ТКИ-241",
            code="ТКИ-2024-41",
            enrollment_year=2024,
            course_number=2,
            direction=direction,
            institute=aga_institute,
            external_group_id="193722",
        )
        group_341 = StudyGroup.objects.create(
            name="ТКИ-341",
            code="ТКИ-2024-41",
            enrollment_year=2024,
            course_number=3,
            direction=direction,
            institute=aga_institute,
            external_group_id="193714",
        )

        path = tmp_path / "tki_split.xlsx"
        title_row = ["Заголовок"] + [""] * (len(COLUMNS) - 1)
        data_rows = [
            [
                "очная",
                "09.03.01",
                "Горячев Иван Иванович",
                "Академия гражданской авиации",
                "Информатика",
                "Профиль",
                "25002390",
                "01.09.2024",
                "бакалавриат",
                2,
                "ТКИ-241",
                "м",
                "",
                "",
                "31.08.2029",
                "18457362806",
                "1335090",
                "",
                "193722",
                "ТКИ-2024-41",
                "perm-341",
            ],
            [
                "очная",
                "09.03.01",
                "Петров Пётр",
                "Академия гражданской авиации",
                "Информатика",
                "Профиль",
                "25005843",
                "01.09.2024",
                "бакалавриат",
                3,
                "ТКИ-341",
                "м",
                "",
                "",
                "31.08.2029",
                "20064882942",
                "1330766",
                "",
                "193714",
                "ТКИ-2024-41",
                "perm-341",
            ],
        ]
        pd.DataFrame([title_row, COLUMNS, *data_rows]).to_excel(
            path, index=False, header=False
        )

        call_command("import_preregistered_students", file=str(path))

        goryachev = PreRegisteredStudent.objects.get(personnel_number="1335090")
        other = PreRegisteredStudent.objects.get(personnel_number="1330766")
        assert goryachev.group_id == group_241.pk
        assert goryachev.student_card == "25002390"
        assert other.group_id == group_341.pk

    def test_import_remaps_merged_external_group_id(
        self, tmp_path: Path, aga_institute: Institute
    ) -> None:
        direction = Direction.objects.create(
            code="09.03.01",
            name="Информатика",
            level=Direction.Level.BAKALAVRIAT,
        )
        target = StudyGroup.objects.create(
            name="ТСТ-441",
            code="ТСТ-2023-41",
            enrollment_year=2023,
            course_number=4,
            direction=direction,
            institute=aga_institute,
            external_group_id="193901",
        )

        path = tmp_path / "remap_students.xlsx"
        title_row = ["Заголовок"] + [""] * (len(COLUMNS) - 1)
        data_row = [
            "очная",
            "09.03.01",
            "Студент ТСТ ТСТ",
            "Академия гражданской авиации",
            "Информатика",
            "Профиль",
            "25009999",
            "01.09.2023",
            "бакалавриат",
            4,
            "ТСТ-442",
            "м",
            "",
            "",
            "31.08.2027",
            "18457362806",
            "1444001",
            "",
            "193902",
            "ТСТ-2023-42",
            "perm-442",
        ]
        pd.DataFrame([title_row, COLUMNS, data_row]).to_excel(
            path, index=False, header=False
        )

        call_command("import_preregistered_students", file=str(path))

        student = PreRegisteredStudent.objects.get(personnel_number="1444001")
        assert student.group_id == target.pk

    def test_import_syncs_registered_user_study_group(
        self,
        sample_contingent_file: Path,
        study_group: StudyGroup,
        roles: dict[str, Any],
        make_user,
    ) -> None:
        user = make_user(role_code="user", email="registered@example.com")
        other_direction = Direction.objects.create(
            code="09.03.01",
            name="Другое",
            level=Direction.Level.BAKALAVRIAT,
        )
        other_group = StudyGroup.objects.create(
            name="Другая",
            code="ДР-2020-01",
            direction=other_direction,
            institute=study_group.institute,
        )
        user.study_group = other_group
        user.save(update_fields=["study_group"])

        PreRegisteredStudent.objects.create(
            personnel_number="1335090",
            last_name="Иванов",
            first_name="Иван",
            middle_name="Иванович",
            student_card="25011884",
            snils="18457362806",
            group=other_group,
            user=user,
        )

        call_command(
            "import_preregistered_students",
            file=str(sample_contingent_file),
        )

        user.refresh_from_db()
        student = PreRegisteredStudent.objects.get(personnel_number="1335090")
        assert student.group_id == study_group.pk
        assert user.study_group_id == study_group.pk

    def test_import_skips_row_without_external_group_id(
        self, tmp_path: Path, study_group: StudyGroup
    ) -> None:
        path = tmp_path / "missing_id.xlsx"
        title_row = ["Заголовок"] + [""] * (len(COLUMNS) - 1)
        data_row = [
            "очная",
            "25.03.03",
            "Иванов Иван Иванович",
            "Академия гражданской авиации",
            "Аэронавигация",
            "Профиль",
            "25011884",
            "01.09.2025",
            "бакалавриат",
            2,
            "АМБ-211",
            "м",
            "",
            "",
            "31.08.2029",
            "18457362806",
            "1335090",
            "",
            "",
            "АМБ-2025-11",
            "",
        ]
        pd.DataFrame([title_row, COLUMNS, data_row]).to_excel(
            path, index=False, header=False
        )

        call_command("import_preregistered_students", file=str(path))

        assert PreRegisteredStudent.objects.count() == 0

    def test_import_skips_excluded_permanent_group(
        self, sample_contingent_file: Path, study_group: StudyGroup, monkeypatch
    ) -> None:
        monkeypatch.setattr(
            "teams.domain.study_group_import.SKIPPED_PERMANENT_GROUP_CODES",
            frozenset({"АМБ-2025-11"}),
        )

        call_command(
            "import_preregistered_students",
            file=str(sample_contingent_file),
        )

        assert PreRegisteredStudent.objects.count() == 0

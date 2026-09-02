"""Тесты импорта учебных групп из контингента 1С."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from django.core.management import call_command
from django.core.management.base import CommandError
import pandas as pd
import pytest

from showcase.models import Institute
from teams.domain.study_group_import import (
    build_group_import_row,
    build_group_name,
    calculate_course_number,
    group_ended_by_planned_dates,
    parse_permanent_group_code,
    parse_planned_end_date,
)
from teams.models import Direction, StudyGroup

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
SAMPLE_FILE = FIXTURES_DIR / "contingent_sample.xlsx"

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
            "Студент 1",
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
            "Студент 2",
            "Академия гражданской авиации",
            "Аэронавигация",
            "Организация бизнес-процессов",
            "25005843",
            "01.09.2025",
            "бакalavriat",
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
    ]
    # Исправляем опечатку в level второй строки
    data_rows[1][8] = "бакалавриат"

    df = pd.DataFrame([title_row, COLUMNS, *data_rows])
    df.to_excel(path, index=False, header=False)


@pytest.fixture
def sample_contingent_file(tmp_path: Path) -> Path:
    """Временный файл контингента для интеграционных тестов."""
    path = tmp_path / "contingent_sample.xlsx"
    _write_sample_contingent(path)
    return path


@pytest.fixture
def direction(db: Any) -> Direction:
    """Направление подготовки для тестов импорта."""
    return Direction.objects.create(
        code="38.03.01",
        name="Экономика",
        level=Direction.Level.BAKALAVRIAT,
    )


@pytest.fixture
def aga_institute(db: Any) -> Institute:
    """Институт АГА для тестового импорта."""
    return Institute.objects.create(
        code="AGA",
        name="Академия гражданской авиации",
        position=1,
        is_active=True,
    )


class TestStudyGroupImportDomain:
    def test_parse_permanent_group_code(self) -> None:
        parsed = parse_permanent_group_code("АМБ-2025-11")
        assert parsed.abbrev == "АМБ"
        assert parsed.enrollment_year == 2025
        assert parsed.group_num == "11"

    def test_parse_permanent_group_code_with_tail(self) -> None:
        parsed = parse_permanent_group_code("ОММ-2022-11-1")
        assert parsed.abbrev == "ОММ"
        assert parsed.enrollment_year == 2022
        assert parsed.group_num == "11"

    def test_calculate_course_autumn(self) -> None:
        assert (
            calculate_course_number(
                current_year=2026,
                enrollment_year=2025,
                semester="autumn",
            )
            == 2
        )

    def test_calculate_course_spring(self) -> None:
        assert (
            calculate_course_number(
                current_year=2027,
                enrollment_year=2025,
                semester="spring",
            )
            == 2
        )

    def test_build_group_name(self) -> None:
        assert (
            build_group_name(abbrev="АМБ", course_number=2, group_num="11") == "АМБ-211"
        )

    def test_build_group_import_row_autumn(self) -> None:
        row = build_group_import_row(
            permanent_group_code="АМБ-2025-11",
            institute_name="Академия гражданской авиации",
            direction_code="25.03.03",
            direction_name="Аэронавигация",
            direction_level="бакалавриат",
            profile="Организация бизнес-процессов",
            form="очная",
            current_year=2026,
            semester="autumn",
        )
        assert row.code == "АМБ-2025-11"
        assert row.name == "АМБ-211"
        assert row.course_number == 2
        assert row.enrollment_year == 2025
        assert row.institute_code == "AGA"
        assert row.profile == "Организация бизнес-процессов"
        assert row.form == "очная"

    def test_parse_planned_end_date_from_string(self) -> None:
        assert parse_planned_end_date("31.08.2029") == date(2029, 8, 31)

    def test_parse_planned_end_date_from_datetime(self) -> None:
        from datetime import datetime

        assert parse_planned_end_date(datetime(2029, 8, 31, 12, 0)) == date(2029, 8, 31)

    def test_group_ended_by_planned_dates_all_past(self) -> None:
        today = date(2026, 8, 29)
        assert group_ended_by_planned_dates(
            [date(2025, 6, 30), date(2025, 6, 30)],
            today=today,
        )

    def test_group_ended_by_planned_dates_with_future(self) -> None:
        today = date(2026, 8, 29)
        assert not group_ended_by_planned_dates(
            [date(2025, 6, 30), date(2029, 8, 31)],
            today=today,
        )

    def test_group_ended_by_planned_dates_empty_values(self) -> None:
        today = date(2026, 8, 29)
        assert not group_ended_by_planned_dates([None, None], today=today)


@pytest.mark.django_db
class TestImportStudyGroupsFromContingentCommand:
    def test_import_autumn_creates_group(
        self, sample_contingent_file: Path, aga_institute: Institute
    ) -> None:
        call_command(
            "import_study_groups_from_contingent",
            file=str(sample_contingent_file),
            year=2026,
            semester="autumn",
        )

        group = StudyGroup.objects.get(code="АМБ-2025-11")
        assert group.name == "АМБ-211"
        assert group.course_number == 2
        assert group.enrollment_year == 2025
        assert group.institute_id == "AGA"
        assert group.profile == "Организация бизнес-процессов"
        assert group.form == "очная"
        assert group.direction_id == "25.03.03"
        assert Direction.objects.filter(code="25.03.03").exists()

    def test_import_spring_same_course(
        self, sample_contingent_file: Path, aga_institute: Institute
    ) -> None:
        call_command(
            "import_study_groups_from_contingent",
            file=str(sample_contingent_file),
            year=2027,
            semester="spring",
        )

        group = StudyGroup.objects.get(code="АМБ-2025-11")
        assert group.name == "АМБ-211"
        assert group.course_number == 2

    def test_import_is_idempotent(
        self, sample_contingent_file: Path, aga_institute: Institute
    ) -> None:
        call_command(
            "import_study_groups_from_contingent",
            file=str(sample_contingent_file),
            year=2026,
            semester="autumn",
        )
        call_command(
            "import_study_groups_from_contingent",
            file=str(sample_contingent_file),
            year=2026,
            semester="autumn",
        )

        assert StudyGroup.objects.filter(code="АМБ-2025-11").count() == 1

    def test_import_clear_removes_old_groups(
        self, sample_contingent_file: Path, aga_institute: Institute, direction: Any
    ) -> None:
        StudyGroup.objects.create(
            name="Старая группа",
            code="OLD-2020-01",
            direction=direction,
            institute=aga_institute,
        )

        call_command(
            "import_study_groups_from_contingent",
            file=str(sample_contingent_file),
            year=2026,
            semester="autumn",
            clear=True,
        )

        assert not StudyGroup.objects.filter(code="OLD-2020-01").exists()
        assert StudyGroup.objects.filter(code="АМБ-2025-11").exists()

    def test_import_unknown_institute_raises(self, tmp_path: Path) -> None:
        path = tmp_path / "unknown_institute.xlsx"
        title_row = ["Заголовок"] + [""] * (len(COLUMNS) - 1)
        data_row = [
            "очная",
            "25.03.03",
            "Студент",
            "Неизвестный институт тестовый",
            "Аэронавигация",
            "Профиль",
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
        ]
        pd.DataFrame([title_row, COLUMNS, data_row]).to_excel(
            path, index=False, header=False
        )

        with pytest.raises(CommandError, match="Неизвестные институты"):
            call_command(
                "import_study_groups_from_contingent",
                file=str(path),
                year=2026,
            )

    def test_import_marks_missing_groups_as_ended(
        self, sample_contingent_file: Path, aga_institute: Institute, direction: Any
    ) -> None:
        old_group = StudyGroup.objects.create(
            name="Старая группа",
            code="OLD-2020-01",
            direction=direction,
            institute=aga_institute,
            is_end=False,
        )

        call_command(
            "import_study_groups_from_contingent",
            file=str(sample_contingent_file),
            year=2026,
            semester="autumn",
        )

        old_group.refresh_from_db()
        imported = StudyGroup.objects.get(code="АМБ-2025-11")
        assert old_group.is_end is True
        assert imported.is_end is False

    def test_import_reactivates_previously_ended_group(
        self, sample_contingent_file: Path, aga_institute: Institute, direction: Any
    ) -> None:
        ended_group = StudyGroup.objects.create(
            name="АМБ-211",
            code="АМБ-2025-11",
            direction=direction,
            institute=aga_institute,
            is_end=True,
        )

        call_command(
            "import_study_groups_from_contingent",
            file=str(sample_contingent_file),
            year=2026,
            semester="autumn",
        )

        ended_group.refresh_from_db()
        assert ended_group.is_end is False

    def test_import_marks_group_ended_when_all_planned_dates_past(
        self, tmp_path: Path, aga_institute: Institute
    ) -> None:
        path = tmp_path / "past_dates.xlsx"
        title_row = ["Заголовок"] + [""] * (len(COLUMNS) - 1)
        data_rows = [
            [
                "очная",
                "25.03.03",
                "Студент 1",
                "Академия гражданской авиации",
                "Аэронавигация",
                "Организация бизнес-процессов",
                "25011884",
                "01.09.2020",
                "бакалавриат",
                7,
                "АМБ-711",
                "м",
                "79161384053",
                "test@mail.ru",
                "31.08.2023",
                "18457362806",
                "1335090",
                "6054707",
                "197175",
                "АМБ-2020-11",
                "309371",
            ],
            [
                "очная",
                "25.03.03",
                "Студент 2",
                "Академия гражданской авиации",
                "Аэронавигация",
                "Организация бизнес-процессов",
                "25005843",
                "01.09.2020",
                "бакалавриат",
                7,
                "АМБ-711",
                "м",
                "79920040184",
                "test2@mail.ru",
                "30.06.2023",
                "20064882942",
                "1330766",
                "6048844",
                "205393",
                "АМБ-2020-11",
                "309835",
            ],
        ]
        pd.DataFrame([title_row, COLUMNS, *data_rows]).to_excel(
            path, index=False, header=False
        )

        call_command(
            "import_study_groups_from_contingent",
            file=str(path),
            year=2026,
            semester="autumn",
        )

        group = StudyGroup.objects.get(code="АМБ-2020-11")
        assert group.is_end is True

    def test_import_keeps_group_active_when_one_planned_date_future(
        self, tmp_path: Path, aga_institute: Institute
    ) -> None:
        path = tmp_path / "mixed_dates.xlsx"
        title_row = ["Заголовок"] + [""] * (len(COLUMNS) - 1)
        data_rows = [
            [
                "очная",
                "25.03.03",
                "Студент 1",
                "Академия гражданской авиации",
                "Аэронавигация",
                "Организация бизнес-процессов",
                "25011884",
                "01.09.2025",
                "бакалавриат",
                2,
                "АМБ-212",
                "м",
                "79161384053",
                "test@mail.ru",
                "31.08.2023",
                "18457362806",
                "1335090",
                "6054707",
                "197175",
                "АМБ-2025-12",
                "309371",
            ],
            [
                "очная",
                "25.03.03",
                "Студент 2",
                "Академия гражданской авиации",
                "Аэронавигация",
                "Организация бизнес-процессов",
                "25005843",
                "01.09.2025",
                "бакалавриат",
                2,
                "АМБ-212",
                "м",
                "79920040184",
                "test2@mail.ru",
                "31.08.2029",
                "20064882942",
                "1330766",
                "6048844",
                "205393",
                "АМБ-2025-12",
                "309835",
            ],
        ]
        pd.DataFrame([title_row, COLUMNS, *data_rows]).to_excel(
            path, index=False, header=False
        )

        call_command(
            "import_study_groups_from_contingent",
            file=str(path),
            year=2026,
            semester="autumn",
        )

        group = StudyGroup.objects.get(code="АМБ-2025-12")
        assert group.is_end is False

    def test_import_backfills_external_group_id(
        self, sample_contingent_file: Path, aga_institute: Institute
    ) -> None:
        call_command(
            "import_study_groups_from_contingent",
            file=str(sample_contingent_file),
            year=2026,
            semester="autumn",
        )

        group = StudyGroup.objects.get(code="АМБ-2025-11")
        assert group.external_group_id == "197175"
        assert group.external_permanent_group_id == "309371"

    def test_import_without_external_columns_skips_phase_two(
        self, tmp_path: Path, aga_institute: Institute
    ) -> None:
        path = tmp_path / "no_external_cols.xlsx"
        columns = [
            col
            for col in COLUMNS
            if col not in ("ID группы", "ID постоянной группы", "Группа", "Курс")
        ]
        title_row = ["Заголовок"] + [""] * (len(columns) - 1)
        data_row = [
            "очная",
            "25.03.03",
            "Студент 1",
            "Академия гражданской авиации",
            "Аэронавигация",
            "Организация бизнес-процессов",
            "25011884",
            "01.09.2025",
            "бакалавриат",
            "м",
            "79161384053",
            "test@mail.ru",
            "31.08.2029",
            "18457362806",
            "1335090",
            "6054707",
            "АМБ-2025-11",
        ]
        pd.DataFrame([title_row, columns, data_row]).to_excel(
            path, index=False, header=False
        )

        call_command(
            "import_study_groups_from_contingent",
            file=str(path),
            year=2026,
            semester="autumn",
        )

        group = StudyGroup.objects.get(code="АМБ-2025-11")
        assert group.external_group_id == ""

    def test_import_skips_excluded_permanent_group(
        self, sample_contingent_file: Path, aga_institute: Institute, monkeypatch
    ) -> None:
        monkeypatch.setattr(
            "teams.domain.study_group_import.SKIPPED_PERMANENT_GROUP_CODES",
            frozenset({"АМБ-2025-11"}),
        )

        call_command(
            "import_study_groups_from_contingent",
            file=str(sample_contingent_file),
            year=2026,
            semester="autumn",
        )

        assert not StudyGroup.objects.filter(code="АМБ-2025-11").exists()

    def test_import_applies_name_override(
        self, sample_contingent_file: Path, aga_institute: Institute, monkeypatch
    ) -> None:
        monkeypatch.setattr(
            "teams.domain.study_group_import.STUDY_GROUP_NAME_OVERRIDES_BY_CODE",
            {"АМБ-2025-11": "АМБ-211Н"},
        )

        call_command(
            "import_study_groups_from_contingent",
            file=str(sample_contingent_file),
            year=2026,
            semester="autumn",
        )

        group = StudyGroup.objects.get(code="АМБ-2025-11")
        assert group.name == "АМБ-211Н"

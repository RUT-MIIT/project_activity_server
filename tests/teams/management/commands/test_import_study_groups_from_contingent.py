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
    build_group_name,
    calculate_course_number,
    group_ended_by_planned_dates,
    parse_permanent_group_code,
    parse_planned_end_date,
)
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


def _write_contingent(path: Path, data_rows: list[list[object]]) -> None:
    title_row = ["Заголовок отчёта"] + [""] * (len(COLUMNS) - 1)
    pd.DataFrame([title_row, COLUMNS, *data_rows]).to_excel(
        path, index=False, header=False
    )


def _base_row(
    *,
    fio: str = "Студент 1",
    card: str = "25011884",
    course: int = 2,
    group_name: str = "АМБ-211",
    group_id: str = "197175",
    permanent: str = "АМБ-2025-11",
    institute: str = "Академия гражданской авиации",
    direction_code: str = "25.03.03",
    direction_name: str = "Аэронавигация",
    personnel: str = "1335090",
    permanent_id: str = "309371",
) -> list[object]:
    return [
        "очная",
        direction_code,
        fio,
        institute,
        direction_name,
        "Организация бизнес-процессов",
        card,
        "01.09.2025",
        "бакалавриат",
        course,
        group_name,
        "м",
        "",
        "",
        "31.08.2029",
        "18457362806",
        personnel,
        "",
        group_id,
        permanent,
        permanent_id,
    ]


@pytest.fixture
def sample_contingent_file(tmp_path: Path) -> Path:
    path = tmp_path / "contingent_sample.xlsx"
    _write_contingent(
        path,
        [
            _base_row(),
            _base_row(
                fio="Студент 2",
                card="25005843",
                personnel="1330766",
            ),
        ],
    )
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
def ief_institute(db: Any) -> Institute:
    return Institute.objects.create(
        code="IEF",
        name="ИЭФ",
        position=10,
        is_active=True,
    )


@pytest.fixture
def ittsy_institute(db: Any) -> Institute:
    return Institute.objects.create(
        code="ITTSY",
        name="ИТТСУ",
        position=11,
        is_active=True,
    )


@pytest.fixture
def direction(db: Any) -> Direction:
    return Direction.objects.create(
        code="38.03.01",
        name="Экономика",
        level=Direction.Level.BAKALAVRIAT,
    )


class TestStudyGroupImportDomainHelpers:
    def test_parse_permanent_group_code(self) -> None:
        parsed = parse_permanent_group_code("АМБ-2025-11")
        assert parsed.abbrev == "АМБ"
        assert parsed.enrollment_year == 2025
        assert parsed.group_num == "11"

    def test_calculate_course_autumn(self) -> None:
        assert (
            calculate_course_number(
                current_year=2026, enrollment_year=2025, semester="autumn"
            )
            == 2
        )

    def test_build_group_name(self) -> None:
        assert (
            build_group_name(abbrev="АМБ", course_number=2, group_num="11") == "АМБ-211"
        )

    def test_parse_planned_end_date_from_string(self) -> None:
        assert parse_planned_end_date("31.08.2029") == date(2029, 8, 31)

    def test_group_ended_by_planned_dates_all_past(self) -> None:
        assert group_ended_by_planned_dates(
            [date(2025, 6, 30), date(2025, 6, 30)],
            today=date(2026, 8, 29),
        )


@pytest.mark.django_db
class TestImportStudyGroupsFromContingentCommand:
    def test_import_creates_group_by_external_id(
        self, sample_contingent_file: Path, aga_institute: Institute
    ) -> None:
        call_command(
            "import_study_groups_from_contingent",
            file=str(sample_contingent_file),
        )

        group = StudyGroup.objects.get(external_group_id="197175")
        assert group.code == "АМБ-2025-11"
        assert group.name == "АМБ-211"
        assert group.course_number == 2
        assert group.enrollment_year == 2025
        assert group.institute_id == "AGA"
        assert group.is_end is False

    def test_import_split_permanent_creates_two_groups_and_claims_by_name(
        self, tmp_path: Path, aga_institute: Institute, direction: Direction
    ) -> None:
        old = StudyGroup.objects.create(
            name="ТКИ-341",
            code="ТКИ-2024-41",
            direction=direction,
            institute=aga_institute,
            enrollment_year=2024,
            course_number=3,
            external_group_id="",
            is_end=False,
        )
        path = tmp_path / "split.xlsx"
        _write_contingent(
            path,
            [
                _base_row(
                    fio="A",
                    card="1",
                    course=2,
                    group_name="ТКИ-241",
                    group_id="193722",
                    permanent="ТКИ-2024-41",
                    personnel="1",
                    permanent_id="p1",
                ),
                _base_row(
                    fio="B",
                    card="2",
                    course=3,
                    group_name="ТКИ-341",
                    group_id="193714",
                    permanent="ТКИ-2024-41",
                    personnel="2",
                    permanent_id="p1",
                ),
            ],
        )

        call_command("import_study_groups_from_contingent", file=str(path))

        old.refresh_from_db()
        assert old.external_group_id == "193714"
        assert old.name == "ТКИ-341"
        assert old.is_end is False

        other = StudyGroup.objects.get(external_group_id="193722")
        assert other.pk != old.pk
        assert other.name == "ТКИ-241"
        assert other.code == "ТКИ-2024-41"
        assert StudyGroup.objects.count() == 2

    def test_import_marks_missing_external_id_groups_as_ended(
        self,
        sample_contingent_file: Path,
        aga_institute: Institute,
        direction: Direction,
    ) -> None:
        orphan = StudyGroup.objects.create(
            name="Старая",
            code="OLD-2020-01",
            direction=direction,
            institute=aga_institute,
            external_group_id="999999",
            is_end=False,
        )
        empty = StudyGroup.objects.create(
            name="Без ID",
            code="OLD-2019-01",
            direction=direction,
            institute=aga_institute,
            external_group_id="",
            is_end=False,
        )

        call_command(
            "import_study_groups_from_contingent",
            file=str(sample_contingent_file),
        )

        orphan.refresh_from_db()
        empty.refresh_from_db()
        imported = StudyGroup.objects.get(external_group_id="197175")
        assert orphan.is_end is True
        assert empty.is_end is True
        assert imported.is_end is False

    def test_import_skips_remapped_away_id(
        self, tmp_path: Path, aga_institute: Institute
    ) -> None:
        path = tmp_path / "remap.xlsx"
        _write_contingent(
            path,
            [
                _base_row(
                    group_name="ТСТ-442",
                    group_id="193902",
                    permanent="ТСТ-2023-42",
                    course=4,
                ),
                _base_row(
                    fio="Целевая",
                    card="9",
                    group_name="ТСТ-441",
                    group_id="193901",
                    permanent="ТСТ-2023-41",
                    course=4,
                    personnel="9",
                ),
            ],
        )

        call_command("import_study_groups_from_contingent", file=str(path))

        assert not StudyGroup.objects.filter(external_group_id="193902").exists()
        assert StudyGroup.objects.filter(external_group_id="193901").exists()

    def test_import_applies_override_by_external_id(
        self,
        tmp_path: Path,
        ief_institute: Institute,
        ittsy_institute: Institute,
    ) -> None:
        path = tmp_path / "tup_override.xlsx"
        _write_contingent(
            path,
            [
                _base_row(
                    institute="Институт транспортной техники и систем управления",
                    direction_code="38.03.03",
                    direction_name="Управление персоналом",
                    group_name="ТУП-211",
                    group_id="149820",
                    permanent="ТУП-2025-11",
                    course=2,
                )
            ],
        )

        call_command("import_study_groups_from_contingent", file=str(path))

        group = StudyGroup.objects.get(external_group_id="149820")
        assert group.name == "ЭПО-211"
        assert group.institute_id == "IEF"
        assert group.code == "ТУП-2025-11"

    def test_import_unknown_institute_fails(
        self, tmp_path: Path, aga_institute: Institute
    ) -> None:
        path = tmp_path / "bad_inst.xlsx"
        _write_contingent(
            path,
            [
                _base_row(institute="Неизвестный институт"),
            ],
        )
        with pytest.raises(CommandError, match="Неизвестные институты"):
            call_command("import_study_groups_from_contingent", file=str(path))

    def test_import_idempotent(
        self, sample_contingent_file: Path, aga_institute: Institute
    ) -> None:
        call_command(
            "import_study_groups_from_contingent", file=str(sample_contingent_file)
        )
        call_command(
            "import_study_groups_from_contingent", file=str(sample_contingent_file)
        )
        assert StudyGroup.objects.filter(external_group_id="197175").count() == 1

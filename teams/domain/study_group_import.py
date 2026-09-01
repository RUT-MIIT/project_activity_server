"""Чистая логика импорта учебных групп из отчёта контингента 1С."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
import re
from typing import Literal

Semester = Literal["autumn", "spring"]

PERMANENT_GROUP_PATTERN = re.compile(
    r"^(?P<abbrev>.+)-(?P<year>\d{4})-(?P<num>\d+)(?:-\d+)?$"
)

TEACHING_GROUP_NAME_PATTERN = re.compile(
    r"^(?P<abbrev>.+)-(?P<course>\d)(?P<group_num>\d+)$"
)

OPTIONAL_EXTERNAL_ID_COLUMNS = (
    "Группа",
    "Курс",
    "ID группы",
)

OPTIONAL_PERMANENT_EXTERNAL_ID_COLUMN = "ID постоянной группы"

INSTITUTE_NAME_TO_CODE: dict[str, str] = {
    "Академия гражданской авиации": "AGA",
    "Академия водного транспорта": "AVT",
    "Академия дорожного хозяйства": "ADH",
    "Высшая инженерная школа": "VISH",
    "Институт международных транспортных коммуникаций": "IMTK",
    "Институт пути, строительства и сооружений": "ISTI",
    "Институт железнодорожного транспорта": "IZhT",
    "Институт строительства транспортной инфраструктуры": "ISTI",
    "Институт транспортной техники и систем управления": "ITTSY",
    "Институт управления и цифровых технологий": "IUCT",
    "Институт экономики и финансов": "IEF",
    "Юридический институт": "YUI",
    "Передовая инженерная школа «Академия ВСМ»": "VSM",
}

REQUIRED_COLUMNS = (
    "Постоянная группа",
    "Институт",
    "Код специальности",
    "Специальность",
    "Вид уровня образования",
    "Профиль/специализация/программа",
    "Форма обучения",
    "Дата планового окончания",
)

VALID_LEVELS = {"бакалавриат", "специалитет"}


@dataclass(frozen=True)
class ParsedPermanentGroup:
    """Разобранный код постоянной группы."""

    abbrev: str
    enrollment_year: int
    group_num: str


@dataclass(frozen=True)
class GroupImportRow:
    """Строка отчёта, подготовленная к импорту одной учебной группы."""

    code: str
    name: str
    enrollment_year: int
    course_number: int
    institute_name: str
    institute_code: str
    direction_code: str
    direction_name: str
    direction_level: str
    profile: str
    form: str
    is_end: bool = False


@dataclass(frozen=True)
class ExternalIds:
    """Внешние идентификаторы группы из отчёта 1С."""

    external_group_id: str
    external_permanent_group_id: str


@dataclass(frozen=True)
class ExternalIdsResult:
    """Результат сбора внешних ID для одной постоянной группы."""

    ids: ExternalIds | None
    conflict_reason: str | None = None


@dataclass(frozen=True)
class ContingentRowForExternalIds:
    """Поля строки контингента, нужные для backfill внешних ID."""

    teaching_group_name: str
    course_from_file: str
    external_group_id: str
    external_permanent_group_id: str


def normalize_cell(value: object) -> str:
    """Приводит значение ячейки к строке без лишних пробелов."""
    if value is None:
        return ""
    text = str(value).strip()
    if text.lower() == "nan":
        return ""
    return text


def parse_planned_end_date(value: object) -> date | None:
    """Парсит дату планового окончания из ячейки отчёта 1С."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value

    text = normalize_cell(value)
    if not text:
        return None

    for fmt in ("%d.%m.%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue

    raise ValueError(f"Некорректная дата планового окончания: «{text}»")


def group_ended_by_planned_dates(
    planned_dates: list[date | None],
    *,
    today: date,
) -> bool:
    """
    Возвращает True, если у группы есть хотя бы одна дата окончания
    и все они раньше указанной даты.
    """
    parsed_dates = [
        planned_date for planned_date in planned_dates if planned_date is not None
    ]
    if not parsed_dates:
        return False
    return all(planned_date < today for planned_date in parsed_dates)


def parse_permanent_group_code(code: str) -> ParsedPermanentGroup:
    """
    Разбирает код постоянной группы вида «АМБ-2025-11» или «ОММ-2022-11-1».

    Raises:
        ValueError: если формат кода не распознан.
    """
    cleaned = code.strip()
    match = PERMANENT_GROUP_PATTERN.match(cleaned)
    if not match:
        raise ValueError(f"Некорректный код постоянной группы: «{code}»")

    return ParsedPermanentGroup(
        abbrev=match.group("abbrev"),
        enrollment_year=int(match.group("year")),
        group_num=match.group("num"),
    )


def calculate_course_number(
    *,
    current_year: int,
    enrollment_year: int,
    semester: Semester,
) -> int:
    """Рассчитывает номер курса на текущий учебный год и семестр."""
    course = current_year - enrollment_year + 1
    if semester == "spring":
        course -= 1
    if course < 1:
        raise ValueError(
            f"Некорректный курс {course} "
            f"(год={current_year}, набор={enrollment_year}, semester={semester})"
        )
    return course


def build_group_name(
    *,
    abbrev: str,
    course_number: int,
    group_num: str,
) -> str:
    """Собирает отображаемое название группы, например «АМБ-211»."""
    return f"{abbrev}-{course_number}{group_num}"


def parse_course_from_teaching_group_name(name: str) -> int | None:
    """
    Извлекает номер курса из названия учебной группы, например «ТПВг-341» → 3.

    Предполагается однозначный номер курса в формате «{abbrev}-{course}{group_num}».
    """
    cleaned = normalize_cell(name)
    if not cleaned:
        return None
    match = TEACHING_GROUP_NAME_PATTERN.match(cleaned)
    if not match:
        return None
    return int(match.group("course"))


def parse_course_from_file_value(value: object) -> int | None:
    """Парсит номер курса из колонки «Курс» отчёта."""
    text = normalize_cell(value)
    if not text:
        return None
    try:
        course = int(float(text))
    except ValueError:
        return None
    if course < 1:
        return None
    return course


def is_convergent_contingent_row(
    permanent_code: str,
    teaching_group_name: str,
    course_from_file: object,
    *,
    current_year: int,
    semester: Semester,
) -> bool:
    """
    Возвращает True, если строка относится к «нормальному» потоку:
    учебная группа совпадает с расчётным именем для постоянной группы.
    """
    teaching_name = normalize_cell(teaching_group_name)
    if not teaching_name:
        return True

    try:
        parsed = parse_permanent_group_code(permanent_code)
        course_number = calculate_course_number(
            current_year=current_year,
            enrollment_year=parsed.enrollment_year,
            semester=semester,
        )
        expected_name = build_group_name(
            abbrev=parsed.abbrev,
            course_number=course_number,
            group_num=parsed.group_num,
        )
    except ValueError:
        return False

    if teaching_name != expected_name:
        return False

    file_course = parse_course_from_file_value(course_from_file)
    if file_course is not None and file_course != course_number:
        return False

    return True


def collect_external_ids_for_group(
    rows: list[ContingentRowForExternalIds],
    *,
    permanent_code: str,
    current_year: int,
    semester: Semester,
) -> ExternalIdsResult:
    """
    Собирает внешние ID из сходящихся строк одной постоянной группы.

    Возвращает None, если сходящихся строк нет или ID противоречат друг другу.
    """
    convergent_rows = [
        row
        for row in rows
        if is_convergent_contingent_row(
            permanent_code,
            row.teaching_group_name,
            row.course_from_file,
            current_year=current_year,
            semester=semester,
        )
    ]
    if not convergent_rows:
        return ExternalIdsResult(
            ids=None,
            conflict_reason="нет сходящихся строк",
        )

    group_ids: set[str] = set()
    permanent_ids: set[str] = set()
    for row in convergent_rows:
        if row.external_group_id:
            group_ids.add(row.external_group_id)
        if row.external_permanent_group_id:
            permanent_ids.add(row.external_permanent_group_id)

    if len(group_ids) > 1:
        return ExternalIdsResult(
            ids=None,
            conflict_reason=f"конфликт ID группы: {sorted(group_ids)}",
        )
    if len(permanent_ids) > 1:
        return ExternalIdsResult(
            ids=None,
            conflict_reason=f"конфликт ID постоянной группы: {sorted(permanent_ids)}",
        )
    if not group_ids:
        return ExternalIdsResult(
            ids=None,
            conflict_reason="нет ID группы в сходящихся строках",
        )

    return ExternalIdsResult(
        ids=ExternalIds(
            external_group_id=next(iter(group_ids)),
            external_permanent_group_id=(
                next(iter(permanent_ids)) if permanent_ids else ""
            ),
        ),
    )


def resolve_institute_code(institute_name: str) -> str:
    """
    Возвращает код института по полному названию из отчёта 1С.

    Raises:
        ValueError: если институт не найден в справочнике маппинга.
    """
    cleaned = institute_name.strip()
    if not cleaned:
        raise ValueError("Пустое название института")

    code = INSTITUTE_NAME_TO_CODE.get(cleaned)
    if code is None:
        raise ValueError(f"Неизвестный институт: «{cleaned}»")
    return code


def parse_direction_level(level_raw: str) -> str:
    """
    Нормализует уровень подготовки из отчёта.

    Raises:
        ValueError: если уровень не поддерживается.
    """
    cleaned = level_raw.strip().lower()
    if cleaned not in VALID_LEVELS:
        raise ValueError(f"Недопустимый уровень подготовки: «{level_raw}»")
    return cleaned


def build_group_import_row(
    *,
    permanent_group_code: str,
    institute_name: str,
    direction_code: str,
    direction_name: str,
    direction_level: str,
    profile: str,
    form: str,
    current_year: int,
    semester: Semester,
) -> GroupImportRow:
    """Собирает DTO одной группы из полей строки отчёта."""
    parsed = parse_permanent_group_code(permanent_group_code)
    course_number = calculate_course_number(
        current_year=current_year,
        enrollment_year=parsed.enrollment_year,
        semester=semester,
    )
    institute_code = resolve_institute_code(institute_name)
    level = parse_direction_level(direction_level)

    if not direction_code.strip():
        raise ValueError("Пустой код специальности")
    if not direction_name.strip():
        raise ValueError("Пустое название специальности")

    return GroupImportRow(
        code=permanent_group_code.strip(),
        name=build_group_name(
            abbrev=parsed.abbrev,
            course_number=course_number,
            group_num=parsed.group_num,
        ),
        enrollment_year=parsed.enrollment_year,
        course_number=course_number,
        institute_name=institute_name.strip(),
        institute_code=institute_code,
        direction_code=direction_code.strip(),
        direction_name=direction_name.strip(),
        direction_level=level,
        profile=profile.strip(),
        form=form.strip(),
    )

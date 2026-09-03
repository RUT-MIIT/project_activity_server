"""Чистая логика импорта учебных групп из отчёта контингента 1С."""

from __future__ import annotations

from dataclasses import dataclass, replace
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
    "ID группы",
    "Группа",
)

VALID_LEVELS = {"бакалавриат", "специалитет"}

# Постоянные группы, полностью исключённые из импорта (группы и студенты).
SKIPPED_PERMANENT_GROUP_CODES: frozenset[str] = frozenset()

# Префиксы постоянных групп для исключения из импорта (например, все ТУП-*).
# Исключение снимается для ID из STUDY_GROUP_OVERRIDES_BY_EXTERNAL_ID.
SKIPPED_PERMANENT_GROUP_PREFIXES: tuple[str, ...] = ("ТУП-",)

# Имена учебных групп (StudyGroup.name), исключённые из импорта групп и студентов.
SKIPPED_STUDY_GROUP_NAMES: frozenset[str] = frozenset(
    {
        "ОММ-221",
        "ОММ-321",
        "ОММ-421",
        "ОММ-521",
        "ОММу-221",
        "ОММу-321",
        "ОММу-421",
    }
)

# Переименование учебных групп: расчётное имя из 1С → имя в БД.
STUDY_GROUP_NAME_OVERRIDES: dict[str, str] = {}

# Переименование по коду постоянной группы (приоритетнее STUDY_GROUP_NAME_OVERRIDES).
STUDY_GROUP_NAME_OVERRIDES_BY_CODE: dict[str, str] = {}

# Замена аббревиатуры в имени группы: ЭБП-211 → ЭПТ-211.
GROUP_ABBREV_RENAMES: dict[str, str] = {
    "ЭБП": "ЭПТ",
}


@dataclass(frozen=True)
class StudyGroupFieldOverride:
    """Ручная правка полей учебной группы по ID группы из 1С."""

    name: str | None = None
    institute_name: str | None = None


# Переопределение полей до записи в БД: ключ — ID группы (1С).
# Также снимает исключение ТУП-/SKIPPED для этих ID.
STUDY_GROUP_OVERRIDES_BY_EXTERNAL_ID: dict[str, StudyGroupFieldOverride] = {
    "149820": StudyGroupFieldOverride(
        name="ЭПО-211",
        institute_name="Институт экономики и финансов",
    ),
    "140100": StudyGroupFieldOverride(
        name="ЭПО-311",
        institute_name="Институт экономики и финансов",
    ),
    "139672": StudyGroupFieldOverride(
        name="ЭПО-411",
        institute_name="Институт экономики и финансов",
    ),
}

# Слияние учебных групп: исходный ID группы (1С) → целевой ID.
# Студенты с исходным ID привязываются к целевой группе; исходная не создаётся.
EXTERNAL_GROUP_ID_REMAP: dict[str, str] = {
    "193902": "193901",  # ТСТ-442 → ТСТ-441
}


@dataclass(frozen=True)
class ParsedPermanentGroup:
    """Разобранный код постоянной группы."""

    abbrev: str
    enrollment_year: int
    group_num: str


@dataclass(frozen=True)
class GroupImportRow:
    """Строка отчёта, подготовленная к импорту одной учебной группы."""

    external_group_id: str
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
    external_permanent_group_id: str = ""
    is_end: bool = False


@dataclass(frozen=True)
class ExistingGroupCandidate:
    """Кандидат StudyGroup для claim без зависимости от ORM."""

    pk: int
    code: str
    name: str
    external_group_id: str


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


def normalize_external_group_id(value: object) -> str:
    """Нормализует ID группы из 1С до строки без дробной части."""
    text = normalize_cell(value)
    if not text:
        return ""
    try:
        return str(int(float(text)))
    except ValueError:
        return text


def remap_external_group_id(value: object) -> str:
    """
    Нормализует ID группы и применяет EXTERNAL_GROUP_ID_REMAP.

    Используется при импорте студентов (и при решении, создавать ли группу).
    """
    normalized = normalize_external_group_id(value)
    if not normalized:
        return ""
    return EXTERNAL_GROUP_ID_REMAP.get(normalized, normalized)


def is_external_group_id_remapped_away(value: object) -> bool:
    """True, если ID слит в другую группу и отдельную StudyGroup создавать не нужно."""
    normalized = normalize_external_group_id(value)
    if not normalized:
        return False
    target = EXTERNAL_GROUP_ID_REMAP.get(normalized)
    return target is not None and target != normalized


def get_study_group_override_by_external_id(
    external_group_id: object,
) -> StudyGroupFieldOverride | None:
    """Возвращает ручной оверрайд по ID группы или None."""
    normalized = normalize_external_group_id(external_group_id)
    if not normalized:
        return None
    return STUDY_GROUP_OVERRIDES_BY_EXTERNAL_ID.get(normalized)


def apply_study_group_override_by_external_id(
    row: GroupImportRow,
    external_group_id: object,
) -> GroupImportRow:
    """
    Переписывает name/институт по STUDY_GROUP_OVERRIDES_BY_EXTERNAL_ID.

    Вызывается до записи в БД. Неизвестный ID оставляет row без изменений.
    """
    override = get_study_group_override_by_external_id(external_group_id)
    if override is None:
        return row

    name = row.name
    institute_name = row.institute_name
    institute_code = row.institute_code

    if override.name:
        name = normalize_cell(override.name)
    if override.institute_name:
        institute_name = normalize_cell(override.institute_name)
        institute_code = resolve_institute_code(institute_name)

    return replace(
        row,
        name=name,
        institute_name=institute_name,
        institute_code=institute_code,
    )


def is_skipped_permanent_group(permanent_group_code: str) -> bool:
    """Возвращает True, если постоянная группа исключена из импорта."""
    code = normalize_cell(permanent_group_code)
    if code in SKIPPED_PERMANENT_GROUP_CODES:
        return True
    return any(code.startswith(prefix) for prefix in SKIPPED_PERMANENT_GROUP_PREFIXES)


def is_skipped_study_group_name(study_group_name: str) -> bool:
    """Возвращает True, если учебная группа исключена из импорта по имени."""
    return normalize_cell(study_group_name) in SKIPPED_STUDY_GROUP_NAMES


def apply_group_abbrev_renames(name: str) -> str:
    """Заменяет аббревиатуру в начале имени учебной группы, например ЭБП → ЭПТ."""
    cleaned = normalize_cell(name)
    if not cleaned:
        return ""
    for old_abbrev, new_abbrev in GROUP_ABBREV_RENAMES.items():
        prefix = f"{old_abbrev}-"
        if cleaned.startswith(prefix):
            return f"{new_abbrev}-{cleaned[len(prefix):]}"
    return cleaned


def resolve_study_group_display_name(
    *,
    calculated_name: str,
    permanent_group_code: str,
) -> str:
    """
    Возвращает имя учебной группы для сохранения в БД.

    Приоритет: переименование по коду постоянной группы → по расчётному имени.
    """
    code = normalize_cell(permanent_group_code)
    by_code = STUDY_GROUP_NAME_OVERRIDES_BY_CODE.get(code)
    if by_code:
        return apply_group_abbrev_renames(by_code)

    name = normalize_cell(calculated_name)
    renamed = STUDY_GROUP_NAME_OVERRIDES.get(name, name)
    return apply_group_abbrev_renames(renamed)


def map_teaching_group_name_for_lookup(teaching_group_name: str) -> str:
    """Преобразует имя из колонки «Группа» к имени в БД для поиска группы."""
    name = normalize_cell(teaching_group_name)
    if not name:
        return ""
    renamed = STUDY_GROUP_NAME_OVERRIDES.get(name, name)
    return apply_group_abbrev_renames(renamed)


def collect_teaching_group_names_in_file(values: list[object]) -> set[str]:
    """
    Собирает имена учебных групп из колонки «Группа» отчёта.

    Имена нормализуются так же, как при поиске StudyGroup по name.
    Пустые и исключённые имена пропускаются.
    """
    names: set[str] = set()
    for value in values:
        mapped = map_teaching_group_name_for_lookup(value)
        if not mapped:
            continue
        if is_skipped_study_group_name(mapped):
            continue
        names.add(mapped)
    return names


def should_keep_missing_group_alive(
    *,
    group_code: str,
    group_name: str,
    imported_codes: set[str],
    teaching_names_in_file: set[str],
) -> bool:
    """
    True, если группу без кода в текущем импорте нельзя помечать is_end.

    Группа остаётся живой, пока её name встречается в колонке «Группа»
    (например, ТКИ-241 при постоянной ТКИ-2024-41 и year=2026).
    """
    code = normalize_cell(group_code)
    if not code or code in imported_codes:
        return False
    if is_skipped_permanent_group(code):
        return False
    name = normalize_cell(group_name)
    if not name or is_skipped_study_group_name(name):
        return False
    return name in teaching_names_in_file


def is_skipped_teaching_group_name(teaching_group_name: str) -> bool:
    """Проверяет имя из колонки «Группа» с учётом переименований для БД."""
    name = normalize_cell(teaching_group_name)
    if not name:
        return False
    if is_skipped_study_group_name(name):
        return True
    return is_skipped_study_group_name(map_teaching_group_name_for_lookup(name))


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


def resolve_existing_group_for_id(
    candidates: list[ExistingGroupCandidate],
    *,
    external_id: str,
    permanent_code: str,
    teaching_name: str,
    ids_per_permanent: dict[str, set[str]],
    claimed_pks: set[int],
) -> ExistingGroupCandidate | None:
    """
    Подбирает существующую StudyGroup для ID группы из 1С.

    Приоритет:
    1. уже с этим external_group_id;
    2. незанятая с code=постоянная и name=учебная группа;
    3. единственная незанятая с этим code, если у постоянной ровно один ID в файле.
    """
    target_id = remap_external_group_id(external_id)
    if not target_id:
        return None

    for candidate in candidates:
        if candidate.external_group_id == target_id:
            return candidate

    permanent = normalize_cell(permanent_code)
    lookup_name = map_teaching_group_name_for_lookup(teaching_name)
    unclaimed = [
        candidate
        for candidate in candidates
        if candidate.pk not in claimed_pks
        and not candidate.external_group_id
        and normalize_cell(candidate.code) == permanent
    ]
    if not unclaimed:
        return None

    name_matches = [
        candidate
        for candidate in unclaimed
        if normalize_cell(candidate.name) == lookup_name
    ]
    if len(name_matches) == 1:
        return name_matches[0]
    if len(name_matches) > 1:
        return name_matches[0]

    permanent_ids = ids_per_permanent.get(permanent, set())
    if len(permanent_ids) == 1 and len(unclaimed) == 1:
        return unclaimed[0]
    return None


def build_group_import_row(
    *,
    permanent_group_code: str,
    teaching_group_name: str,
    institute_name: str,
    direction_code: str,
    direction_name: str,
    direction_level: str,
    profile: str,
    form: str,
    external_group_id: object,
    course_from_file: object = "",
    external_permanent_group_id: object = "",
) -> GroupImportRow:
    """
    Собирает DTO одной группы из полей строки отчёта.

    Identity — ID группы из 1С; имя — колонка «Группа» (с оверрайдами).
    """
    remapped_id = remap_external_group_id(external_group_id)
    if not remapped_id:
        raise ValueError("Пустой ID группы")
    if is_external_group_id_remapped_away(external_group_id):
        raise ValueError(
            f"ID группы «{normalize_external_group_id(external_group_id)}» "
            f"слит в «{remapped_id}»"
        )

    permanent = normalize_cell(permanent_group_code)
    if not permanent:
        raise ValueError("Пустая постоянная группа")

    parsed = parse_permanent_group_code(permanent)
    teaching_name = map_teaching_group_name_for_lookup(teaching_group_name)
    if not teaching_name:
        raise ValueError("Пустое имя учебной группы («Группа»)")

    file_course = parse_course_from_file_value(course_from_file)
    if file_course is None:
        name_course = parse_course_from_teaching_group_name(teaching_name)
        if name_course is None:
            raise ValueError(f"Не удалось определить курс для группы «{teaching_name}»")
        course_number = name_course
    else:
        course_number = file_course

    row_institute = normalize_cell(institute_name)
    override = get_study_group_override_by_external_id(remapped_id)
    if not row_institute and override is not None and override.institute_name:
        row_institute = normalize_cell(override.institute_name)
    if not row_institute:
        raise ValueError("Пустое название института")

    institute_code = resolve_institute_code(row_institute)
    level = parse_direction_level(direction_level)

    if not direction_code.strip():
        raise ValueError("Пустой код специальности")
    if not direction_name.strip():
        raise ValueError("Пустое название специальности")

    display_name = resolve_study_group_display_name(
        calculated_name=teaching_name,
        permanent_group_code=permanent,
    )

    row = GroupImportRow(
        external_group_id=remapped_id,
        code=permanent,
        name=display_name,
        enrollment_year=parsed.enrollment_year,
        course_number=course_number,
        institute_name=row_institute,
        institute_code=institute_code,
        direction_code=direction_code.strip(),
        direction_name=direction_name.strip(),
        direction_level=level,
        profile=profile.strip(),
        form=form.strip(),
        external_permanent_group_id=normalize_external_group_id(
            external_permanent_group_id
        ),
    )
    return apply_study_group_override_by_external_id(row, remapped_id)

from dataclasses import dataclass, field
from typing import Literal

SUBJECT_NAME = "Проектная деятельность"

GroupStatus = Literal[
    "найдено",
    "нет занятий",
    "нет расписания",
    "ошибка загрузки",
]


@dataclass(frozen=True)
class GroupInfo:
    institute: str
    institute_abbr: str
    course: str
    specialty: str
    specialty_abbr: str
    group_id: int
    group_name: str


@dataclass(frozen=True)
class TeacherInfo:
    id: int
    full_fio: str
    short_fio: str
    lesson_count: int = 0


@dataclass
class GroupResult:
    group: GroupInfo
    status: GroupStatus
    semester: str = ""
    teachers: list[TeacherInfo] = field(default_factory=list)
    lesson_count: int = 0
    error: str = ""

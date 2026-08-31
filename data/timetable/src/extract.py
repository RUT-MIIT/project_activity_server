from typing import Any

from src.api import RutMiitClient
from src.models import SUBJECT_NAME, GroupInfo, GroupResult, TeacherInfo


def flatten_groups_catalog(catalog: dict[str, Any]) -> list[GroupInfo]:
    groups: list[GroupInfo] = []
    for institute in catalog.get("institutes", []):
        institute_name = institute.get("name", "")
        institute_abbr = institute.get("abbreviation", "")
        for course in institute.get("courses", []):
            course_name = str(course.get("course", ""))
            for specialty in course.get("specialties", []):
                specialty_name = specialty.get("name", "")
                specialty_abbr = specialty.get("abbreviation", "")
                for group in specialty.get("groups", []):
                    groups.append(
                        GroupInfo(
                            institute=institute_name,
                            institute_abbr=institute_abbr,
                            course=course_name,
                            specialty=specialty_name,
                            specialty_abbr=specialty_abbr,
                            group_id=int(group["id"]),
                            group_name=group.get("name", ""),
                        )
                    )
    return groups


def _select_timetable(timetables: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not timetables:
        return None

    for timetable in timetables:
        if timetable.get("selected"):
            return timetable

    for timetable in timetables:
        if timetable.get("actual"):
            return timetable

    return timetables[0]


def _collect_events(schedule: dict[str, Any]) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []

    periodic = schedule.get("periodicContent")
    if isinstance(periodic, dict):
        events.extend(periodic.get("events", []))

    non_periodic = schedule.get("nonPeriodicContent")
    if isinstance(non_periodic, dict):
        events.extend(non_periodic.get("events", []))

    return events


def _extract_teachers(events: list[dict[str, Any]]) -> tuple[list[TeacherInfo], int]:
    teachers_by_id: dict[int, tuple[str, str]] = {}
    lesson_counts: dict[int, int] = {}
    total_lesson_count = 0

    for event in events:
        if event.get("name") != SUBJECT_NAME:
            continue

        total_lesson_count += 1
        for lecturer in event.get("lecturers", []):
            lecturer_id = lecturer.get("id")
            if lecturer_id is None:
                continue
            lecturer_id = int(lecturer_id)
            lesson_counts[lecturer_id] = lesson_counts.get(lecturer_id, 0) + 1
            teachers_by_id[lecturer_id] = (
                lecturer.get("fullFio", ""),
                lecturer.get("shortFio", ""),
            )

    teachers = [
        TeacherInfo(
            id=lecturer_id,
            full_fio=full_fio,
            short_fio=short_fio,
            lesson_count=lesson_counts[lecturer_id],
        )
        for lecturer_id, (full_fio, short_fio) in teachers_by_id.items()
    ]
    return teachers, total_lesson_count


async def fetch_group_result(client: RutMiitClient, group: GroupInfo) -> GroupResult:
    try:
        timetables_response = await client.get_group_timetables(group.group_id)
        timetable = _select_timetable(timetables_response.get("timetables", []))
        if timetable is None:
            return GroupResult(group=group, status="нет расписания")

        semester = timetable.get("eduStageDisplay", "")
        schedule = await client.get_group_schedule(group.group_id, timetable["id"])
        events = _collect_events(schedule)
        teachers, lesson_count = _extract_teachers(events)

        if not teachers:
            return GroupResult(
                group=group,
                status="нет занятий",
                semester=semester,
                lesson_count=0,
            )

        return GroupResult(
            group=group,
            status="найдено",
            semester=semester,
            teachers=teachers,
            lesson_count=lesson_count,
        )
    except Exception as exc:
        return GroupResult(
            group=group,
            status="ошибка загрузки",
            error=str(exc),
        )

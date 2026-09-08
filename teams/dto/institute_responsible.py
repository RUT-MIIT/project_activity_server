"""DTO для API ответственного по институтам."""

from __future__ import annotations

from typing import Any

from accounts.models import PreRegisteredStudent, User
from showcase.models import Institute, InstituteSemesterSettings, ProjectApplication
from teams.domain.institute_responsible import InstituteResponsibleDomain
from teams.domain.team_lobby import TeamLobbyDomain
from teams.models import StudyGroup, TeamSemester, TeamSemesterMember


def _mentors_from_group(group: StudyGroup | None) -> list[dict[str, Any]]:
    """Список наставников группы из prefetch семестра."""
    if group is None:
        return []
    enrollments = getattr(group, "_semester_enrollments_for_semester", None)
    if not enrollments:
        return []
    enrollment = enrollments[0]
    return [
        InstituteResponsibleEmployeeDTO(mentor).to_dict()
        for mentor in enrollment.mentors.all()
    ]


def _project_snapshot(application: ProjectApplication | None) -> dict[str, Any] | None:
    """Краткое представление выбранного проекта."""
    if application is None:
        return None
    return {
        "id": application.id,
        "title": application.title or "",
    }


class InstituteResponsibleGroupDTO:
    """Компактное представление учебной группы."""

    def __init__(self, group: StudyGroup) -> None:
        self.id = group.id
        self.name = group.name
        self.course_number = group.course_number
        self.direction_code = group.direction.code

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "courseNumber": self.course_number,
            "directionCode": self.direction_code,
        }


class InstituteResponsibleEmployeeDTO:
    """Сотрудник института (id + ФИО)."""

    def __init__(self, user: User) -> None:
        self.id = user.id
        self.full_name = user.get_full_name()

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "fullName": self.full_name,
        }


class InstituteResponsibleMentorDTO:
    """Назначенный наставник группы (полная карточка)."""

    def __init__(self, mentor: User | None) -> None:
        self.mentor = mentor

    def to_dict(self) -> dict[str, Any] | None:
        if self.mentor is None:
            return None
        return InstituteResponsibleEmployeeDTO(self.mentor).to_dict()


class InstituteResponsibleGroupWithMentorDTO:
    """Учебная группа с ID назначенных наставников в семестре."""

    def __init__(self, group: StudyGroup) -> None:
        self.id = group.id
        self.name = group.name
        self.course_number = group.course_number
        self.direction_code = group.direction.code
        self.mentor_ids = self._mentor_ids_for_group(group)

    @staticmethod
    def _mentor_ids_for_group(group: StudyGroup) -> list[int]:
        enrollments = getattr(group, "_semester_enrollments_for_semester", None)
        if not enrollments:
            return []
        enrollment = enrollments[0]
        return [mentor.id for mentor in enrollment.mentors.all()]

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "courseNumber": self.course_number,
            "directionCode": self.direction_code,
            "mentorIds": self.mentor_ids,
        }


class InstituteResponsibleGroupMentorsDTO:
    """Ответ: группы с назначениями наставников."""

    def __init__(self, groups: list[StudyGroup]) -> None:
        self.groups = groups

    def to_list(self) -> list[dict[str, Any]]:
        return [
            InstituteResponsibleGroupWithMentorDTO(group).to_dict()
            for group in self.groups
        ]


class InstituteResponsibleAssignMentorDTO:
    """Ответ после изменения состава наставников."""

    def __init__(self, group_id: int, semester_id: int, mentor_ids: list[int]) -> None:
        self.group_id = group_id
        self.semester_id = semester_id
        self.mentor_ids = mentor_ids

    def to_dict(self) -> dict[str, Any]:
        return {
            "groupId": self.group_id,
            "semesterId": self.semester_id,
            "mentorIds": self.mentor_ids,
        }


class InstituteResponsibleTeamListItemDTO:
    """Строка списка команд института в семестре."""

    def __init__(self, team_semester: TeamSemester) -> None:
        group = team_semester.team.home_study_group
        self.id = team_semester.id
        self.name = team_semester.team.name
        self.study_group = (
            {"id": group.id, "name": group.name} if group is not None else None
        )
        self.mentors = _mentors_from_group(group)
        self.status = team_semester.status
        self.members_count = int(getattr(team_semester, "members_count", 0) or 0)
        self.project = _project_snapshot(team_semester.project_application)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "studyGroup": self.study_group,
            "mentors": self.mentors,
            "status": self.status,
            "membersCount": self.members_count,
            "project": self.project,
        }


class InstituteResponsibleTeamDetailDTO:
    """Подробная карточка команды института."""

    def __init__(self, team_semester: TeamSemester) -> None:
        base = InstituteResponsibleTeamListItemDTO(team_semester)
        self._base = base.to_dict()
        captain = team_semester.captain
        self.captain = {
            "userId": captain.id,
            "fullName": TeamLobbyDomain.user_display_name(captain),
        }
        self.members = [
            {
                "userId": membership.user_id,
                "fullName": TeamLobbyDomain.user_display_name(membership.user),
                "role": membership.role,
            }
            for membership in team_semester.members.all()
        ]

    def to_dict(self) -> dict[str, Any]:
        result = dict(self._base)
        result["captain"] = self.captain
        result["members"] = self.members
        return result


class InstituteResponsibleStudentDTO:
    """Студент контингента института для списка ответственного."""

    def __init__(self, pre_registered: PreRegisteredStudent) -> None:
        group = pre_registered.group
        student = pre_registered.user
        self.id = pre_registered.id
        self.last_name = pre_registered.last_name
        self.first_name = pre_registered.first_name
        self.middle_name = pre_registered.middle_name
        self.is_registered = pre_registered.is_registered
        self.study_group = (
            {"id": group.id, "name": group.name} if group is not None else None
        )
        self.mentors = _mentors_from_group(group)
        self.team_name: str | None = None
        self.team_role: str | None = None
        self.project: dict[str, Any] | None = None
        self._fill_team(student)

    def _fill_team(self, student: User | None) -> None:
        if student is None:
            return
        memberships: list[TeamSemesterMember] = getattr(
            student, "_team_membership_for_semester", []
        )
        if not memberships:
            return
        membership = memberships[0]
        self.team_name = membership.team_semester.team.name
        self.team_role = membership.role
        self.project = _project_snapshot(membership.team_semester.project_application)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "lastName": self.last_name,
            "firstName": self.first_name,
            "middleName": self.middle_name,
            "isRegistered": self.is_registered,
            "studyGroup": self.study_group,
            "mentors": self.mentors,
            "teamName": self.team_name,
            "teamRole": self.team_role,
            "project": self.project,
        }


class InstituteResponsibleRegistrationSettingsDTO:
    """Ответ GET/POST настроек регистрации институтов в семестре."""

    def __init__(
        self,
        *,
        current_institute: Institute,
        current_settings: InstituteSemesterSettings | None,
        other_institutes: list[Institute],
        settings_by_code: dict[str, InstituteSemesterSettings],
    ) -> None:
        self.current_institute = current_institute
        self.current_settings = current_settings
        self.other_institutes = other_institutes
        self.settings_by_code = settings_by_code

    def _current_dict(self) -> dict[str, Any]:
        settings = self.current_settings
        is_open = InstituteResponsibleDomain.is_registration_open(settings)
        return {
            "instituteCode": self.current_institute.code,
            "instituteName": self.current_institute.name,
            "registrationOpensAt": (
                settings.registration_opens_at.isoformat()
                if settings and settings.registration_opens_at
                else None
            ),
            "closedByDecision": (
                settings.closed_by_decision if settings is not None else False
            ),
            "isOpen": is_open,
            "status": "open" if is_open else "closed",
        }

    def _other_list(self) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = []
        for institute in self.other_institutes:
            settings = self.settings_by_code.get(institute.code)
            items.append(
                {
                    "instituteCode": institute.code,
                    "instituteName": institute.name,
                    "registrationOpensAt": (
                        settings.registration_opens_at.isoformat()
                        if settings and settings.registration_opens_at
                        else None
                    ),
                }
            )
        return items

    def to_dict(self) -> dict[str, Any]:
        return {
            "current": self._current_dict(),
            "otherInstitutes": self._other_list(),
        }

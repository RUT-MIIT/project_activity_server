"""Доменная логика студенческой витрины проектов."""

from __future__ import annotations

from typing import TYPE_CHECKING

from teams.domain.team_lobby import TeamLobbyDomain
from teams.models import TeamSemester

if TYPE_CHECKING:
    from accounts.models import User
    from showcase.models import ProjectApplication


class StudentShowcaseDomain:
    """Правила доступа и записи команды на проект витрины."""

    @staticmethod
    def ensure_student_with_group(user: User) -> int:
        """Проверяет роль student и наличие учебной группы; возвращает group_id."""
        return TeamLobbyDomain.ensure_student_with_group(user)

    @staticmethod
    def ensure_is_captain(user: User, team_semester: TeamSemester) -> None:
        """Проверяет, что пользователь — капитан команды."""
        TeamLobbyDomain.ensure_is_captain(user, team_semester)

    @staticmethod
    def ensure_team_assembled(team_semester: TeamSemester) -> None:
        """Запись на проект доступна только при подтверждённом составе."""
        if team_semester.status != TeamSemester.Status.ASSEMBLED:
            raise ValueError(
                "Запись на проект доступна только после подтверждения состава команды"
            )

    @staticmethod
    def ensure_no_project_yet(team_semester: TeamSemester) -> None:
        """Запрещает повторную запись / смену проекта."""
        if team_semester.project_application_id is not None:
            raise ValueError("Команда уже записана на проект")

    @staticmethod
    def ensure_project_in_team_track(
        team_semester: TeamSemester, track_id: int
    ) -> None:
        """Совместимость с прежним API: трек проставляется при enroll.

        Проверка «проект ∈ трек команды» больше не требуется: команда может
        быть без трека или сменить трек при записи на проект.
        """
        _ = (team_semester, track_id)

    @staticmethod
    def ensure_members_fit_project(
        *,
        members_count: int,
        application: ProjectApplication,
    ) -> None:
        """Число участников должно укладываться в лимиты проекта."""
        min_members = application.min_team_members
        max_members = application.max_team_members
        if not (min_members <= members_count <= max_members):
            raise ValueError(
                "Число участников команды должно быть в пределах "
                f"{min_members}–{max_members} для этого проекта"
            )

    @staticmethod
    def ensure_enrollment_slot_available(
        *,
        enrolled_count: int,
        max_teams: int,
    ) -> None:
        """Жёсткий лимит числа команд на проект."""
        if enrolled_count >= max_teams:
            raise ValueError("На проект уже записано максимальное число команд")

    @staticmethod
    def ensure_institute_registration_open(*, is_open: bool) -> None:
        """Запрещает запись, если окно регистрации института закрыто."""
        if not is_open:
            raise ValueError(
                "Запись на проекты закрыта для вашего института в этом семестре"
            )

    @staticmethod
    def ensure_mentor_registration_schedule_open(
        *, is_opened_by_schedule: bool
    ) -> None:
        """Для наставника: дата открытия должна наступить.

        closed_by_decision не блокирует запись наставником.
        """
        if not is_opened_by_schedule:
            raise ValueError(
                "Запись на проекты ещё не открыта для института в этом семестре"
            )

    @staticmethod
    def build_mentor_enroll_log_text(
        *,
        application_title: str,
        previous_title: str | None,
    ) -> str:
        """Текст события лога при записи/смене проекта наставником."""
        if previous_title is not None:
            return (
                f"Наставник сменил проект команды с «{previous_title}» "
                f"на «{application_title}»"
            )
        return f"Наставник записал команду на проект «{application_title}»"

    @classmethod
    def can_enroll(
        cls,
        *,
        is_captain: bool,
        status: str,
        has_project: bool,
        members_count: int,
        min_team_members: int,
        max_team_members: int,
        enrolled_count: int,
        max_teams: int,
        project_track_id: int | None,
        application_track_id: int | None,
        registration_open: bool = True,
    ) -> bool:
        """True, если капитан может записать команду на проект (для UI)."""
        _ = project_track_id
        if not is_captain:
            return False
        if status != TeamSemester.Status.ASSEMBLED:
            return False
        if has_project:
            return False
        if application_track_id is None:
            return False
        if not (min_team_members <= members_count <= max_team_members):
            return False
        if enrolled_count >= max_teams:
            return False
        if not registration_open:
            return False
        return True

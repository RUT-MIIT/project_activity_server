"""Доменные правила управления командой наставником."""

from __future__ import annotations

from teams.models import TeamSemester, TeamSemesterMember


class TeamEnrolledInProjectError(PermissionError):
    """Команда записана на проект — мутации запрещены."""


class MentorTeamDomain:
    """Чистая бизнес-логика API команд наставника."""

    @staticmethod
    def ensure_team_belongs_to_group(
        team_semester: TeamSemester, group_id: int
    ) -> None:
        """Проверяет, что команда принадлежит учебной группе."""
        if team_semester.team.home_study_group_id != group_id:
            raise LookupError("Команда не найдена в этой учебной группе")

    @staticmethod
    def ensure_not_enrolled_in_project(team_semester: TeamSemester) -> None:
        """Запрещает изменения, если команда записана на проект."""
        if team_semester.project_application_id is not None:
            raise TeamEnrolledInProjectError("Сначала отпишите команду от проекта")

    @staticmethod
    def ensure_can_confirm(
        *,
        status: str,
        members_count: int,
        min_team_members: int,
        max_team_members: int,
    ) -> None:
        """Проверяет возможность подтверждения состава."""
        if status != TeamSemester.Status.FORMING:
            raise ValueError("Состав уже подтверждён")
        if not min_team_members <= members_count <= max_team_members:
            raise ValueError(
                "Число участников должно быть в пределах "
                f"{min_team_members}–{max_team_members}"
            )

    @staticmethod
    def ensure_can_unconfirm(status: str) -> None:
        """Проверяет возможность разутверждения состава."""
        if status != TeamSemester.Status.ASSEMBLED:
            raise ValueError("Состав команды ещё не подтверждён")

    @staticmethod
    def ensure_can_delete_team(members_count: int) -> None:
        """Удаление возможно только при пустом составе."""
        if members_count != 0:
            raise ValueError("Перед удалением команды нужно исключить всех участников")

    @staticmethod
    def ensure_captain_is_member(
        team_semester: TeamSemester, captain_user_id: int
    ) -> None:
        """Новый капитан должен быть участником команды."""
        member_ids = {member.user_id for member in team_semester.members.all()}
        if captain_user_id not in member_ids:
            raise ValueError("Капитаном может быть только участник команды")

    @staticmethod
    def ensure_not_captain_removal(
        team_semester: TeamSemester, member_user_id: int
    ) -> None:
        """Нельзя удалить текущего капитана без смены капитана."""
        if team_semester.captain_id == member_user_id:
            raise ValueError("Сначала назначьте нового капитана")

    @staticmethod
    def ensure_student_role(role_code: str | None) -> None:
        """Добавлять в команду можно только студентов."""
        if role_code != "student":
            raise ValueError("В команду можно добавить только студента")

    @staticmethod
    def ensure_same_study_group(user_group_id: int | None, group_id: int) -> None:
        """Студент должен быть из учебной группы наставника."""
        if user_group_id != group_id:
            raise ValueError("Студент должен быть из этой учебной группы")

    @staticmethod
    def ensure_create_payload(name: str, captain_id: int) -> tuple[str, int]:
        """Валидирует название и ID капитана при создании команды."""
        cleaned_name = name.strip()
        if not cleaned_name:
            raise ValueError("Название команды не может быть пустым")
        if captain_id < 1:
            raise ValueError("Некорректный captainId")
        return cleaned_name, captain_id

    @staticmethod
    def resolve_add_role(members_count: int) -> str:
        """Первый участник пустой команды становится капитаном."""
        if members_count == 0:
            return TeamSemesterMember.Role.LEADER
        return TeamSemesterMember.Role.MEMBER

"""Сервис управления командой учебной группы для наставника."""

from __future__ import annotations

from typing import Any

from django.contrib.auth import get_user_model
from django.db import transaction

from accounts.models import Semester
from accounts.repositories.preregistered_student import PreRegisteredStudentRepository
from accounts.services.placeholder_user_service import PlaceholderUserService
from teams.domain.mentor_groups import MentorGroupsDomain
from teams.domain.mentor_team import MentorTeamDomain
from teams.domain.team_lobby import TeamLobbyDomain
from teams.dto.mentor_team import MentorTeamDetailDTO
from teams.models import TeamSemester, TeamSemesterMember
from teams.repositories.mentor_groups import MentorGroupsRepository
from teams.repositories.mentor_team import MentorTeamRepository

User = get_user_model()


class MentorTeamService:
    """Операции наставника над командой группы в семестре."""

    def __init__(self) -> None:
        self.repository = MentorTeamRepository()
        self.groups_repository = MentorGroupsRepository()
        self.pre_registered_repository = PreRegisteredStudentRepository()
        self.placeholder_service = PlaceholderUserService()
        self.groups_domain = MentorGroupsDomain()
        self.domain = MentorTeamDomain()
        self.lobby_domain = TeamLobbyDomain()

    def _to_detail(self, team_semester: TeamSemester) -> dict[str, Any]:
        """Сериализует карточку команды."""
        return MentorTeamDetailDTO(team_semester).to_dict()

    def _authorize_and_load(
        self,
        user: User,
        *,
        group_id: int,
        team_semester_id: int,
        semester_id_raw: str | None,
        check_project_enrollment: bool = True,
    ) -> tuple[int, TeamSemester]:
        """Проверяет доступ наставника и загружает команду."""
        semester_id = Semester.resolve_list_semester_id(semester_id_raw)
        group = self.groups_repository.get_group_header(group_id)
        self.groups_domain.ensure_group_exists(group)
        is_mentor = self.groups_repository.is_mentor(user.id, group_id, semester_id)
        self.groups_domain.ensure_mentor_access(is_mentor)

        team_semester = self.repository.get_team_semester_detail(
            team_semester_id=team_semester_id,
            group_id=group_id,
            semester_id=semester_id,
        )
        if team_semester is None:
            raise LookupError("Команда не найдена")
        self.domain.ensure_team_belongs_to_group(team_semester, group_id)
        if check_project_enrollment:
            self.domain.ensure_not_enrolled_in_project(team_semester)
        return semester_id, team_semester

    def _member_limits(
        self, team_semester: TeamSemester, group_id: int, semester_id: int
    ) -> tuple[int, int]:
        """Лимиты размера команды для группы в семестре."""
        group_tracks = self.repository.list_group_tracks(
            group_id=group_id,
            semester_id=semester_id,
        )
        return self.lobby_domain.resolve_member_limits(
            team_semester.project_track,
            group_tracks=group_tracks,
        )

    @transaction.atomic
    def update_name(
        self,
        user: User,
        *,
        group_id: int,
        team_semester_id: int,
        name: str,
        semester_id_raw: str | None,
    ) -> dict[str, Any]:
        """Обновляет название команды."""
        _, team_semester = self._authorize_and_load(
            user,
            group_id=group_id,
            team_semester_id=team_semester_id,
            semester_id_raw=semester_id_raw,
        )
        cleaned_name = name.strip()
        if not cleaned_name:
            raise ValueError("Название команды не может быть пустым")
        self.repository.update_team_name(team_semester.team_id, cleaned_name)
        team_semester.team.name = cleaned_name
        self.repository.add_event_log(
            team_id=team_semester.team_id,
            team_semester_id=team_semester.id,
            user_id=user.id,
            text=f"Наставник изменил название команды на «{cleaned_name}»",
        )
        return self._to_detail(team_semester)

    @transaction.atomic
    def set_captain(
        self,
        user: User,
        *,
        group_id: int,
        team_semester_id: int,
        captain_id: int,
        semester_id_raw: str | None,
    ) -> dict[str, Any]:
        """Назначает нового капитана из состава команды."""
        _, team_semester = self._authorize_and_load(
            user,
            group_id=group_id,
            team_semester_id=team_semester_id,
            semester_id_raw=semester_id_raw,
        )
        self.domain.ensure_captain_is_member(team_semester, captain_id)
        team_semester = self.repository.transfer_captain(team_semester, captain_id)
        captain = next(
            member.user
            for member in team_semester.members.all()
            if member.user_id == captain_id
        )
        self.repository.add_event_log(
            team_id=team_semester.team_id,
            team_semester_id=team_semester.id,
            user_id=user.id,
            text=(
                "Наставник назначил капитаном "
                f"{self.lobby_domain.user_display_name(captain)}"
            ),
        )
        return self._to_detail(team_semester)

    @transaction.atomic
    def confirm_composition(
        self,
        user: User,
        *,
        group_id: int,
        team_semester_id: int,
        semester_id_raw: str | None,
    ) -> dict[str, Any]:
        """Подтверждает состав команды (forming → assembled)."""
        semester_id, team_semester = self._authorize_and_load(
            user,
            group_id=group_id,
            team_semester_id=team_semester_id,
            semester_id_raw=semester_id_raw,
        )
        members_count = self.repository.count_members(team_semester.id)
        min_members, max_members = self._member_limits(
            team_semester, group_id, semester_id
        )
        self.domain.ensure_can_confirm(
            status=team_semester.status,
            members_count=members_count,
            min_team_members=min_members,
            max_team_members=max_members,
        )
        team_semester = self.repository.set_status(
            team_semester, TeamSemester.Status.ASSEMBLED
        )
        self.repository.add_event_log(
            team_id=team_semester.team_id,
            team_semester_id=team_semester.id,
            user_id=user.id,
            text="Наставник подтвердил состав команды",
        )
        team_semester = self.repository.reload_team_semester(team_semester.id)
        return self._to_detail(team_semester)

    @transaction.atomic
    def unconfirm_composition(
        self,
        user: User,
        *,
        group_id: int,
        team_semester_id: int,
        semester_id_raw: str | None,
    ) -> dict[str, Any]:
        """Возвращает состав на редактирование (assembled → forming)."""
        _, team_semester = self._authorize_and_load(
            user,
            group_id=group_id,
            team_semester_id=team_semester_id,
            semester_id_raw=semester_id_raw,
        )
        self.domain.ensure_can_unconfirm(team_semester.status)
        team_semester = self.repository.set_status(
            team_semester, TeamSemester.Status.FORMING
        )
        self.repository.add_event_log(
            team_id=team_semester.team_id,
            team_semester_id=team_semester.id,
            user_id=user.id,
            text="Наставник вернул состав команды на редактирование",
        )
        team_semester = self.repository.reload_team_semester(team_semester.id)
        return self._to_detail(team_semester)

    @transaction.atomic
    def add_member(
        self,
        user: User,
        *,
        group_id: int,
        team_semester_id: int,
        semester_id_raw: str | None,
        user_id: int | None = None,
        pre_registered_student_id: int | None = None,
    ) -> dict[str, Any]:
        """Добавляет зарегистрированного или незарегистрированного студента."""
        semester_id, team_semester = self._authorize_and_load(
            user,
            group_id=group_id,
            team_semester_id=team_semester_id,
            semester_id_raw=semester_id_raw,
        )
        if (user_id is None) == (pre_registered_student_id is None):
            raise ValueError("Укажите userId или preRegisteredStudentId")

        target_user = self._resolve_member_user(
            group_id=group_id,
            user_id=user_id,
            pre_registered_student_id=pre_registered_student_id,
        )
        self.domain.ensure_student_role(
            target_user.role.code if target_user.role else None
        )
        self.domain.ensure_same_study_group(target_user.study_group_id, group_id)

        if self.repository.user_has_team_in_semester(
            user_id=target_user.id,
            semester_id=semester_id,
        ):
            raise ValueError("Студент уже состоит в команде")

        members_count = self.repository.count_members(team_semester.id)
        _, max_members = self._member_limits(team_semester, group_id, semester_id)
        if members_count >= max_members:
            raise ValueError(f"В команде не может быть больше {max_members} участников")

        role = self.domain.resolve_add_role(members_count)
        self.repository.add_member(
            team_semester_id=team_semester.id,
            user_id=target_user.id,
            role=role,
        )
        if role == TeamSemesterMember.Role.LEADER:
            self.repository.set_captain_for_first_member(team_semester, target_user.id)

        self.repository.mark_user_requests_obsolete(
            user_id=target_user.id,
            semester_id=semester_id,
        )
        self.repository.add_event_log(
            team_id=team_semester.team_id,
            team_semester_id=team_semester.id,
            user_id=user.id,
            text=(
                "Наставник добавил в команду "
                f"{self.lobby_domain.user_display_name(target_user)}"
            ),
        )
        team_semester = self.repository.reload_team_semester(team_semester.id)
        return self._to_detail(team_semester)

    def _resolve_member_user(
        self,
        *,
        group_id: int,
        user_id: int | None,
        pre_registered_student_id: int | None,
    ) -> User:
        """Возвращает пользователя для добавления в команду."""
        if user_id is not None:
            target_user = self.repository.get_user(user_id)
            if target_user is None:
                raise ValueError("Пользователь не найден")
            return target_user

        pre_registered = self.pre_registered_repository.get_by_id(
            pre_registered_student_id
        )
        if pre_registered is None:
            raise ValueError("Предрегистрация не найдена")
        if pre_registered.group_id != group_id:
            raise ValueError("Студент должен быть из этой учебной группы")
        if pre_registered.student_id is not None:
            return pre_registered.student
        return self.placeholder_service.get_or_create_placeholder(pre_registered)

    @transaction.atomic
    def remove_member(
        self,
        user: User,
        *,
        group_id: int,
        team_semester_id: int,
        member_user_id: int,
        semester_id_raw: str | None,
    ) -> dict[str, Any]:
        """Удаляет участника из команды."""
        _, team_semester = self._authorize_and_load(
            user,
            group_id=group_id,
            team_semester_id=team_semester_id,
            semester_id_raw=semester_id_raw,
        )
        self.domain.ensure_not_captain_removal(team_semester, member_user_id)

        member = next(
            (
                item
                for item in team_semester.members.all()
                if item.user_id == member_user_id
            ),
            None,
        )
        if member is None:
            raise ValueError("Участник не найден в команде")

        display = self.lobby_domain.user_display_name(member.user)
        removed = self.repository.remove_member_force(
            team_semester_id=team_semester.id,
            user_id=member_user_id,
        )
        if not removed:
            raise ValueError("Участник не найден в команде")

        self.repository.add_event_log(
            team_id=team_semester.team_id,
            team_semester_id=team_semester.id,
            user_id=user.id,
            text=f"Наставник исключил из команды {display}",
        )
        team_semester = self.repository.reload_team_semester(team_semester.id)
        return self._to_detail(team_semester)

    @transaction.atomic
    def delete_team(
        self,
        user: User,
        *,
        group_id: int,
        team_semester_id: int,
        semester_id_raw: str | None,
    ) -> dict[str, Any]:
        """Удаляет пустую команду."""
        _, team_semester = self._authorize_and_load(
            user,
            group_id=group_id,
            team_semester_id=team_semester_id,
            semester_id_raw=semester_id_raw,
        )
        members_count = self.repository.count_members(team_semester.id)
        self.domain.ensure_can_delete_team(members_count)

        team_id = team_semester.team_id
        team_semester_id_value = team_semester.id
        team_name = team_semester.team.name
        self.repository.add_event_log(
            team_id=team_id,
            team_semester_id=team_semester_id_value,
            user_id=user.id,
            text=f"Наставник удалил команду «{team_name}»",
        )
        self.repository.delete_team_semester(team_semester)
        return {
            "id": team_semester_id_value,
            "name": team_name,
            "status": team_semester.status,
            "membersCount": 0,
            "members": [],
        }

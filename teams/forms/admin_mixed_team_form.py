"""Форма admin для сборки смешанной команды из любых групп."""

from __future__ import annotations

from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model

from accounts.models import Semester
from showcase.models import ProjectApplication, ProjectTrack
from teams.domain.admin_mixed_team import AdminMixedTeamDomain
from teams.models import (
    AdminMixedTeamCreate,
    StudyGroup,
    TeamSemester,
    TeamSemesterMember,
)

User = get_user_model()


def _student_queryset():
    """Активные зарегистрированные студенты с группой для подписей."""
    return (
        User.objects.filter(
            role__code="student",
            is_active=True,
            is_placeholder=False,
        )
        .select_related("study_group", "role")
        .order_by("last_name", "first_name", "email")
    )


def _mentor_queryset():
    """Пользователи с ролью наставника."""
    return (
        User.objects.filter(role__code="mentor", is_active=True)
        .select_related("role")
        .order_by("last_name", "first_name", "email")
    )


def _user_label(user: User) -> str:
    """Подпись пользователя: ФИО, группа, email."""
    full_name = user.get_full_name() or "Без ФИО"
    group_name = user.study_group.name if user.study_group_id else "без группы"
    return f"{full_name} · {group_name} · {user.email}"


class AdminMixedTeamCreateForm(forms.ModelForm):
    """Единая форма: название, семестр, трек, капитан, участники из любых групп."""

    semester = forms.ModelChoiceField(
        queryset=Semester.objects.all().order_by("-position", "code"),
        label="Семестр",
        help_text="Семестр, в котором создаётся команда.",
    )
    home_study_group = forms.ModelChoiceField(
        queryset=StudyGroup.objects.filter(is_end=False)
        .select_related("institute")
        .order_by("institute__code", "name"),
        required=False,
        label="Домашняя учебная группа",
        help_text="Если пусто — берётся группа капитана.",
    )
    project_track = forms.ModelChoiceField(
        queryset=ProjectTrack.objects.select_related("semester").order_by(
            "-semester__position", "name"
        ),
        required=False,
        label="Проектный трек",
        help_text="Можно указать трек даже если не все группы к нему привязаны.",
    )
    project_application = forms.ModelChoiceField(
        queryset=ProjectApplication.objects.select_related("semester").order_by("-id"),
        required=False,
        label="Проектная заявка",
        help_text="Опционально: сразу записать команду на проект.",
    )
    captain = forms.ModelChoiceField(
        queryset=_student_queryset(),
        label="Капитан",
        help_text="Студент-капитан; будет добавлен в состав с ролью leader.",
    )
    members = forms.ModelMultipleChoiceField(
        queryset=_student_queryset(),
        required=False,
        label="Участники",
        help_text=(
            "Студенты из любых институтов и групп. Капитана можно не дублировать — "
            "он добавится автоматически."
        ),
        widget=FilteredSelectMultiple("студенты", is_stacked=False),
    )
    mentor = forms.ModelChoiceField(
        queryset=_mentor_queryset(),
        required=False,
        label="Наставник команды",
        help_text="Один наставник на TeamSemester (роль mentor).",
    )
    status = forms.ChoiceField(
        choices=TeamSemester.Status.choices,
        initial=TeamSemester.Status.ASSEMBLED,
        label="Статус состава",
        help_text="assembled — состав сразу подтверждён; forming — ещё редактируемый.",
    )

    class Meta:
        model = AdminMixedTeamCreate
        fields = ("name",)
        labels = {"name": "Название команды"}
        help_texts = {
            "name": (
                "Сборка без проверки, что группы участников входят в один трек. "
                "Используйте для смешанных институтов."
            ),
        }

    class Media:
        css = {"all": ("admin/css/widgets.css",)}
        js = (
            "admin/js/core.js",
            "admin/js/vendor/jquery/jquery.min.js",
            "admin/js/jquery.init.js",
            "admin/js/SelectBox.js",
            "admin/js/SelectFilter2.js",
        )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["captain"].label_from_instance = _user_label
        self.fields["members"].label_from_instance = _user_label
        self.fields["mentor"].label_from_instance = _user_label
        self.fields["name"].widget.attrs.setdefault("size", 60)
        self.domain = AdminMixedTeamDomain()

    def clean(self):
        cleaned = super().clean()
        captain = cleaned.get("captain")
        members = list(cleaned.get("members") or [])
        semester = cleaned.get("semester")
        project_track = cleaned.get("project_track")
        project_application = cleaned.get("project_application")
        mentor = cleaned.get("mentor")
        status = cleaned.get("status")
        home_study_group = cleaned.get("home_study_group")
        name = cleaned.get("name")

        if captain is not None and all(m.id != captain.id for m in members):
            members.append(captain)
        cleaned["members"] = members

        if not all([captain, semester, status, name]):
            return cleaned

        try:
            self.domain.normalize_name(name)
            member_ids = self.domain.merge_captain_into_members(
                captain_id=captain.id,
                member_ids=[user.id for user in members],
            )
            users_by_id = {user.id: user for user in members}
            users_by_id[captain.id] = captain
            ordered_users = [users_by_id[user_id] for user_id in member_ids]

            self.domain.ensure_student_users(ordered_users)
            self.domain.ensure_registered_users(ordered_users)
            self.domain.resolve_home_study_group(
                home_study_group=home_study_group,
                captain=captain,
            )
            min_members, max_members = self.domain.resolve_member_limits(project_track)
            self.domain.ensure_status_member_count(
                status=status,
                members_count=len(ordered_users),
                min_team_members=min_members,
                max_team_members=max_members,
            )

            if (
                project_application is not None
                and project_application.semester_id is not None
                and project_application.semester_id != semester.id
            ):
                raise ValueError("Проектная заявка относится к другому семестру")
            if project_track is not None and project_track.semester_id != semester.id:
                raise ValueError("Проектный трек относится к другому семестру")

            if mentor is not None:
                mentor_role = mentor.role.code if mentor.role else None
                if mentor_role != "mentor":
                    raise ValueError("Наставник должен иметь роль mentor")

            busy = set(
                TeamSemesterMember.objects.filter(
                    user_id__in=member_ids,
                    semester_id=semester.id,
                ).values_list("user_id", flat=True)
            )
            if busy:
                busy_names = ", ".join(
                    users_by_id[user_id].get_full_name() or users_by_id[user_id].email
                    for user_id in member_ids
                    if user_id in busy
                )
                raise ValueError(f"Уже состоят в команде в этом семестре: {busy_names}")
        except ValueError as exc:
            raise forms.ValidationError(str(exc)) from exc

        return cleaned

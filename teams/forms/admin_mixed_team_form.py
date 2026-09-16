"""Форма admin для сборки смешанной команды из любых групп."""

from __future__ import annotations

from django import forms
from django.contrib import admin as django_admin
from django.contrib.admin.widgets import AutocompleteSelect, AutocompleteSelectMultiple
from django.contrib.auth import get_user_model

from accounts.models import Semester
from showcase.models import ProjectApplication, ProjectTrack
from teams.domain.admin_mixed_team import AdminMixedTeamDomain
from teams.models import (
    AdminMixedTeamCreate,
    StudyGroup,
    Team,
    TeamSemester,
    TeamSemesterMember,
)

User = get_user_model()


def _user_label(user: User) -> str:
    """Подпись пользователя: ФИО, группа, email."""
    full_name = user.get_full_name() or "Без ФИО"
    group_name = user.study_group.name if user.study_group_id else "без группы"
    return f"{full_name} · {group_name} · {user.email}"


def _bind_autocomplete(
    field: forms.Field,
    *,
    db_field,
    admin_site: django_admin.AdminSite,
    multiple: bool = False,
) -> None:
    """Подключает AJAX-поиск Django admin (Select2) к полю формы."""
    widget_cls = AutocompleteSelectMultiple if multiple else AutocompleteSelect
    widget = widget_cls(db_field, admin_site)
    widget.is_required = field.required
    field.widget = widget


class AdminMixedTeamCreateForm(forms.ModelForm):
    """Единая форма: название, семестр, трек, капитан, участники из любых групп."""

    semester = forms.ModelChoiceField(
        queryset=Semester.objects.all(),
        label="Семестр",
        help_text="Начните вводить код или название семестра.",
    )
    home_study_group = forms.ModelChoiceField(
        queryset=StudyGroup.objects.filter(is_end=False),
        required=False,
        label="Домашняя учебная группа",
        help_text="Поиск по названию/коду. Если пусто — берётся группа капитана.",
    )
    project_track = forms.ModelChoiceField(
        queryset=ProjectTrack.objects.all(),
        required=False,
        label="Проектный трек",
        help_text="Поиск по названию трека. Привязка групп к треку не требуется.",
    )
    project_application = forms.ModelChoiceField(
        queryset=ProjectApplication.objects.all(),
        required=False,
        label="Проектная заявка",
        help_text="Поиск по названию заявки. Опционально.",
    )
    captain = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Капитан",
        help_text="Поиск по ФИО/email/группе. Должен быть зарегистрированным студентом.",
    )
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        label="Участники",
        help_text=(
            "Поиск и множественный выбор студентов из любых институтов. "
            "Капитан добавится автоматически, если не выбран."
        ),
    )
    mentor = forms.ModelChoiceField(
        queryset=User.objects.filter(role__code="mentor"),
        required=False,
        label="Наставник команды",
        help_text="Поиск наставника (роль mentor).",
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

    def __init__(self, *args, admin_site=None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        site = admin_site or django_admin.site
        self.domain = AdminMixedTeamDomain()

        _bind_autocomplete(
            self.fields["semester"],
            db_field=TeamSemester._meta.get_field("semester"),
            admin_site=site,
        )
        _bind_autocomplete(
            self.fields["home_study_group"],
            db_field=Team._meta.get_field("home_study_group"),
            admin_site=site,
        )
        _bind_autocomplete(
            self.fields["project_track"],
            db_field=TeamSemester._meta.get_field("project_track"),
            admin_site=site,
        )
        _bind_autocomplete(
            self.fields["project_application"],
            db_field=TeamSemester._meta.get_field("project_application"),
            admin_site=site,
        )
        _bind_autocomplete(
            self.fields["captain"],
            db_field=TeamSemester._meta.get_field("captain"),
            admin_site=site,
        )
        _bind_autocomplete(
            self.fields["members"],
            db_field=TeamSemesterMember._meta.get_field("user"),
            admin_site=site,
            multiple=True,
        )
        _bind_autocomplete(
            self.fields["mentor"],
            db_field=TeamSemester._meta.get_field("mentor"),
            admin_site=site,
        )

        self.fields["captain"].label_from_instance = _user_label
        self.fields["members"].label_from_instance = _user_label
        self.fields["mentor"].label_from_instance = _user_label
        self.fields["name"].widget.attrs.setdefault("size", 60)

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

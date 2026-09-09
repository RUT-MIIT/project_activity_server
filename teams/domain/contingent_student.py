"""Единое представление студента контингента группы."""

from __future__ import annotations

from dataclasses import dataclass

from accounts.models import PreRegisteredStudent, User
from teams.models import StudyGroup


@dataclass(frozen=True)
class ContingentStudent:
    """
    Студент контингента из предрегистрации или напрямую созданного User.

    Для предрегистрации ``id`` — PreRegisteredStudent.id.
    Для студента без предрегистрации ``id`` совпадает с ``user_id``.
    """

    id: int
    last_name: str
    first_name: str
    middle_name: str
    is_registered: bool
    user: User | None
    group: StudyGroup | None
    user_id: int | None

    @classmethod
    def from_pre_registered(
        cls, pre_registered: PreRegisteredStudent
    ) -> ContingentStudent:
        """Строит строку контингента из предрегистрации."""
        return cls(
            id=pre_registered.id,
            last_name=pre_registered.last_name,
            first_name=pre_registered.first_name,
            middle_name=pre_registered.middle_name or "",
            is_registered=pre_registered.is_registered,
            user=pre_registered.user,
            group=pre_registered.group,
            user_id=pre_registered.user_id,
        )

    @classmethod
    def from_user(cls, user: User) -> ContingentStudent:
        """Строит строку контингента из напрямую созданного пользователя."""
        return cls(
            id=user.id,
            last_name=user.last_name,
            first_name=user.first_name,
            middle_name=user.middle_name or "",
            is_registered=True,
            user=user,
            group=getattr(user, "study_group", None),
            user_id=user.id,
        )


def merge_contingent_students(
    pre_registered: list[PreRegisteredStudent],
    direct_users: list[User],
    *,
    sort_key=None,
) -> list[ContingentStudent]:
    """
    Объединяет предрегистрацию и прямых студентов без дублей.

    Пользователь, уже связанный с предрегистрацией в выборке, не дублируется.
    """
    linked_user_ids = {
        item.user_id for item in pre_registered if item.user_id is not None
    }
    rows = [ContingentStudent.from_pre_registered(item) for item in pre_registered]
    for user in direct_users:
        if user.id in linked_user_ids:
            continue
        rows.append(ContingentStudent.from_user(user))

    if sort_key is None:

        def default_sort_key(row: ContingentStudent) -> tuple:
            return (row.last_name, row.first_name, row.id)

        sort_key = default_sort_key
    rows.sort(key=sort_key)
    return rows

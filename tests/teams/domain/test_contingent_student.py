"""Тесты объединения контингента из предрегистрации и прямых User."""

from __future__ import annotations

from types import SimpleNamespace

from teams.domain.contingent_student import ContingentStudent, merge_contingent_students


def test_from_user_marks_registered_and_uses_user_id() -> None:
    user = SimpleNamespace(
        id=42,
        last_name="Прямой",
        first_name="Студент",
        middle_name="И",
        study_group=None,
    )
    row = ContingentStudent.from_user(user)
    assert row.id == 42
    assert row.user_id == 42
    assert row.is_registered is True
    assert row.last_name == "Прямой"


def test_merge_excludes_user_linked_in_preregistration() -> None:
    pre = SimpleNamespace(
        id=10,
        last_name="Аа",
        first_name="А",
        middle_name="",
        is_registered=True,
        user=None,
        user_id=5,
        group=None,
    )
    linked_user = SimpleNamespace(
        id=5,
        last_name="Аа",
        first_name="А",
        middle_name="",
        study_group=None,
    )
    other_user = SimpleNamespace(
        id=7,
        last_name="Бб",
        first_name="Б",
        middle_name="",
        study_group=None,
    )

    rows = merge_contingent_students([pre], [linked_user, other_user])
    assert [row.id for row in rows] == [10, 7]
    assert rows[1].user_id == 7

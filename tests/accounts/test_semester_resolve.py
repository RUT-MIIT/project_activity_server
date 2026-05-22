"""Тесты разбора semester_id для GET-списков."""

import pytest

from accounts.models import (
    ACTIVE_SEMESTER_SETTING_CODE,
    NEXT_SEMESTER_SETTING_CODE,
    Semester,
    Settings,
)


@pytest.mark.django_db
class TestSemesterResolveListSemesterId:
    def test_numeric_id(self):
        semester = Semester.objects.create(code="s1", name="S1", position=1)
        assert Semester.resolve_list_semester_id(str(semester.pk)) == semester.pk

    def test_next_from_settings(self):
        semester = Semester.objects.create(code="next-sem", name="Next", position=1)
        Settings.objects.update_or_create(
            code=NEXT_SEMESTER_SETTING_CODE,
            defaults={"value": semester.code, "description": ""},
        )
        assert Semester.resolve_list_semester_id("next") == semester.pk

    def test_actual_from_settings(self):
        semester = Semester.objects.create(code="actual-sem", name="Actual", position=1)
        Settings.objects.update_or_create(
            code=ACTIVE_SEMESTER_SETTING_CODE,
            defaults={"value": semester.code, "description": ""},
        )
        assert Semester.resolve_list_semester_id("actual") == semester.pk

    def test_unknown_id_raises(self):
        with pytest.raises(ValueError, match="не найден"):
            Semester.resolve_list_semester_id("99999")

    def test_invalid_token_raises(self):
        with pytest.raises(ValueError, match="next.*actual"):
            Semester.resolve_list_semester_id("invalid")

    def test_next_not_configured_raises(self):
        with pytest.raises(ValueError, match="next"):
            Semester.resolve_list_semester_id("next")

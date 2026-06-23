"""Тесты institute_access."""

import pytest

from showcase.models import ApplicationInvolvedDepartment, ProjectApplication
from teams.domain.institute_access import (
    application_available_for_institute,
    application_belongs_to_institutes,
)


@pytest.fixture
def semester(db):
    from accounts.models import Semester

    return Semester.objects.create(code="s1", name="S1", position=1)


def _create_approved_app(
    *,
    semester,
    statuses,
    title: str = "Проект",
) -> ProjectApplication:
    return ProjectApplication.objects.create(
        title=title,
        company="ООО",
        author_lastname="Иванов",
        author_firstname="Иван",
        author_email="a@b.c",
        semester=semester,
        status=statuses["approved"],
        goal="Длинная цель проекта больше пятидесяти символов для валидации",
        problem_holder="Носитель",
        barrier="Длинный барьер больше пятидесяти символов для валидации",
    )


@pytest.mark.django_db
class TestApplicationBelongsToInstitutes:
    def test_target_institutes_ignored_without_involved_department(
        self, statuses, institute, semester
    ):
        app = _create_approved_app(semester=semester, statuses=statuses)
        app.target_institutes.add(institute)

        assert application_belongs_to_institutes(app, [institute.code]) is False

    def test_by_involved_department(self, statuses, institute, semester, departments):
        app = _create_approved_app(semester=semester, statuses=statuses)
        ApplicationInvolvedDepartment.objects.create(
            application=app,
            department=departments["child"],
        )

        assert application_belongs_to_institutes(app, [institute.code]) is True

    def test_denied_for_other_institute_involved_department(
        self, statuses, institute, semester, departments
    ):
        from accounts.models import Department
        from showcase.models import Institute

        other_parent = Department.objects.create(name="Other Root", short_name="OR")
        other_institute = Institute.objects.create(
            code="OTHER",
            name="Other",
            position=2,
            department=other_parent,
        )
        other_child = Department.objects.create(
            name="Other Child",
            short_name="OC",
            parent=other_parent,
        )
        app = _create_approved_app(semester=semester, statuses=statuses)
        ApplicationInvolvedDepartment.objects.create(
            application=app,
            department=other_child,
        )

        assert application_belongs_to_institutes(app, [institute.code]) is False
        assert application_belongs_to_institutes(app, [other_institute.code]) is True

    def test_empty_targets_and_no_involved_denied(self, statuses, institute, semester):
        app = _create_approved_app(semester=semester, statuses=statuses)

        assert application_belongs_to_institutes(app, [institute.code]) is False


@pytest.mark.django_db
class TestApplicationAvailableForInstitute:
    def test_by_target_institutes_only(self, statuses, institute, semester):
        app = _create_approved_app(semester=semester, statuses=statuses)
        app.target_institutes.add(institute)

        assert application_available_for_institute(app, [institute.code]) is True
        assert application_belongs_to_institutes(app, [institute.code]) is False

    def test_by_involved_department(self, statuses, institute, semester, departments):
        app = _create_approved_app(semester=semester, statuses=statuses)
        ApplicationInvolvedDepartment.objects.create(
            application=app,
            department=departments["child"],
        )

        assert application_available_for_institute(app, [institute.code]) is True

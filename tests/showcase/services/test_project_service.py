"""Тесты ProjectService."""

import pytest

from accounts.models import Department, Semester
from showcase.models import ApplicationInvolvedDepartment, Institute, ProjectApplication
from showcase.services.project_service import ProjectService


@pytest.fixture
def other_institute(departments):
    other_dept = Department.objects.create(name="Other Parent", short_name="OP")
    return Institute.objects.create(
        code="OTHER",
        name="Other Institute",
        position=2,
        department=other_dept,
    )


@pytest.mark.django_db
class TestProjectService:
    def test_list_projects_filters_by_institute_and_status(
        self, roles, make_user, statuses, institute, other_institute, departments
    ):
        semester = Semester.objects.create(code="s1", name="S1", position=1)
        user = make_user(role_code="institute_validator", with_department=True)
        service = ProjectService()

        own = ProjectApplication.objects.create(
            title="Свой",
            company="ООО",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="a@example.com",
            semester=semester,
            status=statuses["approved"],
            goal="Длинная цель проекта больше пятидесяти символов для валидации",
            problem_holder="Носитель",
            barrier="Длинный барьер больше пятидесяти символов для валидации",
        )
        own.target_institutes.add(institute)

        foreign = ProjectApplication.objects.create(
            title="Чужой",
            company="ООО",
            author_lastname="Петров",
            author_firstname="Пётр",
            author_email="b@example.com",
            semester=semester,
            status=statuses["approved"],
            goal="Длинная цель проекта больше пятидесяти символов для валидации",
            problem_holder="Носитель",
            barrier="Длинный барьер больше пятидесяти символов для валидации",
        )
        foreign.target_institutes.add(other_institute)

        ids = set(
            service.list_projects(user, str(semester.id)).values_list("id", flat=True)
        )
        assert ids == {own.id}

    def test_list_projects_includes_non_approved_for_validator(
        self, make_user, statuses, institute
    ):
        semester = Semester.objects.create(code="s1", name="S1", position=1)
        user = make_user(role_code="institute_validator", with_department=True)
        service = ProjectService()

        pending = ProjectApplication.objects.create(
            title="В работе",
            company="ООО",
            author_lastname="Петров",
            author_firstname="Пётр",
            author_email="petr@example.com",
            semester=semester,
            status=statuses["await_cpds"],
            goal="Длинная цель проекта больше пятидесяти символов для валидации",
            problem_holder="Носитель",
            barrier="Длинный барьер больше пятидесяти символов для валидации",
        )
        pending.target_institutes.add(institute)

        ids = set(
            service.list_projects(user, str(semester.id)).values_list("id", flat=True)
        )
        assert ids == {pending.id}

    def test_list_projects_admin_sees_all_statuses(
        self, make_user, statuses, institute, other_institute
    ):
        semester = Semester.objects.create(code="s1", name="S1", position=1)
        admin = make_user(role_code="admin")
        service = ProjectService()

        approved = ProjectApplication.objects.create(
            title="Одобрен",
            company="ООО",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="a@example.com",
            semester=semester,
            status=statuses["approved"],
            goal="Длинная цель проекта больше пятидесяти символов для валидации",
            problem_holder="Носитель",
            barrier="Длинный барьер больше пятидесяти символов для валидации",
        )
        approved.target_institutes.add(institute)

        pending = ProjectApplication.objects.create(
            title="Чужой институт",
            company="ООО",
            author_lastname="Петров",
            author_firstname="Пётр",
            author_email="b@example.com",
            semester=semester,
            status=statuses["await_cpds"],
            goal="Длинная цель проекта больше пятидесяти символов для валидации",
            problem_holder="Носитель",
            barrier="Длинный барьер больше пятидесяти символов для валидации",
        )
        pending.target_institutes.add(other_institute)

        ids = set(
            service.list_projects(admin, str(semester.id)).values_list("id", flat=True)
        )
        assert ids == {approved.id, pending.id}

    def test_list_projects_admin_without_semester_returns_all(
        self, make_user, statuses, institute
    ):
        semester1 = Semester.objects.create(code="s1", name="S1", position=1)
        semester2 = Semester.objects.create(code="s2", name="S2", position=2)
        admin = make_user(role_code="admin")
        service = ProjectService()

        app1 = ProjectApplication.objects.create(
            title="S1",
            company="ООО",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="a@example.com",
            semester=semester1,
            status=statuses["approved"],
            goal="Длинная цель проекта больше пятидесяти символов для валидации",
            problem_holder="Носитель",
            barrier="Длинный барьер больше пятидесяти символов для валидации",
        )
        app2 = ProjectApplication.objects.create(
            title="S2",
            company="ООО",
            author_lastname="Петров",
            author_firstname="Пётр",
            author_email="b@example.com",
            semester=semester2,
            status=statuses["created"],
            goal="Длинная цель проекта больше пятидесяти символов для валидации",
            problem_holder="Носитель",
            barrier="Длинный барьер больше пятидесяти символов для валидации",
        )

        ids = set(service.list_projects(admin, None).values_list("id", flat=True))
        assert ids == {app1.id, app2.id}

    def test_list_projects_raises_for_regular_user(self, make_user, statuses):
        semester = Semester.objects.create(code="s1", name="S1", position=1)
        user = make_user(role_code="user")
        service = ProjectService()

        with pytest.raises(PermissionError, match="прав"):
            service.list_projects(user, str(semester.id))

    def test_list_projects_empty_without_institutes(self, make_user, statuses):
        semester = Semester.objects.create(code="s1", name="S1", position=1)
        user = make_user(role_code="institute_validator", with_department=False)
        service = ProjectService()

        assert service.list_projects(user, str(semester.id)).count() == 0

    def test_list_projects_by_involved_department(
        self, make_user, statuses, institute, departments
    ):
        semester = Semester.objects.create(code="s1", name="S1", position=1)
        user = make_user(role_code="institute_validator", with_department=True)
        service = ProjectService()

        app = ProjectApplication.objects.create(
            title="По кафедре",
            company="ООО",
            author_lastname="Иванов",
            author_firstname="Иван",
            author_email="a@example.com",
            semester=semester,
            status=statuses["approved"],
            goal="Длинная цель проекта больше пятидесяти символов для валидации",
            problem_holder="Носитель",
            barrier="Длинный барьер больше пятидесяти символов для валидации",
        )
        ApplicationInvolvedDepartment.objects.create(
            application=app,
            department=departments["child"],
        )

        ids = set(
            service.list_projects(user, str(semester.id)).values_list("id", flat=True)
        )
        assert ids == {app.id}

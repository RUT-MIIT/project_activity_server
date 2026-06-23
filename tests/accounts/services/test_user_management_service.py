"""Тесты UserManagementService."""

import pytest

from accounts.models import Department
from accounts.services.user_management_service import UserManagementService
from showcase.models import ProjectApplication


@pytest.mark.django_db
class TestUserManagementService:
    def test_list_users_admin_sees_non_admin_users(self, make_user, roles):
        admin = make_user(role_code="admin")
        regular = make_user(role_code="user", email="regular@example.com")
        service = UserManagementService()

        ids = set(service.list_users(admin).values_list("id", flat=True))
        assert regular.id in ids
        assert admin.id not in ids

    def test_list_users_validator_filters_by_institute_subtree(
        self, make_user, departments, institute
    ):
        validator = make_user(
            role_code="institute_validator",
            with_department=True,
            email="validator@example.com",
        )
        own_dept_user = make_user(
            role_code="user",
            with_department=True,
            email="own@example.com",
        )

        other_parent = Department.objects.create(name="Other Root", short_name="OR")
        other_child = Department.objects.create(
            name="Other Child", short_name="OC", parent=other_parent
        )
        foreign_user = make_user(
            role_code="user",
            email="foreign@example.com",
        )
        foreign_user.department = other_child
        foreign_user.save(update_fields=["department"])

        service = UserManagementService()
        ids = set(service.list_users(validator).values_list("id", flat=True))

        assert own_dept_user.id in ids
        assert validator.id in ids
        assert foreign_user.id not in ids

    def test_list_users_annotates_authored_projects_count(self, make_user, statuses):
        from accounts.models import Semester

        admin = make_user(role_code="admin")
        author = make_user(role_code="user", email="author@example.com")
        semester = Semester.objects.create(code="s1", name="S1", position=1)

        ProjectApplication.objects.create(
            title="Проект 1",
            company="ООО",
            author=author,
            author_lastname=author.last_name,
            author_firstname=author.first_name,
            author_email=author.email,
            semester=semester,
            status=statuses["created"],
            goal="Длинная цель проекта больше пятидесяти символов для валидации",
            problem_holder="Носитель",
            barrier="Длинный барьер больше пятидесяти символов для валидации",
        )
        ProjectApplication.objects.create(
            title="Проект 2",
            company="ООО",
            author=author,
            author_lastname=author.last_name,
            author_firstname=author.first_name,
            author_email=author.email,
            semester=semester,
            status=statuses["approved"],
            goal="Длинная цель проекта больше пятидесяти символов для валидации",
            problem_holder="Носитель",
            barrier="Длинный барьер больше пятидесяти символов для валидации",
        )

        service = UserManagementService()
        user = service.list_users(admin).get(pk=author.id)
        assert user.authored_projects_count == 2

    def test_update_user_changes_role(self, make_user, roles, departments):
        admin = make_user(role_code="admin")
        target = make_user(role_code="user", email="target@example.com")
        service = UserManagementService()

        updated = service.update_user(
            admin,
            target.id,
            role_code="department_validator",
            department_id=departments["child"].id,
            fields_set={"role", "department_id"},
        )
        updated.refresh_from_db()
        assert updated.role.code == "department_validator"
        assert updated.department_id == departments["child"].id

    def test_update_user_validator_raises_permission_error(self, make_user):
        validator = make_user(role_code="institute_validator", with_department=True)
        target = make_user(role_code="user", email="target2@example.com")
        service = UserManagementService()

        with pytest.raises(PermissionError):
            service.update_user(
                validator,
                target.id,
                role_code="mentor",
                department_id=None,
                fields_set={"role"},
            )

"""Тесты UserManagementDomain."""

import pytest

from accounts.domain.user_management import UserManagementDomain
from accounts.models import Role


@pytest.mark.django_db
class TestUserManagementDomain:
    def test_can_list_users_admin(self, make_user):
        user = make_user(role_code="admin")
        ok, _ = UserManagementDomain.can_list_users(user)
        assert ok is True

    def test_can_list_users_validator(self, make_user):
        user = make_user(role_code="institute_validator", with_department=True)
        ok, _ = UserManagementDomain.can_list_users(user)
        assert ok is True

    def test_can_list_users_denied_for_regular_user(self, make_user):
        user = make_user(role_code="user")
        ok, error = UserManagementDomain.can_list_users(user)
        assert ok is False
        assert error

    def test_can_update_users_validator_denied(self, make_user):
        user = make_user(role_code="institute_validator", with_department=True)
        ok, error = UserManagementDomain.can_update_users(user)
        assert ok is False
        assert error

    def test_validate_update_rejects_admin_role_assignment(self, make_user, roles):
        target = make_user(role_code="user")
        admin_role = roles["admin"]
        ok, error = UserManagementDomain.validate_update(
            target, admin_role, None, {"role"}
        )
        assert ok is False
        assert "администратора" in error

    def test_validate_update_requires_department_for_role(self, make_user, roles):
        target = make_user(role_code="user", with_department=False)
        role = Role.objects.create(
            code="needs_dept",
            name="Needs Dept",
            requires_department=True,
        )
        ok, error = UserManagementDomain.validate_update(target, role, None, {"role"})
        assert ok is False
        assert "подразделение" in error

    def test_is_protected_user_staff(self, make_user, user_model):
        user = make_user(role_code="user")
        user.is_staff = True
        user.save(update_fields=["is_staff"])
        assert UserManagementDomain.is_protected_user(user) is True

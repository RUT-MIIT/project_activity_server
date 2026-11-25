"""Ограниченное управление пользователями ответственным института."""

import pytest
from rest_framework.test import APIClient

from accounts.models import Department
from showcase.models import Institute


@pytest.fixture
def scope(make_user, departments, institute):
    actor = make_user(role_code="institute_validator", with_department=True)
    target = make_user(role_code="mentor", with_department=True)
    client = APIClient()
    client.force_authenticate(user=actor)
    return actor, target, client


def patch_user(client, target, data):
    return client.patch(f"/api/accounts/users/{target.pk}/", data, format="json")


@pytest.mark.django_db
def test_assign_move_and_remove_department_role(scope, departments, roles):
    _, target, client = scope
    nested = Department.objects.create(
        name="Nested", short_name="N", parent=departments["child"]
    )
    roles["department_validator"].requires_department = True
    roles["department_validator"].save()
    response = patch_user(
        client, target, {"role": "department_validator", "department_id": nested.pk}
    )
    assert response.status_code == 200
    target.refresh_from_db()
    assert target.role_id == "department_validator"
    assert target.department_id == nested.pk
    response = patch_user(client, target, {"role": "user"})
    assert response.status_code == 200
    target.refresh_from_db()
    assert target.role_id == "user"


@pytest.mark.django_db
def test_shared_root_does_not_grant_cross_institute_write(
    scope, departments, make_user
):
    _, target, client = scope
    common = Department.objects.create(name="University", short_name="U")
    departments["parent"].parent = common
    departments["parent"].save()
    foreign = Department.objects.create(name="Other", short_name="O", parent=common)
    Institute.objects.create(code="OTHER", name="Other", position=2, department=foreign)
    foreign_user = make_user()
    foreign_user.department = foreign
    foreign_user.save()
    assert patch_user(client, foreign_user, {"role": "mentor"}).status_code == 403
    assert patch_user(client, target, {"department_id": foreign.pk}).status_code == 403
    assert patch_user(client, target, {"department_id": common.pk}).status_code == 403
    target.refresh_from_db()
    assert target.department_id == departments["child"].pk


@pytest.mark.django_db
def test_no_department_and_inactive_institute(scope, make_user, institute):
    _, target, client = scope
    assert patch_user(client, make_user(), {"role": "mentor"}).status_code == 403
    assert patch_user(client, target, {"department_id": None}).status_code == 403
    institute.is_active = False
    institute.save()
    assert patch_user(client, target, {"role": "user"}).status_code == 403


@pytest.mark.django_db
def test_role_requiring_department_uses_resulting_department(
    make_user, roles, departments
):
    actor = make_user(role_code="admin")
    target = make_user()
    roles["department_validator"].requires_department = True
    roles["department_validator"].save()
    client = APIClient()
    client.force_authenticate(user=actor)
    assert (
        patch_user(client, target, {"role": "department_validator"}).status_code == 400
    )
    assert (
        patch_user(
            client,
            target,
            {"role": "department_validator", "department_id": departments["child"].pk},
        ).status_code
        == 200
    )
    assert patch_user(client, target, {"department_id": None}).status_code == 400
    target.refresh_from_db()
    assert target.department_id == departments["child"].pk


@pytest.mark.django_db
@pytest.mark.parametrize("role", ["admin", "cpds", "institute_validator"])
def test_protected_role_and_target(scope, make_user, role):
    _, target, client = scope
    assert patch_user(client, target, {"role": role}).status_code == 403
    protected = make_user(role_code=role, with_department=True)
    assert patch_user(client, protected, {"role": "user"}).status_code == 403
    target.refresh_from_db()
    assert target.role_id == "mentor"


@pytest.mark.django_db
def test_staff_and_contact_fields_are_protected(scope, make_user):
    _, target, client = scope
    staff = make_user(with_department=True)
    staff.is_staff = True
    staff.save()
    assert patch_user(client, staff, {"role": "mentor"}).status_code == 403
    for field, value in [("email", "changed@example.com"), ("phone", "123")]:
        assert (
            patch_user(client, target, {"role": "user", field: value}).status_code
            == 403
        )
        target.refresh_from_db()
        assert target.role_id == "mentor"


@pytest.mark.django_db
@pytest.mark.parametrize("role", ["admin", "cpds", "user"])
def test_existing_roles_and_staff_contact_permissions(make_user, role):
    actor = make_user(role_code=role)
    if role == "user":
        actor.is_staff = True
        actor.save()
    target = make_user()
    client = APIClient()
    client.force_authenticate(user=actor)
    response = patch_user(
        client, target, {"email": "updated@example.com", "phone": "123"}
    )
    assert response.status_code == 200
    target.refresh_from_db()
    assert target.email == "updated@example.com"
    assert target.phone == "123"


@pytest.mark.django_db
def test_regular_user_still_cannot_patch(make_user):
    client = APIClient()
    client.force_authenticate(user=make_user())
    assert patch_user(client, make_user(), {"role": "mentor"}).status_code == 403

"""Unit-тесты для утилит работы с подразделениями."""

import pytest

from accounts.models import Department
from accounts.utils import get_root_department, is_cpds_department


@pytest.mark.django_db
class TestGetRootDepartment:
    """Тесты для функции get_root_department."""

    def test_department_without_parent_returns_itself(self):
        """Подразделение без parent возвращает само себя."""
        dept = Department.objects.create(name="Root Dept", short_name="RD")
        root = get_root_department(dept)

        assert root == dept
        assert root.parent is None

    def test_department_with_one_level_parent(self, departments):
        """Подразделение с одним уровнем parent возвращает корневое."""
        child = departments["child"]
        root = get_root_department(child)

        assert root == departments["parent"]
        assert root.parent is None

    def test_department_with_multiple_levels_parent(self):
        """Подразделение с несколькими уровнями parent возвращает корневое."""
        root_dept = Department.objects.create(name="Root", short_name="R")
        middle_dept = Department.objects.create(
            name="Middle", short_name="M", parent=root_dept
        )
        child_dept = Department.objects.create(
            name="Child", short_name="C", parent=middle_dept
        )

        root = get_root_department(child_dept)

        assert root == root_dept
        assert root.parent is None

    def test_none_returns_none(self):
        """None на входе возвращает None."""
        root = get_root_department(None)

        assert root is None


@pytest.mark.django_db
class TestIsCpdsDepartment:
    """Тесты для функции is_cpds_department."""

    def test_cpds_department_detected_by_short_name(self):
        dept = Department.objects.create(
            name="Центр проектного развития", short_name="ЦПДС"
        )
        assert is_cpds_department(dept) is True

    def test_regular_department_is_not_cpds(self, departments):
        assert is_cpds_department(departments["parent"]) is False

    def test_none_is_not_cpds(self):
        assert is_cpds_department(None) is False

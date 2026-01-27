"""Unit-тесты для утилит работы с подразделениями."""

import pytest

from accounts.models import Department
from accounts.utils import get_root_department


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

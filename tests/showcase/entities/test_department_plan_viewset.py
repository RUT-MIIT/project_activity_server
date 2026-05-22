"""Unit-тесты для DepartmentPlanViewSet API эндпоинта.

Проверяем все крайние ситуации для POST и GET эндпоинтов.
"""

import pytest
from rest_framework.test import APIClient

from accounts.models import Department, Semester
from showcase.models import (
    ApplicationInvolvedDepartment,
    ApplicationStatus,
    DepartmentPlan,
    Institute,
    ProjectApplication,
)


@pytest.mark.django_db
class TestDepartmentPlanViewSetCreate:
    """Тесты для POST /api/showcase/department-plans/ - установка плана."""

    def test_create_plan_success(self, make_user, departments):
        """Успешное создание плана для подразделения на семестр."""
        client = APIClient()
        user = make_user(role_code="admin")
        client.force_authenticate(user=user)

        semester = Semester.objects.create(
            code="2024-fall", name="Осенний семестр 2024", position=1
        )
        department = departments["parent"]

        data = {
            "department_id": department.id,
            "semester_id": semester.id,
            "plan": 10,
        }

        response = client.post("/api/showcase/department-plans/", data, format="json")

        assert response.status_code == 201
        assert response.data["department_id"] == department.id
        assert response.data["semester_id"] == semester.id
        assert response.data["plan"] == 10
        assert "id" in response.data

        # Проверяем, что план создан в БД
        plan = DepartmentPlan.objects.get(department=department, semester=semester)
        assert plan.plan == 10

    def test_update_plan_success(self, make_user, departments):
        """Успешное обновление существующего плана."""
        client = APIClient()
        user = make_user(role_code="admin")
        client.force_authenticate(user=user)

        semester = Semester.objects.create(
            code="2024-fall", name="Осенний семестр 2024", position=1
        )
        department = departments["parent"]

        # Создаем план
        DepartmentPlan.objects.create(department=department, semester=semester, plan=5)

        # Обновляем план
        data = {
            "department_id": department.id,
            "semester_id": semester.id,
            "plan": 15,
        }

        response = client.post("/api/showcase/department-plans/", data, format="json")

        assert response.status_code == 200
        assert response.data["plan"] == 15

        # Проверяем, что план обновлен в БД
        plan = DepartmentPlan.objects.get(department=department, semester=semester)
        assert plan.plan == 15

    def test_create_plan_zero_value(self, make_user, departments):
        """Создание плана со значением 0 (минимальное допустимое)."""
        client = APIClient()
        user = make_user(role_code="admin")
        client.force_authenticate(user=user)

        semester = Semester.objects.create(
            code="2024-fall", name="Осенний семестр 2024", position=1
        )
        department = departments["parent"]

        data = {
            "department_id": department.id,
            "semester_id": semester.id,
            "plan": 0,
        }

        response = client.post("/api/showcase/department-plans/", data, format="json")

        assert response.status_code == 201
        assert response.data["plan"] == 0

    def test_create_plan_large_value(self, make_user, departments):
        """Создание плана с большим значением."""
        client = APIClient()
        user = make_user(role_code="admin")
        client.force_authenticate(user=user)

        semester = Semester.objects.create(
            code="2024-fall", name="Осенний семестр 2024", position=1
        )
        department = departments["parent"]

        data = {
            "department_id": department.id,
            "semester_id": semester.id,
            "plan": 999999,
        }

        response = client.post("/api/showcase/department-plans/", data, format="json")

        assert response.status_code == 201
        assert response.data["plan"] == 999999

    def test_create_plan_unauthorized(self, departments):
        """Ошибка: неавторизованный пользователь."""
        client = APIClient()
        semester = Semester.objects.create(
            code="2024-fall", name="Осенний семестр 2024", position=1
        )
        department = departments["parent"]

        data = {
            "department_id": department.id,
            "semester_id": semester.id,
            "plan": 10,
        }

        response = client.post("/api/showcase/department-plans/", data, format="json")

        assert response.status_code == 401

    def test_create_plan_department_not_found(self, make_user):
        """Ошибка: подразделение не найдено."""
        client = APIClient()
        user = make_user(role_code="admin")
        client.force_authenticate(user=user)

        semester = Semester.objects.create(
            code="2024-fall", name="Осенний семестр 2024", position=1
        )

        data = {
            "department_id": 99999,
            "semester_id": semester.id,
            "plan": 10,
        }

        response = client.post("/api/showcase/department-plans/", data, format="json")

        assert response.status_code == 404
        assert "не найдено" in response.data["error"].lower()

    def test_create_plan_semester_not_found(self, make_user, departments):
        """Ошибка: семестр не найден."""
        client = APIClient()
        user = make_user(role_code="admin")
        client.force_authenticate(user=user)

        department = departments["parent"]

        data = {
            "department_id": department.id,
            "semester_id": 99999,
            "plan": 10,
        }

        response = client.post("/api/showcase/department-plans/", data, format="json")

        assert response.status_code == 404
        assert "семестр" in response.data["error"].lower()

    def test_create_plan_negative_value(self, make_user, departments):
        """Ошибка: отрицательное значение plan."""
        client = APIClient()
        user = make_user(role_code="admin")
        client.force_authenticate(user=user)

        semester = Semester.objects.create(
            code="2024-fall", name="Осенний семестр 2024", position=1
        )
        department = departments["parent"]

        data = {
            "department_id": department.id,
            "semester_id": semester.id,
            "plan": -1,
        }

        response = client.post("/api/showcase/department-plans/", data, format="json")

        assert response.status_code == 400

    def test_create_plan_missing_department_id(self, make_user):
        """Ошибка: отсутствует department_id."""
        client = APIClient()
        user = make_user(role_code="admin")
        client.force_authenticate(user=user)

        semester = Semester.objects.create(
            code="2024-fall", name="Осенний семестр 2024", position=1
        )

        data = {
            "semester_id": semester.id,
            "plan": 10,
        }

        response = client.post("/api/showcase/department-plans/", data, format="json")

        assert response.status_code == 400

    def test_create_plan_missing_semester_id(self, make_user, departments):
        """Ошибка: отсутствует semester_id."""
        client = APIClient()
        user = make_user(role_code="admin")
        client.force_authenticate(user=user)

        department = departments["parent"]

        data = {
            "department_id": department.id,
            "plan": 10,
        }

        response = client.post("/api/showcase/department-plans/", data, format="json")

        assert response.status_code == 400

    def test_create_plan_missing_plan(self, make_user, departments):
        """Ошибка: отсутствует plan."""
        client = APIClient()
        user = make_user(role_code="admin")
        client.force_authenticate(user=user)

        semester = Semester.objects.create(
            code="2024-fall", name="Осенний семестр 2024", position=1
        )
        department = departments["parent"]

        data = {
            "department_id": department.id,
            "semester_id": semester.id,
        }

        response = client.post("/api/showcase/department-plans/", data, format="json")

        assert response.status_code == 400

    def test_create_plan_invalid_department_id_type(self, make_user):
        """Ошибка: некорректный тип department_id."""
        client = APIClient()
        user = make_user(role_code="admin")
        client.force_authenticate(user=user)

        semester = Semester.objects.create(
            code="2024-fall", name="Осенний семестр 2024", position=1
        )

        data = {
            "department_id": "invalid",
            "semester_id": semester.id,
            "plan": 10,
        }

        response = client.post("/api/showcase/department-plans/", data, format="json")

        assert response.status_code == 400

    def test_create_plan_invalid_semester_id_type(self, make_user, departments):
        """Ошибка: некорректный тип semester_id."""
        client = APIClient()
        user = make_user(role_code="admin")
        client.force_authenticate(user=user)

        department = departments["parent"]

        data = {
            "department_id": department.id,
            "semester_id": "invalid",
            "plan": 10,
        }

        response = client.post("/api/showcase/department-plans/", data, format="json")

        assert response.status_code == 400

    def test_create_plan_invalid_plan_type(self, make_user, departments):
        """Ошибка: некорректный тип plan."""
        client = APIClient()
        user = make_user(role_code="admin")
        client.force_authenticate(user=user)

        semester = Semester.objects.create(
            code="2024-fall", name="Осенний семестр 2024", position=1
        )
        department = departments["parent"]

        data = {
            "department_id": department.id,
            "semester_id": semester.id,
            "plan": "invalid",
        }

        response = client.post("/api/showcase/department-plans/", data, format="json")

        assert response.status_code == 400

    def test_create_plan_float_value(self, make_user, departments):
        """Ошибка: дробное значение plan."""
        client = APIClient()
        user = make_user(role_code="admin")
        client.force_authenticate(user=user)

        semester = Semester.objects.create(
            code="2024-fall", name="Осенний семестр 2024", position=1
        )
        department = departments["parent"]

        data = {
            "department_id": department.id,
            "semester_id": semester.id,
            "plan": 10.5,
        }

        response = client.post("/api/showcase/department-plans/", data, format="json")

        assert response.status_code == 400


@pytest.mark.django_db
class TestDepartmentPlanViewSetList:
    """Тесты для GET /api/showcase/department-plans/ - получение планов."""

    def test_list_with_institute_code_success(
        self, make_user, departments, statuses, institute
    ):
        """Успешное получение планов дочерних подразделений по коду института."""
        client = APIClient()
        user = make_user(role_code="admin")
        client.force_authenticate(user=user)

        semester = Semester.objects.create(
            code="2024-fall", name="Осенний семестр 2024", position=1
        )
        parent_dept = departments["parent"]
        child_dept = departments["child"]

        # Создаем еще одно дочернее подразделение
        child_dept2 = Department.objects.create(
            name="Child Dept 2", short_name="CD2", parent=parent_dept
        )

        # Создаем планы
        DepartmentPlan.objects.create(department=child_dept, semester=semester, plan=10)
        DepartmentPlan.objects.create(department=child_dept2, semester=semester, plan=5)

        response = client.get(
            f"/api/showcase/department-plans/?institute_code={institute.code}&semester_id={semester.id}"
        )

        assert response.status_code == 200
        assert len(response.data) == 2

        # Проверяем структуру ответа
        dept1_data = next(
            d for d in response.data if d["department_id"] == child_dept.id
        )
        assert dept1_data["department_id"] == child_dept.id
        assert dept1_data["department_name"] == child_dept.name
        assert dept1_data["department_short_name"] == child_dept.short_name
        assert dept1_data["plan"] == 10
        assert isinstance(dept1_data["applications_by_status"], dict)

    def test_list_without_institute_code_success(self, make_user, departments):
        """Успешное получение планов верхнеуровневых подразделений."""
        client = APIClient()
        user = make_user(role_code="admin")
        client.force_authenticate(user=user)

        semester = Semester.objects.create(
            code="2024-fall", name="Осенний семестр 2024", position=1
        )
        parent_dept = departments["parent"]

        # Создаем еще одно верхнеуровневое подразделение
        top_dept2 = Department.objects.create(
            name="Top Dept 2", short_name="TD2", parent=None
        )

        # Создаем планы
        DepartmentPlan.objects.create(
            department=parent_dept, semester=semester, plan=20
        )
        DepartmentPlan.objects.create(department=top_dept2, semester=semester, plan=15)

        response = client.get(
            f"/api/showcase/department-plans/?semester_id={semester.id}"
        )

        assert response.status_code == 200
        assert len(response.data) >= 2

        # Проверяем, что оба подразделения присутствуют
        dept_ids = [d["department_id"] for d in response.data]
        assert parent_dept.id in dept_ids
        assert top_dept2.id in dept_ids

    def test_list_empty_children(self, make_user, departments, institute):
        """Пустой список дочерних подразделений."""
        client = APIClient()
        user = make_user(role_code="admin")
        client.force_authenticate(user=user)

        semester = Semester.objects.create(
            code="2024-fall", name="Осенний семестр 2024", position=1
        )
        parent_dept = departments["parent"]

        # Удаляем дочернее подразделение
        departments["child"].delete()

        response = client.get(
            f"/api/showcase/department-plans/?institute_code={institute.code}&semester_id={semester.id}"
        )

        assert response.status_code == 200
        assert len(response.data) == 0
        assert isinstance(response.data, list)

    def test_list_plan_missing_returns_zero(self, make_user, departments, institute):
        """Если план отсутствует, возвращается 0."""
        client = APIClient()
        user = make_user(role_code="admin")
        client.force_authenticate(user=user)

        semester = Semester.objects.create(
            code="2024-fall", name="Осенний семестр 2024", position=1
        )
        child_dept = departments["child"]

        # Не создаем план для этого подразделения

        response = client.get(
            f"/api/showcase/department-plans/?institute_code={institute.code}&semester_id={semester.id}"
        )

        assert response.status_code == 200
        dept_data = next(
            d for d in response.data if d["department_id"] == child_dept.id
        )
        assert dept_data["plan"] == 0

    def test_list_applications_by_status(
        self, make_user, departments, statuses, institute
    ):
        """Проверка статистики заявок по статусам."""
        client = APIClient()
        user = make_user(role_code="admin")
        client.force_authenticate(user=user)

        semester = Semester.objects.create(
            code="2024-fall", name="Осенний семестр 2024", position=1
        )
        child_dept = departments["child"]

        # Создаем заявки с разными статусами
        ProjectApplication.objects.create(
            main_department=child_dept,
            semester=semester,
            status=statuses["created"],
            title="Заявка 1",
        )
        ProjectApplication.objects.create(
            main_department=child_dept,
            semester=semester,
            status=statuses["created"],
            title="Заявка 2",
        )
        ProjectApplication.objects.create(
            main_department=child_dept,
            semester=semester,
            status=statuses["approved"],
            title="Заявка 3",
        )

        response = client.get(
            f"/api/showcase/department-plans/?institute_code={institute.code}&semester_id={semester.id}"
        )

        assert response.status_code == 200
        dept_data = next(
            d for d in response.data if d["department_id"] == child_dept.id
        )
        assert dept_data["applications_by_status"]["created"] == 2
        assert dept_data["applications_by_status"]["approved"] == 1

    def test_list_no_applications_empty_status(self, make_user, departments, institute):
        """Подразделение без заявок - пустая статистика."""
        client = APIClient()
        user = make_user(role_code="admin")
        client.force_authenticate(user=user)

        semester = Semester.objects.create(
            code="2024-fall", name="Осенний семестр 2024", position=1
        )
        child_dept = departments["child"]

        # Не создаем заявки

        response = client.get(
            f"/api/showcase/department-plans/?institute_code={institute.code}&semester_id={semester.id}"
        )

        assert response.status_code == 200
        dept_data = next(
            d for d in response.data if d["department_id"] == child_dept.id
        )
        assert dept_data["applications_by_status"] == {}

    def test_list_unauthorized(self):
        """Ошибка: неавторизованный пользователь."""
        client = APIClient()
        semester = Semester.objects.create(
            code="2024-fall", name="Осенний семестр 2024", position=1
        )

        response = client.get(
            f"/api/showcase/department-plans/?semester_id={semester.id}"
        )

        assert response.status_code == 401

    def test_list_missing_semester_id(self, make_user, departments, institute):
        """Ошибка: отсутствует semester_id."""
        client = APIClient()
        user = make_user(role_code="admin")
        client.force_authenticate(user=user)

        response = client.get(
            f"/api/showcase/department-plans/?institute_code={institute.code}"
        )

        assert response.status_code == 400
        assert "semester_id" in response.data["error"].lower()

    def test_list_semester_not_found(self, make_user, departments, institute):
        """Ошибка: семестр не найден."""
        client = APIClient()
        user = make_user(role_code="admin")
        client.force_authenticate(user=user)

        response = client.get(
            f"/api/showcase/department-plans/?institute_code={institute.code}&semester_id=99999"
        )

        assert response.status_code == 404
        assert "семестр" in response.data["error"].lower()

    def test_list_institute_not_found(self, make_user):
        """Ошибка: институт не найден."""
        client = APIClient()
        user = make_user(role_code="admin")
        client.force_authenticate(user=user)

        semester = Semester.objects.create(
            code="2024-fall", name="Осенний семестр 2024", position=1
        )

        response = client.get(
            f"/api/showcase/department-plans/?institute_code=UNKNOWN&semester_id={semester.id}"
        )

        assert response.status_code == 404
        assert "не найден" in response.data["error"].lower()

    def test_list_institute_without_department(self, make_user):
        """Ошибка: у института нет связанного подразделения."""
        client = APIClient()
        user = make_user(role_code="admin")
        client.force_authenticate(user=user)

        semester = Semester.objects.create(
            code="2024-fall", name="Осенний семестр 2024", position=1
        )
        institute = Institute.objects.create(
            code="NODEPT", name="No Department", position=2, department=None
        )

        response = client.get(
            f"/api/showcase/department-plans/?institute_code={institute.code}&semester_id={semester.id}"
        )

        assert response.status_code == 404
        assert "не указано связанное подразделение" in response.data["error"].lower()

    def test_list_applications_different_semester_excluded(
        self, make_user, departments, statuses, institute
    ):
        """Заявки из другого семестра не учитываются."""
        client = APIClient()
        user = make_user(role_code="admin")
        client.force_authenticate(user=user)

        semester1 = Semester.objects.create(
            code="2024-fall", name="Осенний семестр 2024", position=1
        )
        semester2 = Semester.objects.create(
            code="2025-spring", name="Весенний семестр 2025", position=2
        )
        child_dept = departments["child"]

        # Создаем заявки в разных семестрах
        ProjectApplication.objects.create(
            main_department=child_dept,
            semester=semester1,
            status=statuses["created"],
            title="Заявка семестр 1",
        )
        ProjectApplication.objects.create(
            main_department=child_dept,
            semester=semester2,
            status=statuses["created"],
            title="Заявка семестр 2",
        )

        response = client.get(
            f"/api/showcase/department-plans/?institute_code={institute.code}&semester_id={semester1.id}"
        )

        assert response.status_code == 200
        dept_data = next(
            d for d in response.data if d["department_id"] == child_dept.id
        )
        # Должна быть только одна заявка из semester1
        assert dept_data["applications_by_status"]["created"] == 1

    def test_list_applications_different_department_excluded(
        self, make_user, departments, statuses, institute
    ):
        """Заявки из другого подразделения не учитываются."""
        client = APIClient()
        user = make_user(role_code="admin")
        client.force_authenticate(user=user)

        semester = Semester.objects.create(
            code="2024-fall", name="Осенний семестр 2024", position=1
        )
        parent_dept = departments["parent"]
        child_dept = departments["child"]

        # Создаем другое подразделение
        other_dept = Department.objects.create(
            name="Other Dept", short_name="OD", parent=None
        )

        # Создаем заявки в разных подразделениях
        ProjectApplication.objects.create(
            main_department=child_dept,
            semester=semester,
            status=statuses["created"],
            title="Заявка child",
        )
        ProjectApplication.objects.create(
            main_department=other_dept,
            semester=semester,
            status=statuses["created"],
            title="Заявка other",
        )

        response = client.get(
            f"/api/showcase/department-plans/?institute_code={institute.code}&semester_id={semester.id}"
        )

        assert response.status_code == 200
        dept_data = next(
            d for d in response.data if d["department_id"] == child_dept.id
        )
        # Должна быть только одна заявка из child_dept
        assert dept_data["applications_by_status"]["created"] == 1

    def test_list_applications_involved_department_included(
        self, make_user, departments, statuses, institute
    ):
        """Заявки, где департамент причастен (но не основной), учитываются."""
        client = APIClient()
        user = make_user(role_code="admin")
        client.force_authenticate(user=user)

        semester = Semester.objects.create(
            code="2024-fall", name="Осенний семестр 2024", position=1
        )
        parent_dept = departments["parent"]
        child_dept = departments["child"]

        # Создаем заявку, где основной департамент другой
        main_dept = Department.objects.create(
            name="Main Dept", short_name="MD", parent=None
        )
        application = ProjectApplication.objects.create(
            main_department=main_dept,
            semester=semester,
            status=statuses["created"],
            title="Заявка другого департамента",
        )
        # Добавляем причастное подразделение (child_dept)
        ApplicationInvolvedDepartment.objects.create(
            application=application, department=child_dept
        )

        response = client.get(
            f"/api/showcase/department-plans/?institute_code={institute.code}&semester_id={semester.id}"
        )

        assert response.status_code == 200
        dept_data = next(
            d for d in response.data if d["department_id"] == child_dept.id
        )
        # Заявка должна учитываться для причастного подразделения
        assert dept_data["applications_by_status"]["created"] == 1

    def test_list_applications_without_status(self, make_user, departments, institute):
        """Заявки без статуса учитываются со значением None."""
        client = APIClient()
        user = make_user(role_code="admin")
        client.force_authenticate(user=user)

        semester = Semester.objects.create(
            code="2024-fall", name="Осенний семестр 2024", position=1
        )
        child_dept = departments["child"]

        # Создаем заявку без статуса
        ProjectApplication.objects.create(
            main_department=child_dept,
            semester=semester,
            status=None,
            title="Заявка без статуса",
        )

        response = client.get(
            f"/api/showcase/department-plans/?institute_code={institute.code}&semester_id={semester.id}"
        )

        assert response.status_code == 200
        dept_data = next(
            d for d in response.data if d["department_id"] == child_dept.id
        )
        # Заявка без статуса учитывается со значением None
        assert None in dept_data["applications_by_status"]
        assert dept_data["applications_by_status"][None] == 1

    def test_list_ordered_by_name(self, make_user, departments, institute):
        """Подразделения отсортированы по имени."""
        client = APIClient()
        user = make_user(role_code="admin")
        client.force_authenticate(user=user)

        semester = Semester.objects.create(
            code="2024-fall", name="Осенний семестр 2024", position=1
        )
        parent_dept = departments["parent"]

        # Создаем дочерние подразделения в разном порядке
        dept_c = Department.objects.create(
            name="C Department", short_name="CD", parent=parent_dept
        )
        dept_a = Department.objects.create(
            name="A Department", short_name="AD", parent=parent_dept
        )
        dept_b = Department.objects.create(
            name="B Department", short_name="BD", parent=parent_dept
        )

        response = client.get(
            f"/api/showcase/department-plans/?institute_code={institute.code}&semester_id={semester.id}"
        )

        assert response.status_code == 200
        # Проверяем порядок (должны быть отсортированы по name)
        dept_names = [d["department_name"] for d in response.data]
        # Находим индексы наших подразделений
        idx_a = dept_names.index("A Department")
        idx_b = dept_names.index("B Department")
        idx_c = dept_names.index("C Department")

        assert idx_a < idx_b < idx_c


@pytest.mark.django_db
class TestDepartmentPlanViewSetMyDepartmentPlan:
    """Тесты для GET /api/showcase/my-department-plan/ - план текущего пользователя."""

    def test_my_department_plan_success(self, make_user, statuses):
        """Успешное получение плана и статистики для подразделения пользователя."""
        client = APIClient()
        user = make_user(role_code="admin", with_department=True)
        client.force_authenticate(user=user)

        semester = Semester.objects.create(
            code="2024-fall", name="Осенний семестр 2024", position=1
        )
        department = user.department

        # План для подразделения
        DepartmentPlan.objects.create(
            department=department,
            semester=semester,
            plan=7,
        )

        # Заявки разного статуса
        ProjectApplication.objects.create(
            main_department=department,
            semester=semester,
            status=statuses["created"],
            title="Заявка 1",
        )
        ProjectApplication.objects.create(
            main_department=department,
            semester=semester,
            status=statuses["approved"],
            title="Заявка 2",
        )

        response = client.get(
            f"/api/showcase/my-department-plan/?semester_id={semester.id}"
        )

        assert response.status_code == 200
        assert response.data["department_id"] == department.id
        assert response.data["department_name"] == department.name
        assert response.data["department_short_name"] == department.short_name
        assert response.data["plan"] == 7
        assert response.data["applications_by_status"]["created"] == 1
        assert response.data["applications_by_status"]["approved"] == 1

    def test_my_department_plan_without_plan_returns_zero(self, make_user, statuses):
        """Если план отсутствует, возвращается 0, но статистика заявок учитывается."""
        client = APIClient()
        user = make_user(role_code="admin", with_department=True)
        client.force_authenticate(user=user)

        semester = Semester.objects.create(
            code="2024-fall", name="Осенний семестр 2024", position=1
        )
        department = user.department

        # План не создаем, только заявки
        ProjectApplication.objects.create(
            main_department=department,
            semester=semester,
            status=statuses["created"],
            title="Заявка 1",
        )

        response = client.get(
            f"/api/showcase/my-department-plan/?semester_id={semester.id}"
        )

        assert response.status_code == 200
        assert response.data["department_id"] == department.id
        assert response.data["plan"] == 0
        assert response.data["applications_by_status"]["created"] == 1

    def test_my_department_plan_missing_semester_id(self, make_user):
        """Ошибка: отсутствует semester_id."""
        client = APIClient()
        user = make_user(role_code="admin", with_department=True)
        client.force_authenticate(user=user)

        response = client.get("/api/showcase/my-department-plan/")

        assert response.status_code == 400
        assert "semester_id" in response.data["error"].lower()

    def test_my_department_plan_semester_not_found(self, make_user):
        """Ошибка: семестр не найден."""
        client = APIClient()
        user = make_user(role_code="admin", with_department=True)
        client.force_authenticate(user=user)

        response = client.get("/api/showcase/my-department-plan/?semester_id=99999")

        assert response.status_code == 404
        assert "семестр" in response.data["error"].lower()

    def test_my_department_plan_user_without_department(self, make_user):
        """Ошибка: у пользователя не указано подразделение."""
        client = APIClient()
        user = make_user(role_code="admin", with_department=False)
        client.force_authenticate(user=user)

        semester = Semester.objects.create(
            code="2024-fall", name="Осенний семестр 2024", position=1
        )

        response = client.get(
            f"/api/showcase/my-department-plan/?semester_id={semester.id}"
        )

        assert response.status_code == 400
        assert "подразделение" in response.data["error"].lower()

    def test_my_department_plan_unauthorized(self):
        """Ошибка: неавторизованный пользователь."""
        client = APIClient()
        semester = Semester.objects.create(
            code="2024-fall", name="Осенний семестр 2024", position=1
        )

        response = client.get(
            f"/api/showcase/my-department-plan/?semester_id={semester.id}"
        )

        assert response.status_code == 401

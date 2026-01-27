"""ViewSet для работы с планами подразделений по проектным заявкам."""

from collections.abc import Iterable

from django.db.models import Q
from rest_framework import permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from accounts.models import Department, Semester
from showcase.models import DepartmentPlan, Institute, ProjectApplication


class DepartmentPlanSerializer(serializers.Serializer):
    """Сериализатор для создания/обновления плана подразделения."""

    department_id = serializers.IntegerField(required=True)
    semester_id = serializers.IntegerField(required=True)
    plan = serializers.IntegerField(required=True, min_value=0)


class DepartmentPlanViewSet(viewsets.ViewSet):
    """ViewSet для операций с планами подразделений."""

    permission_classes = [permissions.IsAuthenticated]

    def create(self, request: Request) -> Response:
        """POST /api/showcase/department-plans/

        Установка плана для подразделения на семестр.
        Тело запроса: {"department_id": 1, "semester_id": 1, "plan": 10}
        """
        serializer = DepartmentPlanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        department_id = serializer.validated_data["department_id"]
        semester_id = serializer.validated_data["semester_id"]
        plan_value = serializer.validated_data["plan"]

        try:
            department = Department.objects.get(pk=department_id)
        except Department.DoesNotExist:
            return Response(
                {"error": f"Подразделение с id={department_id} не найдено"},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            semester = Semester.objects.get(pk=semester_id)
        except Semester.DoesNotExist:
            return Response(
                {"error": f"Семестр с id={semester_id} не найден"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Создаем или обновляем план
        department_plan, created = DepartmentPlan.objects.update_or_create(
            semester=semester,
            department=department,
            defaults={"plan": plan_value},
        )

        return Response(
            {
                "id": department_plan.id,
                "department_id": department_plan.department.id,
                "semester_id": department_plan.semester.id,
                "plan": department_plan.plan,
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )

    def _get_semester_from_query(self, request: Request) -> Semester | Response:
        """Получить и провалидировать семестр из query-параметров.

        Ожидает обязательный параметр semester_id.
        При ошибке возвращает Response с корректным HTTP-статусом.
        """
        semester_id = request.query_params.get("semester_id")

        if not semester_id:
            return Response(
                {"error": "Параметр semester_id обязателен"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            semester = Semester.objects.get(pk=semester_id)
        except Semester.DoesNotExist:
            return Response(
                {"error": f"Семестр с id={semester_id} не найден"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return semester

    def _get_plans_for_departments(
        self,
        departments: Iterable[Department],
        semester: Semester,
    ) -> dict[int, int]:
        """Получить словарь планов по подразделениям для указанного семестра."""
        dept_ids = [d.id for d in departments]
        return {
            plan.department_id: plan.plan
            for plan in DepartmentPlan.objects.filter(
                semester=semester,
                department_id__in=dept_ids,
            )
        }

    def _get_app_stats_for_departments(
        self,
        departments: Iterable[Department],
        semester: Semester,
    ) -> dict[int, dict]:
        """Получить статистику заявок по статусам для каждого подразделения."""
        stats_dict: dict[int, dict] = {}

        dept_ids = {d.id for d in departments}

        # Один запрос, который подтягивает заявки, относящиеся к любому из
        # интересующих нас подразделений (как основное, так и причастное).
        # Далее считаем количество уникальных заявок на стороне Python,
        # чтобы избежать N+1-запросов.
        rows = (
            ProjectApplication.objects.filter(semester=semester)
            .filter(
                Q(main_department_id__in=dept_ids)
                | Q(involved_departments__department_id__in=dept_ids)
            )
            .values(
                "id",
                "status__code",
                "main_department_id",
                "involved_departments__department_id",
            )
        )

        # Временное хранилище для множеств ID заявок:
        # dept_id -> status_code -> set(application_id)
        tmp: dict[int, dict[str | None, set[int]]] = {}

        for row in rows:
            app_id = row["id"]
            status_code = row["status__code"]
            main_dept_id = row["main_department_id"]
            involved_dept_id = row["involved_departments__department_id"]

            for dept_id in (main_dept_id, involved_dept_id):
                if dept_id is None or dept_id not in dept_ids:
                    continue
                status_map = tmp.setdefault(dept_id, {})
                app_ids = status_map.setdefault(status_code, set())
                app_ids.add(app_id)

        # Преобразуем множества в счетчики
        for dept_id, status_map in tmp.items():
            stats_dict[dept_id] = {
                status: len(app_ids) for status, app_ids in status_map.items()
            }

        return stats_dict

    def list(self, request: Request) -> Response:
        """GET /api/showcase/department-plans/?institute_code=INST&semester_id=1

        Получение планов дочерних подразделений с количеством заявок по статусам.
        Если `institute_code` не передан - возвращаются подразделения верхнего уровня.
        """
        institute_code = request.query_params.get("institute_code")

        semester_or_response = self._get_semester_from_query(request)
        if isinstance(semester_or_response, Response):
            return semester_or_response
        semester = semester_or_response

        # Определяем, какие подразделения нужно получить
        if institute_code:
            try:
                institute = Institute.objects.select_related("department").get(
                    code=institute_code
                )
            except Institute.DoesNotExist:
                return Response(
                    {"error": f"Институт с кодом={institute_code} не найден"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            if not institute.department:
                return Response(
                    {
                        "error": (
                            f"У института с кодом={institute_code} "
                            "не указано связанное подразделение"
                        )
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

            parent_department = institute.department
            departments = Department.objects.filter(parent=parent_department)
        else:
            # Верхнеуровневые подразделения (у которых нет родителя)
            departments = Department.objects.filter(parent__isnull=True)

        # Получаем все планы и статистику для этих подразделений и семестра
        plans_dict = self._get_plans_for_departments(departments, semester)
        stats_dict = self._get_app_stats_for_departments(departments, semester)

        # Формируем ответ
        result = []
        for department in departments.order_by("name"):
            plan_value = plans_dict.get(department.id, 0)
            applications_by_status = stats_dict.get(department.id, {})

            result.append(
                {
                    "department_id": department.id,
                    "department_name": department.name,
                    "department_short_name": department.short_name,
                    "plan": plan_value,
                    "applications_by_status": applications_by_status,
                }
            )

        return Response(result)

    @action(detail=False, methods=["get"], url_path="my-department-plan")
    def my_department_plan(self, request: Request) -> Response:
        """GET /api/showcase/my-department-plan/?semester_id=ID

        Возвращает план и статистику заявок для подразделения текущего пользователя.
        """
        semester_or_response = self._get_semester_from_query(request)
        if isinstance(semester_or_response, Response):
            return semester_or_response
        semester = semester_or_response

        user = request.user
        department = getattr(user, "department", None)
        if department is None:
            return Response(
                {"error": "У пользователя не указано подразделение"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        departments = [department]
        plans_dict = self._get_plans_for_departments(departments, semester)
        stats_dict = self._get_app_stats_for_departments(departments, semester)

        plan_value = plans_dict.get(department.id, 0)
        applications_by_status = stats_dict.get(department.id, {})

        return Response(
            {
                "department_id": department.id,
                "department_name": department.name,
                "department_short_name": department.short_name,
                "plan": plan_value,
                "applications_by_status": applications_by_status,
            }
        )

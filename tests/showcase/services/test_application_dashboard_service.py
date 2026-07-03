"""Тесты ApplicationDashboardService."""

from datetime import timedelta

from django.utils import timezone
import pytest

from accounts.models import Department, Semester
from showcase.models import (
    ApplicationInvolvedDepartment,
    ApplicationStatus,
    Institute,
    ProjectApplication,
    ProjectApplicationStatusLog,
)
from showcase.services.application_dashboard_service import ApplicationDashboardService


@pytest.fixture
def semester(db):
    return Semester.objects.create(code="s1", name="S1", position=1)


@pytest.fixture
def second_institute(departments):
    other_parent = Department.objects.create(name="Other Parent", short_name="OP")
    return Institute.objects.create(
        code="OTHER",
        name="Other Institute",
        position=2,
        department=other_parent,
    )


def _create_app(
    *,
    semester: Semester,
    status: ApplicationStatus,
    main_department: Department | None = None,
    involved_department: Department | None = None,
    is_external: bool = False,
    title: str = "Проект",
    institute: Institute | None = None,
) -> ProjectApplication:
    app = ProjectApplication.objects.create(
        title=title,
        company="ООО Тест",
        author_lastname="Иванов",
        author_firstname="Иван",
        author_email="ivan@example.com",
        semester=semester,
        status=status,
        main_department=main_department,
        is_external=is_external,
        goal="Длинная цель проекта больше пятидесяти символов для валидации",
        problem_holder="Носитель",
        barrier="Длинный барьер больше пятидесяти символов для валидации",
    )
    if involved_department is not None:
        ApplicationInvolvedDepartment.objects.create(
            application=app,
            department=involved_department,
        )
    if institute is not None:
        app.target_institutes.add(institute)
    return app


@pytest.mark.django_db
class TestApplicationDashboardService:
    """Тесты сервиса дашборда."""

    def test_dashboard_structure(
        self, statuses, institute, semester, departments, make_user
    ):
        """Ответ содержит все ключи виджетов."""
        _create_app(
            semester=semester,
            status=statuses["approved"],
            main_department=departments["child"],
            institute=institute,
        )
        user = make_user(role_code="admin")
        service = ApplicationDashboardService()

        data = service.get_dashboard(
            user=user,
            semester_id_raw=str(semester.pk),
            institute_code=None,
            department_id_raw=None,
            status_raw=None,
            application_type_raw=None,
            days_raw=None,
        )

        assert set(data.keys()) == {
            "filters_applied",
            "summary_cards",
            "rating_chart",
            "external_share_chart",
            "status_distribution",
            "application_type_distribution",
            "daily_dynamics",
            "oldest_in_progress",
        }
        assert len(data["summary_cards"]["cards"]) == 5
        assert data["summary_cards"]["cards"][0]["id"] == "total"
        assert data["summary_cards"]["cards"][0]["value"] == 1

    def test_department_subtree_filter_includes_child(
        self, statuses, institute, semester, departments, make_user
    ):
        """Заявка дочернего подразделения видна при фильтре по родителю."""
        _create_app(
            semester=semester,
            status=statuses["created"],
            main_department=departments["child"],
            institute=institute,
        )
        user = make_user(role_code="admin")
        service = ApplicationDashboardService()

        data_parent = service.get_dashboard(
            user=user,
            semester_id_raw=str(semester.pk),
            institute_code=None,
            department_id_raw=str(departments["parent"].pk),
            status_raw=None,
            application_type_raw=None,
            days_raw=None,
        )
        assert data_parent["summary_cards"]["cards"][0]["value"] == 1

        other_dept = Department.objects.create(name="Alien", short_name="AL")
        _create_app(
            semester=semester,
            status=statuses["created"],
            main_department=other_dept,
        )

        data_parent_after = service.get_dashboard(
            user=user,
            semester_id_raw=str(semester.pk),
            institute_code=None,
            department_id_raw=str(departments["parent"].pk),
            status_raw=None,
            application_type_raw=None,
            days_raw=None,
        )
        assert data_parent_after["summary_cards"]["cards"][0]["value"] == 1

    def test_application_type_external_filter(
        self, statuses, semester, departments, make_user
    ):
        """Фильтр application_type=external."""
        _create_app(
            semester=semester,
            status=statuses["created"],
            main_department=departments["child"],
            is_external=True,
        )
        _create_app(
            semester=semester,
            status=statuses["created"],
            main_department=departments["child"],
            is_external=False,
        )
        user = make_user(role_code="admin")
        service = ApplicationDashboardService()

        data = service.get_dashboard(
            user=user,
            semester_id_raw=str(semester.pk),
            institute_code=None,
            department_id_raw=None,
            status_raw=None,
            application_type_raw="external",
            days_raw=None,
        )
        assert data["summary_cards"]["cards"][0]["value"] == 1

    def test_status_group_filter(self, statuses, semester, departments, make_user):
        """Фильтр по группам статусов."""
        _create_app(
            semester=semester,
            status=statuses["approved"],
            main_department=departments["child"],
        )
        _create_app(
            semester=semester,
            status=statuses["created"],
            main_department=departments["child"],
        )
        user = make_user(role_code="admin")
        service = ApplicationDashboardService()

        data = service.get_dashboard(
            user=user,
            semester_id_raw=str(semester.pk),
            institute_code=None,
            department_id_raw=None,
            status_raw="approved",
            application_type_raw=None,
            days_raw=None,
        )
        assert data["summary_cards"]["cards"][0]["value"] == 1

    def test_in_work_card_is_total_minus_approved_minus_rejected(
        self, statuses, semester, departments, make_user
    ):
        """Карточка in_work = total - approved - rejected."""
        _create_app(
            semester=semester,
            status=statuses["approved"],
            main_department=departments["child"],
        )
        _create_app(
            semester=semester,
            status=statuses["rejected"],
            main_department=departments["child"],
        )
        _create_app(
            semester=semester,
            status=statuses["created"],
            main_department=departments["child"],
        )
        _create_app(
            semester=semester,
            status=statuses["await_department"],
            main_department=departments["child"],
        )
        user = make_user(role_code="admin")
        service = ApplicationDashboardService()
        data = service.get_dashboard(
            user=user,
            semester_id_raw=str(semester.pk),
            institute_code=None,
            department_id_raw=None,
            status_raw=None,
            application_type_raw=None,
            days_raw=None,
        )

        cards = {card["id"]: card for card in data["summary_cards"]["cards"]}
        assert cards["total"]["value"] == 4
        assert cards["approved"]["value"] == 1
        assert cards["rejected"]["value"] == 1
        assert cards["in_work"]["value"] == 2
        assert cards["in_work"]["label"] == "В РАБОТЕ"

    def test_resolution_time_metrics(self, statuses, semester, departments, make_user):
        """Среднее и медиана времени до решения."""
        app = _create_app(
            semester=semester,
            status=statuses["approved"],
            main_department=departments["child"],
        )
        ProjectApplication.objects.filter(pk=app.pk).update(
            creation_date=timezone.now() - timedelta(days=10)
        )
        ProjectApplicationStatusLog.objects.create(
            application=app,
            action_type="status_change",
            to_status=statuses["approved"],
        )

        user = make_user(role_code="admin")
        service = ApplicationDashboardService()
        data = service.get_dashboard(
            user=user,
            semester_id_raw=str(semester.pk),
            institute_code=None,
            department_id_raw=None,
            status_raw=None,
            application_type_raw=None,
            days_raw=None,
        )

        avg_card = data["summary_cards"]["cards"][4]
        assert avg_card["id"] == "avg_resolution_days"
        assert avg_card["value"] >= 0

    def test_oldest_in_progress_lists_created_apps(
        self, statuses, semester, departments, make_user
    ):
        """Топ старых заявок включает заявки в статусе in_progress."""
        _create_app(
            semester=semester,
            status=statuses["created"],
            main_department=departments["child"],
            institute=None,
        )
        user = make_user(role_code="admin")
        service = ApplicationDashboardService()
        data = service.get_dashboard(
            user=user,
            semester_id_raw=str(semester.pk),
            institute_code=None,
            department_id_raw=None,
            status_raw=None,
            application_type_raw=None,
            days_raw=None,
        )
        assert len(data["oldest_in_progress"]["items"]) == 1

    def test_institute_validator_forbidden_for_other_institute(
        self, statuses, institute, second_institute, semester, departments, make_user
    ):
        """institute_validator не видит чужой институт."""
        user = make_user(role_code="institute_validator", with_department=True)
        user.department = departments["parent"]
        user.save()

        service = ApplicationDashboardService()
        with pytest.raises(PermissionError):
            service.get_dashboard(
                user=user,
                semester_id_raw=str(semester.pk),
                institute_code=second_institute.code,
                department_id_raw=None,
                status_raw=None,
                application_type_raw=None,
                days_raw=None,
            )

    def test_regular_user_forbidden(self, semester, make_user):
        """Обычный пользователь не имеет доступа."""
        user = make_user(role_code="user")
        service = ApplicationDashboardService()
        with pytest.raises(PermissionError):
            service.get_dashboard(
                user=user,
                semester_id_raw=str(semester.pk),
                institute_code=None,
                department_id_raw=None,
                status_raw=None,
                application_type_raw=None,
                days_raw=None,
            )

    def test_rating_chart_departments_sorted_by_total_desc(
        self, statuses, institute, semester, departments, make_user
    ):
        """Рейтинг по подразделениям отсортирован по убыванию числа заявок."""
        dept_a = Department.objects.create(
            name="Dept A", short_name="DA", parent=departments["parent"]
        )
        dept_b = Department.objects.create(
            name="Dept B", short_name="DB", parent=departments["parent"]
        )
        dept_c = Department.objects.create(
            name="Dept C", short_name="DC", parent=departments["parent"]
        )

        for _ in range(3):
            _create_app(
                semester=semester,
                status=statuses["approved"],
                main_department=dept_b,
                institute=institute,
            )
        for _ in range(2):
            _create_app(
                semester=semester,
                status=statuses["created"],
                main_department=dept_c,
                institute=institute,
            )
        _create_app(
            semester=semester,
            status=statuses["rejected"],
            main_department=dept_a,
            institute=institute,
        )

        user = make_user(role_code="admin")
        service = ApplicationDashboardService()
        data = service.get_dashboard(
            user=user,
            semester_id_raw=str(semester.pk),
            institute_code=institute.code,
            department_id_raw=None,
            status_raw=None,
            application_type_raw=None,
            days_raw=None,
        )

        assert data["rating_chart"]["dimension"] == "department"
        category_ids = [
            category["id"] for category in data["rating_chart"]["categories"]
        ]
        our_departments = {dept_a.id, dept_b.id, dept_c.id}
        sorted_our = [dept_id for dept_id in category_ids if dept_id in our_departments]
        assert sorted_our == [dept_b.id, dept_c.id, dept_a.id]

    def test_external_share_chart_by_departments(
        self, statuses, institute, semester, departments, make_user
    ):
        """Доля внешних заявок считается по каждому подразделению."""
        dept_a = Department.objects.create(
            name="Dept A", short_name="DA", parent=departments["parent"]
        )
        dept_b = Department.objects.create(
            name="Dept B", short_name="DB", parent=departments["parent"]
        )

        _create_app(
            semester=semester,
            status=statuses["created"],
            main_department=dept_a,
            institute=institute,
            is_external=True,
        )
        _create_app(
            semester=semester,
            status=statuses["created"],
            main_department=dept_a,
            institute=institute,
            is_external=False,
        )
        for _ in range(3):
            _create_app(
                semester=semester,
                status=statuses["created"],
                main_department=dept_b,
                institute=institute,
                is_external=True,
            )

        user = make_user(role_code="admin")
        service = ApplicationDashboardService()
        data = service.get_dashboard(
            user=user,
            semester_id_raw=str(semester.pk),
            institute_code=institute.code,
            department_id_raw=None,
            status_raw=None,
            application_type_raw=None,
            days_raw=None,
        )

        chart = data["external_share_chart"]
        assert chart["id"] == "external_share_chart"
        assert chart["dimension"] == "department"
        assert chart["type"] == "vertical_bar"

        items_by_id = {item["category"]["id"]: item for item in chart["items"]}
        assert items_by_id[dept_a.id]["total"] == 2
        assert items_by_id[dept_a.id]["external_count"] == 1
        assert items_by_id[dept_a.id]["percent"] == 50.0
        assert items_by_id[dept_b.id]["total"] == 3
        assert items_by_id[dept_b.id]["external_count"] == 3
        assert items_by_id[dept_b.id]["percent"] == 100.0

        percents = chart["series"][0]["data"]
        assert percents[0] == 100.0
        assert percents[1] == 50.0

    def test_rating_chart_switches_to_departments_with_department_filter(
        self, statuses, institute, semester, departments, make_user
    ):
        """При department_id рейтинг переключается на подразделения."""
        _create_app(
            semester=semester,
            status=statuses["approved"],
            main_department=departments["child"],
            institute=institute,
        )
        user = make_user(role_code="admin")
        service = ApplicationDashboardService()
        data = service.get_dashboard(
            user=user,
            semester_id_raw=str(semester.pk),
            institute_code=None,
            department_id_raw=str(departments["parent"].pk),
            status_raw=None,
            application_type_raw=None,
            days_raw=None,
        )
        assert data["rating_chart"]["dimension"] == "department"

    def test_rating_chart_shows_from_institute_row_for_parent_only_apps(
        self, statuses, institute, semester, departments, make_user
    ):
        """Заявки только на уровне института попадают в строку «От института»."""
        _create_app(
            semester=semester,
            status=statuses["approved"],
            main_department=departments["child"],
            institute=institute,
        )
        _create_app(
            semester=semester,
            status=statuses["created"],
            main_department=departments["parent"],
            institute=institute,
        )
        _create_app(
            semester=semester,
            status=statuses["rejected"],
            main_department=departments["parent"],
            institute=institute,
        )

        user = make_user(role_code="admin")
        service = ApplicationDashboardService()
        data = service.get_dashboard(
            user=user,
            semester_id_raw=str(semester.pk),
            institute_code=None,
            department_id_raw=str(departments["parent"].pk),
            status_raw=None,
            application_type_raw=None,
            days_raw=None,
        )

        categories = data["rating_chart"]["categories"]
        from_institute = next(
            (item for item in categories if item["name"] == "От института"),
            None,
        )
        assert from_institute is not None
        assert from_institute["id"] == departments["parent"].id
        assert from_institute["parent_id"] == departments["parent"].id

        from_institute_index = categories.index(from_institute)
        series = data["rating_chart"]["series"]
        assert series[0]["data"][from_institute_index] == 0
        assert series[1]["data"][from_institute_index] == 1
        assert series[2]["data"][from_institute_index] == 1

    def test_rating_chart_from_institute_excludes_apps_with_child_department(
        self, statuses, institute, semester, departments, make_user
    ):
        """Заявка с кафедрой не дублируется в строке «От института»."""
        _create_app(
            semester=semester,
            status=statuses["approved"],
            main_department=departments["parent"],
            involved_department=departments["child"],
            institute=institute,
        )

        user = make_user(role_code="admin")
        service = ApplicationDashboardService()
        data = service.get_dashboard(
            user=user,
            semester_id_raw=str(semester.pk),
            institute_code=None,
            department_id_raw=str(departments["parent"].pk),
            status_raw=None,
            application_type_raw=None,
            days_raw=None,
        )

        categories = data["rating_chart"]["categories"]
        assert not any(item["name"] == "От института" for item in categories)
        child_category = next(
            item for item in categories if item["id"] == departments["child"].id
        )
        child_index = categories.index(child_category)
        assert data["rating_chart"]["series"][0]["data"][child_index] == 1

    def test_rating_chart_from_institute_with_institute_filter(
        self, statuses, institute, semester, departments, make_user
    ):
        """При фильтре по институту строка «От института» тоже отображается."""
        _create_app(
            semester=semester,
            status=statuses["approved"],
            main_department=departments["parent"],
            institute=institute,
        )

        user = make_user(role_code="admin")
        service = ApplicationDashboardService()
        data = service.get_dashboard(
            user=user,
            semester_id_raw=str(semester.pk),
            institute_code=institute.code,
            department_id_raw=None,
            status_raw=None,
            application_type_raw=None,
            days_raw=None,
        )

        categories = data["rating_chart"]["categories"]
        from_institute = next(
            (item for item in categories if item["name"] == "От института"),
            None,
        )
        assert from_institute is not None
        assert from_institute["id"] == institute.department_id
        assert from_institute["code"] == institute.code

    def test_rating_chart_nested_department_rolls_up_to_direct_child(
        self, statuses, institute, semester, departments, make_user
    ):
        """Заявка на вложенном подразделении учитывается в прямой дочерней кафедре."""
        nested = Department.objects.create(
            name="Nested Dept",
            short_name="ND",
            parent=departments["child"],
        )
        _create_app(
            semester=semester,
            status=statuses["approved"],
            main_department=nested,
            institute=institute,
        )

        user = make_user(role_code="admin")
        service = ApplicationDashboardService()
        data = service.get_dashboard(
            user=user,
            semester_id_raw=str(semester.pk),
            institute_code=institute.code,
            department_id_raw=None,
            status_raw=None,
            application_type_raw=None,
            days_raw=None,
        )

        categories = data["rating_chart"]["categories"]
        child_category = next(
            item for item in categories if item["id"] == departments["child"].id
        )
        child_index = categories.index(child_category)
        assert data["rating_chart"]["series"][0]["data"][child_index] == 1
        assert not any(item["name"] == "От института" for item in categories)

    def test_rating_chart_series_has_three_categories(
        self, statuses, institute, semester, departments, make_user
    ):
        """rating_chart.series содержит только approved, in_work, rejected."""
        _create_app(
            semester=semester,
            status=statuses["approved"],
            main_department=departments["child"],
            institute=institute,
        )
        _create_app(
            semester=semester,
            status=statuses["rejected"],
            main_department=departments["child"],
            institute=institute,
        )
        _create_app(
            semester=semester,
            status=statuses["created"],
            main_department=departments["child"],
            institute=institute,
        )
        _create_app(
            semester=semester,
            status=statuses["await_department"],
            main_department=departments["child"],
            institute=institute,
        )
        user = make_user(role_code="admin")
        service = ApplicationDashboardService()
        data = service.get_dashboard(
            user=user,
            semester_id_raw=str(semester.pk),
            institute_code=None,
            department_id_raw=None,
            status_raw=None,
            application_type_raw=None,
            days_raw=None,
        )

        series = data["rating_chart"]["series"]
        assert [item["id"] for item in series] == ["approved", "in_work", "rejected"]
        assert len(series) == 3

        institute_index = next(
            index
            for index, category in enumerate(data["rating_chart"]["categories"])
            if category["id"] == institute.department_id
        )
        assert series[0]["data"][institute_index] == 1
        assert series[1]["data"][institute_index] == 2
        assert series[2]["data"][institute_index] == 1

    def test_category_includes_institute_code(
        self, statuses, institute, semester, departments, make_user
    ):
        """Объект подразделения в categories содержит code института."""
        _create_app(
            semester=semester,
            status=statuses["approved"],
            main_department=departments["child"],
            institute=institute,
        )
        user = make_user(role_code="admin")
        service = ApplicationDashboardService()
        data = service.get_dashboard(
            user=user,
            semester_id_raw=str(semester.pk),
            institute_code=None,
            department_id_raw=None,
            status_raw=None,
            application_type_raw=None,
            days_raw=None,
        )

        category = data["rating_chart"]["categories"][0]
        assert category["id"] == institute.department_id
        assert category["code"] == institute.code

    def test_department_child_includes_parent_institute_code(
        self, statuses, institute, semester, departments, make_user
    ):
        """Дочернее подразделение получает code института из иерархии."""
        _create_app(
            semester=semester,
            status=statuses["approved"],
            main_department=departments["child"],
            institute=institute,
        )
        user = make_user(role_code="admin")
        service = ApplicationDashboardService()
        data = service.get_dashboard(
            user=user,
            semester_id_raw=str(semester.pk),
            institute_code=institute.code,
            department_id_raw=None,
            status_raw=None,
            application_type_raw=None,
            days_raw=None,
        )

        category = next(
            item
            for item in data["rating_chart"]["categories"]
            if item["id"] == departments["child"].id
        )
        assert category["code"] == institute.code

    def test_status_distribution_segments(
        self, statuses, semester, departments, make_user
    ):
        """Распределение по статусам: approved, in_work, rejected."""
        _create_app(
            semester=semester,
            status=statuses["approved"],
            main_department=departments["child"],
        )
        _create_app(
            semester=semester,
            status=statuses["created"],
            main_department=departments["child"],
        )
        _create_app(
            semester=semester,
            status=statuses["await_department"],
            main_department=departments["child"],
        )
        _create_app(
            semester=semester,
            status=statuses["returned_department"],
            main_department=departments["child"],
        )
        user = make_user(role_code="admin")
        service = ApplicationDashboardService()
        data = service.get_dashboard(
            user=user,
            semester_id_raw=str(semester.pk),
            institute_code=None,
            department_id_raw=None,
            status_raw=None,
            application_type_raw=None,
            days_raw=None,
        )

        segments = data["status_distribution"]["segments"]
        assert [segment["group"] for segment in segments] == [
            "approved",
            "in_work",
            "rejected",
        ]
        assert len(segments) == 3

        segments_by_group = {segment["group"]: segment for segment in segments}
        assert segments_by_group["approved"]["count"] == 1
        assert segments_by_group["in_work"]["count"] == 3
        assert segments_by_group["in_work"]["label"] == "В работе"
        assert segments_by_group["rejected"]["count"] == 0

    def test_application_type_distribution_pie_segments(
        self, statuses, semester, departments, make_user
    ):
        """pie chart по внутренним/внешним заявкам содержит 2 сегмента."""
        _create_app(
            semester=semester,
            status=statuses["created"],
            main_department=departments["child"],
            is_external=False,
        )
        _create_app(
            semester=semester,
            status=statuses["created"],
            main_department=departments["child"],
            is_external=True,
        )
        user = make_user(role_code="admin")
        service = ApplicationDashboardService()
        data = service.get_dashboard(
            user=user,
            semester_id_raw=str(semester.pk),
            institute_code=None,
            department_id_raw=None,
            status_raw=None,
            application_type_raw=None,
            days_raw=None,
        )

        widget = data["application_type_distribution"]
        assert widget["type"] == "pie"
        assert len(widget["segments"]) == 2
        segments = {s["group"]: s for s in widget["segments"]}
        assert segments["internal"]["count"] == 1
        assert segments["external"]["count"] == 1

    def test_oldest_in_progress_no_n_plus_one_queries(
        self, statuses, semester, departments, make_user
    ):
        """Число запросов для oldest_in_progress не растёт линейно с числом заявок."""
        from django.db import connection
        from django.test.utils import CaptureQueriesContext

        from showcase.domain.application_dashboard import DashboardFilters
        from showcase.repositories.application_dashboard import (
            ApplicationDashboardRepository,
        )

        def count_oldest_queries(app_count: int) -> int:
            ProjectApplication.objects.filter(semester=semester).delete()
            for index in range(app_count):
                _create_app(
                    semester=semester,
                    status=statuses["created"],
                    main_department=departments["child"],
                    title=f"Проект {index}",
                )

            filters = DashboardFilters(
                semester_id=semester.pk,
                institute_code=None,
                department_id=None,
                status_groups=("in_progress",),
                application_type="all",
                days=30,
                accessible_institute_codes=None,
            )
            repository = ApplicationDashboardRepository()
            queryset = repository.get_filtered_queryset(filters)
            with CaptureQueriesContext(connection) as context:
                repository.get_oldest_in_progress(queryset)
            return len(context.captured_queries)

        queries_for_five = count_oldest_queries(5)
        queries_for_twenty = count_oldest_queries(20)

        assert queries_for_twenty <= queries_for_five + 1

    def test_dashboard_department_code_map_no_n_plus_one_queries(
        self, statuses, institute, semester, departments, make_user
    ):
        """Построение code для подразделений не даёт N+1 при росте числа заявок."""
        from django.db import connection
        from django.test.utils import CaptureQueriesContext

        user = make_user(role_code="admin")
        service = ApplicationDashboardService()

        def count_dashboard_queries(app_count: int) -> int:
            ProjectApplication.objects.filter(semester=semester).delete()
            for index in range(app_count):
                _create_app(
                    semester=semester,
                    status=statuses["created"],
                    main_department=departments["child"],
                    institute=institute,
                    title=f"Проект {index}",
                )

            with CaptureQueriesContext(connection) as context:
                service.get_dashboard(
                    user=user,
                    semester_id_raw=str(semester.pk),
                    institute_code=institute.code,
                    department_id_raw=None,
                    status_raw=None,
                    application_type_raw=None,
                    days_raw=None,
                )
            return len(context.captured_queries)

        queries_for_five = count_dashboard_queries(5)
        queries_for_twenty = count_dashboard_queries(20)

        assert queries_for_twenty <= queries_for_five + 1

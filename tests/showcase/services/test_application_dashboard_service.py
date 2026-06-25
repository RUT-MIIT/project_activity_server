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
            "status_distribution",
            "daily_dynamics",
            "oldest_in_progress",
        }
        assert len(data["summary_cards"]["cards"]) == 4
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

        avg_card = data["summary_cards"]["cards"][3]
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

    def test_status_distribution_segments(
        self, statuses, semester, departments, make_user
    ):
        """Распределение по статусам содержит 4 сегмента."""
        _create_app(
            semester=semester,
            status=statuses["approved"],
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
        assert len(data["status_distribution"]["segments"]) == 4

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

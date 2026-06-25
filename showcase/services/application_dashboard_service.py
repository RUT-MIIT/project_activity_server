"""Сервис дашборда проектных заявок."""

from __future__ import annotations

from accounts.models import Semester, User
from showcase.domain.application_dashboard import (
    ApplicationDashboardDomain,
    DashboardFilters,
)
from showcase.dto.application_dashboard import ApplicationDashboardDTO, SummaryCardsDTO
from showcase.repositories.application_dashboard import ApplicationDashboardRepository


class ApplicationDashboardService:
    """Оркестрация получения данных дашборда заявок."""

    def __init__(self) -> None:
        self.domain = ApplicationDashboardDomain()
        self.repository = ApplicationDashboardRepository()

    def get_dashboard(
        self,
        user: User,
        semester_id_raw: str,
        institute_code: str | None,
        department_id_raw: str | None,
        status_raw: str | None,
        application_type_raw: str | None,
        days_raw: str | None,
    ) -> dict:
        """Возвращает полную структуру дашборда."""
        can_view, error = self.domain.can_view_dashboard(user)
        if not can_view:
            raise PermissionError(error)

        semester_id = Semester.resolve_list_semester_id(semester_id_raw)
        institute_code = self.domain.validate_institute_access(user, institute_code)

        department_id: int | None = None
        if department_id_raw is not None and str(department_id_raw).strip():
            try:
                department_id = int(department_id_raw)
            except ValueError as err:
                raise ValueError(
                    "Параметр department_id должен быть целым числом"
                ) from err
            if department_id <= 0:
                raise ValueError("Параметр department_id должен быть положительным")

        status_groups = self.domain.parse_status_groups(status_raw)
        application_type = self.domain.parse_application_type(application_type_raw)
        days = self.domain.parse_days(days_raw)

        if department_id is not None:
            self.domain.resolve_department_subtree_ids(department_id)

        if institute_code:
            from showcase.models import Institute

            if not Institute.objects.filter(
                code=institute_code, is_active=True
            ).exists():
                raise ValueError(f"Институт с кодом={institute_code} не найден")

        accessible_codes = self.domain.get_accessible_institute_codes(user)

        filters = DashboardFilters(
            semester_id=semester_id,
            institute_code=institute_code,
            department_id=department_id,
            status_groups=status_groups,
            application_type=application_type,
            days=days,
            accessible_institute_codes=accessible_codes,
        )

        queryset = self.repository.get_filtered_queryset(filters)
        summary_data = self.repository.get_summary_data(queryset)

        dto = ApplicationDashboardDTO(
            filters_applied={
                "semester_id": semester_id,
                "institute_code": institute_code,
                "department_id": department_id,
                "status_groups": list(status_groups),
                "application_type": application_type,
                "days": days,
            },
            summary_cards=SummaryCardsDTO(summary_data).to_dict(),
            rating_chart=self.repository.get_rating_chart_data(queryset, filters),
            status_distribution=self.repository.get_status_distribution(queryset),
            daily_dynamics=self.repository.get_daily_dynamics(queryset, days),
            oldest_in_progress=self.repository.get_oldest_in_progress(queryset),
        )
        return dto.to_dict()

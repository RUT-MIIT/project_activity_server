"""Репозиторий агрегаций для дашборда проектных заявок."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from datetime import datetime, timedelta
from statistics import median

from django.db.models import Count, Min, OuterRef, Q, QuerySet, Subquery
from django.utils import timezone

from accounts.models import Department
from accounts.utils import get_department_subtree_ids
from showcase.domain.application_dashboard import (
    FINAL_RESOLUTION_STATUS_CODES,
    STATUS_GROUPS,
    ApplicationDashboardDomain,
    DashboardFilters,
)
from showcase.models import Institute, ProjectApplication, ProjectApplicationStatusLog
from teams.domain.institute_access import (
    get_department_ids_by_institute_code,
    get_department_ids_for_institute_codes,
)


class ApplicationDashboardRepository:
    """ORM-запросы и агрегации для дашборда заявок."""

    def __init__(self) -> None:
        self.domain = ApplicationDashboardDomain()

    @staticmethod
    def _institute_access_q(institute_codes: list[str], prefix: str = "") -> Q:
        """Q-фильтр: заявка доступна институту."""
        if not institute_codes:
            return Q(pk__in=[])

        department_ids = get_department_ids_for_institute_codes(institute_codes)
        involved_q = Q()
        if department_ids:
            involved_q = Q(
                **{f"{prefix}involved_departments__department_id__in": department_ids}
            ) | Q(**{f"{prefix}main_department_id__in": department_ids})

        targets_q = Q(**{f"{prefix}target_institutes__code__in": institute_codes})
        return involved_q | targets_q

    def get_filtered_queryset(
        self, filters: DashboardFilters
    ) -> QuerySet[ProjectApplication]:
        """Базовый queryset заявок с учётом всех фильтров."""
        status_codes = self.domain.expand_status_filter(filters.status_groups)
        queryset = (
            ProjectApplication.objects.filter(semester_id=filters.semester_id)
            .filter(status__code__in=status_codes)
            .select_related("status", "main_department")
            .prefetch_related("target_institutes", "involved_departments")
        )

        if filters.application_type == "external":
            queryset = queryset.filter(is_external=True)
        elif filters.application_type == "internal":
            queryset = queryset.filter(is_external=False)

        if filters.department_id is not None:
            dept_ids = self.domain.resolve_department_subtree_ids(filters.department_id)
            queryset = queryset.filter(
                Q(main_department_id__in=dept_ids)
                | Q(involved_departments__department_id__in=dept_ids)
            )

        if filters.institute_code:
            queryset = queryset.filter(
                self._institute_access_q([filters.institute_code])
            )

        if filters.accessible_institute_codes is not None:
            queryset = queryset.filter(
                self._institute_access_q(filters.accessible_institute_codes)
            )

        return queryset.distinct()

    def get_summary_data(self, queryset: QuerySet[ProjectApplication]) -> dict:
        """Сводные KPI: total, approved, rejected, resolution times."""
        now = timezone.now()
        week_ago = now - timedelta(days=7)

        aggregates = queryset.aggregate(
            total=Count("id"),
            approved_count=Count(
                "id", filter=Q(status__code__in=STATUS_GROUPS["approved"])
            ),
            rejected_count=Count(
                "id", filter=Q(status__code__in=STATUS_GROUPS["rejected"])
            ),
            recent_count=Count("id", filter=Q(creation_date__gte=week_ago)),
        )
        total = aggregates["total"]
        approved_count = aggregates["approved_count"]
        rejected_count = aggregates["rejected_count"]
        recent_count = aggregates["recent_count"]

        app_ids = list(queryset.values_list("id", flat=True))
        resolution_days: list[int] = []
        if app_ids:
            resolved_logs = (
                ProjectApplicationStatusLog.objects.filter(
                    application_id__in=app_ids,
                    action_type="status_change",
                    to_status__code__in=FINAL_RESOLUTION_STATUS_CODES,
                )
                .values("application_id")
                .annotate(first_resolved_at=Min("changed_at"))
            )
            creation_map = dict(
                queryset.filter(pk__in=app_ids).values_list("id", "creation_date")
            )
            for row in resolved_logs:
                app_id = row["application_id"]
                creation_date = creation_map.get(app_id)
                resolved_at = row["first_resolved_at"]
                if creation_date and resolved_at:
                    delta = resolved_at - creation_date
                    resolution_days.append(max(delta.days, 0))

        avg_days = (
            round(sum(resolution_days) / len(resolution_days), 1)
            if resolution_days
            else 0.0
        )
        median_days = round(median(resolution_days), 1) if resolution_days else 0.0

        return {
            "total": total,
            "recent_count": recent_count,
            "approved_count": approved_count,
            "rejected_count": rejected_count,
            "avg_resolution_days": avg_days,
            "median_resolution_days": median_days,
        }

    def _aggregate_by_dimension(
        self,
        queryset: QuerySet[ProjectApplication],
        dimension_map: dict[str, set[int]],
    ) -> dict[str, dict[str, int]]:
        """Агрегирует заявки по измерению (institute/department) и группе статуса."""
        result: dict[str, dict[str, int]] = {
            key: {group: 0 for group in STATUS_GROUPS} for key in dimension_map
        }

        all_app_ids: set[int] = set()
        for app_ids in dimension_map.values():
            all_app_ids.update(app_ids)
        if not all_app_ids:
            return result

        status_by_app = {
            row["id"]: self.domain.status_code_to_group(row["status__code"])
            for row in queryset.filter(id__in=all_app_ids).values("id", "status__code")
        }

        for key, app_ids in dimension_map.items():
            for app_id in app_ids:
                group = status_by_app.get(app_id)
                if group:
                    result[key][group] += 1

        return result

    def _build_institute_dimension_map(
        self,
        queryset: QuerySet[ProjectApplication],
        institutes: Iterable[Institute],
    ) -> dict[str, set[int]]:
        """Строит карту institute_code -> множество id заявок."""
        app_ids = set(queryset.values_list("id", flat=True))
        if not app_ids:
            return {inst.code: set() for inst in institutes}

        institute_codes = [inst.code for inst in institutes]
        dept_ids_by_institute = get_department_ids_by_institute_code(institute_codes)

        rows = (
            ProjectApplication.objects.filter(id__in=app_ids)
            .values(
                "id",
                "main_department_id",
                "involved_departments__department_id",
                "target_institutes__code",
            )
            .distinct()
        )

        dimension_map: dict[str, set[int]] = {code: set() for code in institute_codes}
        for row in rows:
            app_id = row["id"]
            main_dept_id = row["main_department_id"]
            involved_dept_id = row["involved_departments__department_id"]
            target_code = row["target_institutes__code"]

            for code in institute_codes:
                matched = False
                if target_code == code:
                    matched = True
                else:
                    allowed = dept_ids_by_institute[code]
                    if main_dept_id in allowed or involved_dept_id in allowed:
                        matched = True
                if matched:
                    dimension_map[code].add(app_id)

        return dimension_map

    def _build_department_dimension_map(
        self,
        queryset: QuerySet[ProjectApplication],
        departments: Iterable[Department],
    ) -> dict[str, set[int]]:
        """Строит карту department_id -> множество id заявок (как в DepartmentPlan)."""
        dept_list = list(departments)
        dept_ids = {dept.id for dept in dept_list}
        if not dept_ids:
            return {}

        rows = (
            queryset.filter(
                Q(main_department_id__in=dept_ids)
                | Q(involved_departments__department_id__in=dept_ids)
            )
            .values(
                "id",
                "status__code",
                "main_department_id",
                "involved_departments__department_id",
            )
            .distinct()
        )

        tmp: dict[int, set[int]] = {dept_id: set() for dept_id in dept_ids}
        for row in rows:
            app_id = row["id"]
            for dept_id in (
                row["main_department_id"],
                row["involved_departments__department_id"],
            ):
                if dept_id is not None and dept_id in dept_ids:
                    tmp[dept_id].add(app_id)

        return {str(dept_id): app_ids for dept_id, app_ids in tmp.items()}

    def get_rating_chart_data(
        self,
        queryset: QuerySet[ProjectApplication],
        filters: DashboardFilters,
    ) -> dict:
        """Данные для горизонтального stacked bar."""
        if filters.department_id is not None:
            return self._rating_by_departments(queryset, filters.department_id)
        if filters.institute_code:
            return self._rating_by_institute_departments(
                queryset, filters.institute_code
            )
        return self._rating_by_institutes(queryset)

    def _rating_by_institutes(self, queryset: QuerySet[ProjectApplication]) -> dict:
        """Рейтинг по институтам."""
        institutes = list(Institute.objects.filter(is_active=True).order_by("position"))
        dimension_map = self._build_institute_dimension_map(queryset, institutes)
        stats = self._aggregate_by_dimension(queryset, dimension_map)

        categories_data = []
        for inst in institutes:
            counts = stats.get(inst.code, {g: 0 for g in STATUS_GROUPS})
            total = sum(counts.values())
            categories_data.append(
                {
                    "key": inst.code,
                    "label": inst.code,
                    "total": total,
                    "counts": counts,
                }
            )

        categories_data.sort(key=lambda item: item["total"], reverse=True)
        return self._format_rating_chart(categories_data, dimension="institute")

    def _rating_by_institute_departments(
        self,
        queryset: QuerySet[ProjectApplication],
        institute_code: str,
    ) -> dict:
        """Рейтинг по дочерним подразделениям института."""
        institute = Institute.objects.select_related("department").get(
            code=institute_code
        )
        if institute.department_id is None:
            return self._format_rating_chart([], dimension="department")

        departments = list(
            Department.objects.filter(parent_id=institute.department_id).order_by(
                "name"
            )
        )
        return self._rating_by_departments_list(queryset, departments)

    def _rating_by_departments(
        self,
        queryset: QuerySet[ProjectApplication],
        department_id: int,
    ) -> dict:
        """Рейтинг по дочерним подразделениям выбранного подразделения."""
        departments = list(
            Department.objects.filter(parent_id=department_id).order_by("name")
        )
        if not departments:
            departments = self._leaf_departments_in_subtree(department_id)
        return self._rating_by_departments_list(queryset, departments)

    @staticmethod
    def _leaf_departments_in_subtree(department_id: int) -> list[Department]:
        """Листовые подразделения в поддереве, если прямых дочерних нет."""
        subtree_ids = get_department_subtree_ids(department_id)
        all_depts = list(Department.objects.filter(id__in=subtree_ids))
        parent_ids_in_subtree = {
            dept.parent_id for dept in all_depts if dept.parent_id in subtree_ids
        }
        leaf_ids = subtree_ids - parent_ids_in_subtree
        return [dept for dept in all_depts if dept.id in leaf_ids]

    def _rating_by_departments_list(
        self,
        queryset: QuerySet[ProjectApplication],
        departments: list[Department],
    ) -> dict:
        """Общая логика рейтинга по списку подразделений."""
        dimension_map = self._build_department_dimension_map(queryset, departments)
        stats = self._aggregate_by_dimension(queryset, dimension_map)

        categories_data = []
        for dept in departments:
            key = str(dept.id)
            counts = stats.get(key, {g: 0 for g in STATUS_GROUPS})
            total = sum(counts.values())
            label = dept.short_name or dept.name
            categories_data.append(
                {"key": key, "label": label, "total": total, "counts": counts}
            )

        categories_data.sort(key=lambda item: item["total"], reverse=True)
        return self._format_rating_chart(categories_data, dimension="department")

    @staticmethod
    def _format_rating_chart(categories_data: list[dict], dimension: str) -> dict:
        """Форматирует данные рейтинга для API."""
        from showcase.domain.application_dashboard import GROUP_COLORS, GROUP_LABELS

        categories = [item["label"] for item in categories_data]
        series = []
        for group in STATUS_GROUPS:
            series.append(
                {
                    "id": group,
                    "name": GROUP_LABELS[group],
                    "color": GROUP_COLORS[group],
                    "data": [item["counts"].get(group, 0) for item in categories_data],
                }
            )

        title = (
            "Рейтинг по подразделениям"
            if dimension == "department"
            else "Рейтинг по институтам"
        )
        subtitle = (
            "Stacked bar по статусам, сортировка по общему количеству. "
            "При выборе подразделения — рейтинг по подразделениям."
        )

        return {
            "id": "rating_chart",
            "title": title,
            "subtitle": subtitle,
            "type": "horizontal_stacked_bar",
            "dimension": dimension,
            "categories": categories,
            "series": series,
        }

    def get_status_distribution(self, queryset: QuerySet[ProjectApplication]) -> dict:
        """Доли заявок по группам статусов."""
        from showcase.domain.application_dashboard import GROUP_COLORS, GROUP_LABELS

        aggregates = queryset.aggregate(
            total=Count("id"),
            **{
                f"count_{group}": Count(
                    "id", filter=Q(status__code__in=STATUS_GROUPS[group])
                )
                for group in STATUS_GROUPS
            },
        )
        total = aggregates["total"]
        segments = []
        for group in STATUS_GROUPS:
            count = aggregates[f"count_{group}"]
            percent = round((count / total) * 100, 1) if total else 0.0
            segments.append(
                {
                    "group": group,
                    "label": GROUP_LABELS[group],
                    "count": count,
                    "percent": percent,
                    "color": GROUP_COLORS[group],
                }
            )

        return {
            "id": "status_distribution",
            "title": "Доли заявок по статусам",
            "subtitle": (
                "100% stacked bar — доля каждого статуса от общего числа заявок"
            ),
            "type": "percent_stacked_bar",
            "segments": segments,
        }

    def get_daily_dynamics(
        self,
        queryset: QuerySet[ProjectApplication],
        days: int,
    ) -> dict:
        """Динамика создания и решения заявок по дням."""
        today = timezone.localdate()
        date_from = today - timedelta(days=days - 1)
        date_to = today

        categories: list[str] = []
        current = date_from
        while current <= date_to:
            categories.append(current.isoformat())
            current += timedelta(days=1)

        app_ids = list(queryset.values_list("id", flat=True))

        created_by_date: dict[str, int] = defaultdict(int)
        if app_ids:
            created_rows = (
                queryset.filter(
                    creation_date__date__gte=date_from,
                    creation_date__date__lte=date_to,
                )
                .values("creation_date__date")
                .annotate(count=Count("id", distinct=True))
            )
            for row in created_rows:
                day = row["creation_date__date"]
                if day:
                    created_by_date[day.isoformat()] = row["count"]

        resolved_by_date: dict[str, int] = defaultdict(int)
        if app_ids:
            resolved_rows = (
                ProjectApplicationStatusLog.objects.filter(
                    application_id__in=app_ids,
                    action_type="status_change",
                    to_status__code__in=FINAL_RESOLUTION_STATUS_CODES,
                    changed_at__date__gte=date_from,
                    changed_at__date__lte=date_to,
                )
                .values("changed_at__date")
                .annotate(count=Count("application_id", distinct=True))
            )
            for row in resolved_rows:
                day = row["changed_at__date"]
                if day:
                    resolved_by_date[day.isoformat()] = row["count"]

        created_data = [created_by_date.get(day, 0) for day in categories]
        resolved_data = [resolved_by_date.get(day, 0) for day in categories]
        ma7_data = self._moving_average(created_data, window=7)

        return {
            "id": "daily_dynamics",
            "title": "Динамика заявок по дням",
            "subtitle": "Создано / Решено + скользящее среднее 7 дней",
            "type": "line",
            "date_from": date_from.isoformat(),
            "date_to": date_to.isoformat(),
            "categories": categories,
            "series": [
                {"id": "created", "name": "Создано", "data": created_data},
                {"id": "resolved", "name": "Решено", "data": resolved_data},
                {
                    "id": "created_ma7",
                    "name": "Скользящее среднее 7 дней",
                    "style": "dashed",
                    "data": ma7_data,
                },
            ],
        }

    @staticmethod
    def _moving_average(values: list[int], window: int) -> list[float]:
        """Скользящее среднее с заданным окном."""
        result: list[float] = []
        for index in range(len(values)):
            start = max(0, index - window + 1)
            chunk = values[start : index + 1]
            result.append(round(sum(chunk) / len(chunk), 1))
        return result

    def get_oldest_in_progress(
        self,
        queryset: QuerySet[ProjectApplication],
        limit: int = 10,
    ) -> dict:
        """Топ самых старых заявок в статусе «В работе»."""
        last_status_log = ProjectApplicationStatusLog.objects.filter(
            application_id=OuterRef("pk"),
            action_type="status_change",
            to_status_id=OuterRef("status_id"),
        ).order_by("-changed_at")

        in_progress_qs = (
            queryset.filter(status__code__in=STATUS_GROUPS["in_progress"])
            .select_related("main_department")
            .prefetch_related("target_institutes")
            .annotate(
                last_status_change_at=Subquery(last_status_log.values("changed_at")[:1])
            )
        )

        today = timezone.localdate()
        items: list[dict] = []

        for app in in_progress_qs:
            reference = app.last_status_change_at or app.creation_date
            if isinstance(reference, datetime):
                reference_date = timezone.localtime(reference).date()
            else:
                reference_date = reference
            days = (today - reference_date).days

            institute_code = ""
            targets = list(app.target_institutes.all())
            if targets:
                institute_code = targets[0].code
            elif app.main_department:
                institute_code = (
                    app.main_department.short_name or app.main_department.name
                )

            items.append(
                {
                    "application_number": app.print_number or f"#{app.pk}",
                    "days": days,
                    "institute_code": institute_code,
                }
            )

        items.sort(key=lambda item: item["days"], reverse=True)
        return {
            "id": "oldest_in_progress",
            "title": "Топ-10 самых старых в работе",
            "subtitle": "Заявки с наибольшим временем в статусе «В работе»",
            "type": "table",
            "items": items[:limit],
        }

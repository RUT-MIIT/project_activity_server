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
    INSTITUTE_LEVEL_CATEGORY_KEY,
    INSTITUTE_LEVEL_CATEGORY_LABEL,
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
        self._department_institute_code_map: dict[int, str] | None = None

    def _get_department_institute_code_map(self) -> dict[int, str]:
        """Возвращает кэшированную карту department_id -> institute.code."""
        if self._department_institute_code_map is None:
            self._department_institute_code_map = (
                self._build_department_institute_code_map()
            )
        return self._department_institute_code_map

    @staticmethod
    def _build_department_institute_code_map() -> dict[int, str]:
        """Строит карту department_id -> institute.code без N+1."""
        parent_by_id: dict[int, int | None] = dict(
            Department.objects.values_list("id", "parent_id")
        )
        children_by_parent: dict[int, list[int]] = defaultdict(list)
        for dept_id, parent_id in parent_by_id.items():
            if parent_id is not None:
                children_by_parent[parent_id].append(dept_id)

        def subtree_ids(root_id: int) -> set[int]:
            result = {root_id}
            queue = [root_id]
            while queue:
                current = queue.pop()
                for child_id in children_by_parent.get(current, []):
                    if child_id not in result:
                        result.add(child_id)
                        queue.append(child_id)
            return result

        def root_id(dept_id: int) -> int:
            current = dept_id
            while parent_by_id.get(current) is not None:
                current = parent_by_id[current]
            return current

        institutes = (
            Institute.objects.filter(is_active=True, department_id__isnull=False)
            .only("code", "department_id")
            .order_by("position")
        )

        code_by_dept: dict[int, str] = {}
        for institute in institutes:
            institute_root_id = root_id(institute.department_id)
            for dept_id in subtree_ids(institute_root_id):
                if dept_id not in code_by_dept:
                    code_by_dept[dept_id] = institute.code

        return code_by_dept

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

    def _aggregate_external_share(
        self,
        queryset: QuerySet[ProjectApplication],
        dimension_map: dict[str, set[int]],
    ) -> dict[str, dict[str, int | float]]:
        """Считает долю внешних заявок по каждому измерению."""
        result: dict[str, dict[str, int | float]] = {
            key: {"external_count": 0, "percent": 0.0} for key in dimension_map
        }

        all_app_ids: set[int] = set()
        for app_ids in dimension_map.values():
            all_app_ids.update(app_ids)
        if not all_app_ids:
            return result

        external_by_app = dict(
            queryset.filter(id__in=all_app_ids).values_list("id", "is_external")
        )

        for key, app_ids in dimension_map.items():
            total = len(app_ids)
            external_count = sum(1 for app_id in app_ids if external_by_app.get(app_id))
            percent = round((external_count / total) * 100, 1) if total else 0.0
            result[key] = {"external_count": external_count, "percent": percent}

        return result

    @staticmethod
    def _external_share_color(percent: float) -> str:
        """Цвет столбца по порогам доли внешних заявок."""
        if percent < 30:
            return "green"
        if percent <= 40:
            return "orange"
        return "red"

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

    def _build_institute_level_dimension_map(
        self,
        queryset: QuerySet[ProjectApplication],
        anchor_department_id: int,
        child_department_ids: set[int],
    ) -> dict[str, set[int]]:
        """Заявки, привязанные к anchor, но не к дочерним подразделениям рейтинга."""
        anchor_app_ids = set(
            queryset.filter(
                Q(main_department_id=anchor_department_id)
                | Q(involved_departments__department_id=anchor_department_id)
            )
            .values_list("id", flat=True)
            .distinct()
        )
        if not anchor_app_ids:
            return {}

        if child_department_ids:
            child_app_ids = set(
                queryset.filter(
                    Q(main_department_id__in=child_department_ids)
                    | Q(involved_departments__department_id__in=child_department_ids)
                )
                .values_list("id", flat=True)
                .distinct()
            )
            institute_level_ids = anchor_app_ids - child_app_ids
        else:
            institute_level_ids = anchor_app_ids

        if not institute_level_ids:
            return {}
        return {INSTITUTE_LEVEL_CATEGORY_KEY: institute_level_ids}

    @staticmethod
    def _institute_level_category_dict(
        anchor_department_id: int,
        institute_code: str | None = None,
    ) -> dict:
        """Категория «От института» для рейтинга по подразделениям."""
        return {
            "id": anchor_department_id,
            "name": INSTITUTE_LEVEL_CATEGORY_LABEL,
            "short_name": INSTITUTE_LEVEL_CATEGORY_LABEL,
            "parent_id": anchor_department_id,
            "code": institute_code,
        }

    def get_rating_chart_data(
        self,
        queryset: QuerySet[ProjectApplication],
        filters: DashboardFilters,
    ) -> dict:
        """Данные для горизонтального stacked bar."""
        categories_data, dimension = self._get_rating_categories_data(queryset, filters)
        return self._format_rating_chart(categories_data, dimension=dimension)

    def get_external_share_chart_data(
        self,
        queryset: QuerySet[ProjectApplication],
        filters: DashboardFilters,
    ) -> dict:
        """Доля внешних заявок по подразделениям или институтам."""
        categories_data, dimension = self._get_rating_categories_data(queryset, filters)
        sorted_data = sorted(
            categories_data,
            key=lambda item: item["external_percent"],
            reverse=True,
        )
        return self._format_external_share_chart(sorted_data, dimension=dimension)

    def _get_rating_categories_data(
        self,
        queryset: QuerySet[ProjectApplication],
        filters: DashboardFilters,
    ) -> tuple[list[dict], str]:
        """Собирает данные категорий для рейтинга и доли внешних заявок."""
        if filters.department_id is not None:
            return (
                self._categories_data_by_departments(queryset, filters.department_id),
                "department",
            )
        if filters.institute_code:
            return (
                self._categories_data_by_institute_departments(
                    queryset, filters.institute_code
                ),
                "department",
            )
        return self._categories_data_by_institutes(queryset), "institute"

    def _categories_data_by_institutes(
        self, queryset: QuerySet[ProjectApplication]
    ) -> list[dict]:
        """Данные категорий рейтинга по институтам."""
        institutes = list(
            Institute.objects.filter(is_active=True)
            .select_related("department")
            .order_by("position")
        )
        dimension_map = self._build_institute_dimension_map(queryset, institutes)
        stats = self._aggregate_by_dimension(queryset, dimension_map)
        external_stats = self._aggregate_external_share(queryset, dimension_map)

        categories_data = []
        for inst in institutes:
            counts = stats.get(inst.code, {g: 0 for g in STATUS_GROUPS})
            total = sum(counts.values())
            external = external_stats[inst.code]
            categories_data.append(
                {
                    "key": inst.code,
                    "category": self._department_to_dict(
                        inst.department,
                        institute_code=inst.code,
                    ),
                    "total": total,
                    "counts": counts,
                    "external_count": external["external_count"],
                    "external_percent": external["percent"],
                }
            )

        categories_data.sort(key=lambda item: item["total"], reverse=True)
        return categories_data

    def _categories_data_by_institute_departments(
        self,
        queryset: QuerySet[ProjectApplication],
        institute_code: str,
    ) -> list[dict]:
        """Данные категорий рейтинга по дочерним подразделениям института."""
        institute = Institute.objects.select_related("department").get(
            code=institute_code
        )
        if institute.department_id is None:
            return []

        departments = list(
            Department.objects.filter(parent_id=institute.department_id).order_by(
                "name"
            )
        )
        return self._categories_data_by_departments_list(
            queryset,
            departments,
            anchor_department_id=institute.department_id,
        )

    def _categories_data_by_departments(
        self,
        queryset: QuerySet[ProjectApplication],
        department_id: int,
    ) -> list[dict]:
        """Данные категорий рейтинга по дочерним подразделениям."""
        departments = list(
            Department.objects.filter(parent_id=department_id).order_by("name")
        )
        if not departments:
            departments = self._leaf_departments_in_subtree(department_id)
        return self._categories_data_by_departments_list(
            queryset,
            departments,
            anchor_department_id=department_id,
        )

    def _categories_data_by_departments_list(
        self,
        queryset: QuerySet[ProjectApplication],
        departments: list[Department],
        anchor_department_id: int | None = None,
    ) -> list[dict]:
        """Общая логика сбора данных по списку подразделений."""
        dimension_map = self._build_department_dimension_map(queryset, departments)
        if anchor_department_id is not None:
            child_ids = {dept.id for dept in departments}
            institute_level_map = self._build_institute_level_dimension_map(
                queryset,
                anchor_department_id,
                child_ids,
            )
            dimension_map.update(institute_level_map)

        stats = self._aggregate_by_dimension(queryset, dimension_map)
        external_stats = self._aggregate_external_share(queryset, dimension_map)
        institute_codes = self._get_department_institute_code_map()

        categories_data = []
        for dept in departments:
            key = str(dept.id)
            counts = stats.get(key, {g: 0 for g in STATUS_GROUPS})
            total = sum(counts.values())
            external = external_stats[key]
            categories_data.append(
                {
                    "key": key,
                    "category": self._department_to_dict(
                        dept,
                        institute_code=institute_codes.get(dept.id),
                    ),
                    "total": total,
                    "counts": counts,
                    "external_count": external["external_count"],
                    "external_percent": external["percent"],
                }
            )

        if INSTITUTE_LEVEL_CATEGORY_KEY in dimension_map:
            key = INSTITUTE_LEVEL_CATEGORY_KEY
            counts = stats.get(key, {g: 0 for g in STATUS_GROUPS})
            total = sum(counts.values())
            if total > 0:
                external = external_stats[key]
                anchor_code = (
                    institute_codes.get(anchor_department_id)
                    if anchor_department_id is not None
                    else None
                )
                categories_data.append(
                    {
                        "key": key,
                        "category": self._institute_level_category_dict(
                            anchor_department_id,
                            institute_code=anchor_code,
                        ),
                        "total": total,
                        "counts": counts,
                        "external_count": external["external_count"],
                        "external_percent": external["percent"],
                    }
                )

        categories_data.sort(key=lambda item: item["total"], reverse=True)
        return categories_data

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

    @staticmethod
    def _format_rating_chart(categories_data: list[dict], dimension: str) -> dict:
        """Форматирует данные рейтинга для API."""
        from showcase.domain.application_dashboard import (
            RATING_CHART_SERIES,
            RATING_CHART_SERIES_COLORS,
            RATING_CHART_SERIES_LABELS,
        )

        categories = [item["category"] for item in categories_data]
        series = []
        for group in RATING_CHART_SERIES:
            if group == "in_work":
                data = [
                    item["counts"].get("pending", 0)
                    + item["counts"].get("in_progress", 0)
                    for item in categories_data
                ]
            else:
                data = [item["counts"].get(group, 0) for item in categories_data]
            series.append(
                {
                    "id": group,
                    "name": RATING_CHART_SERIES_LABELS[group],
                    "color": RATING_CHART_SERIES_COLORS[group],
                    "data": data,
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

    @staticmethod
    def _format_external_share_chart(
        categories_data: list[dict], dimension: str
    ) -> dict:
        """Форматирует данные доли внешних заявок для API."""
        categories = [item["category"] for item in categories_data]
        items = [
            {
                "category": item["category"],
                "total": item["total"],
                "external_count": item["external_count"],
                "percent": item["external_percent"],
                "color": ApplicationDashboardRepository._external_share_color(
                    item["external_percent"]
                ),
            }
            for item in categories_data
        ]

        if dimension == "department":
            title = "Доля внешних по подразделениям"
            subtitle = (
                "% внешних заявок от общего числа по каждому подразделению — "
                "для сравнимости"
            )
        else:
            title = "Доля внешних по институтам"
            subtitle = (
                "% внешних заявок от общего числа по каждому институту — "
                "для сравнимости"
            )

        return {
            "id": "external_share_chart",
            "title": title,
            "subtitle": subtitle,
            "type": "vertical_bar",
            "dimension": dimension,
            "categories": categories,
            "items": items,
            "series": [
                {
                    "id": "external_share",
                    "name": "Доля внешних",
                    "unit": "%",
                    "data": [item["external_percent"] for item in categories_data],
                    "colors": [
                        ApplicationDashboardRepository._external_share_color(
                            item["external_percent"]
                        )
                        for item in categories_data
                    ],
                }
            ],
        }

    def get_status_distribution(self, queryset: QuerySet[ProjectApplication]) -> dict:
        """Доли заявок по группам статусов (согласовано / в работе / отклонено)."""
        from showcase.domain.application_dashboard import (
            RATING_CHART_SERIES,
            RATING_CHART_SERIES_COLORS,
            RATING_CHART_SERIES_LABELS,
        )

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
        for group in RATING_CHART_SERIES:
            if group == "in_work":
                count = aggregates["count_pending"] + aggregates["count_in_progress"]
            else:
                count = aggregates[f"count_{group}"]
            percent = round((count / total) * 100, 1) if total else 0.0
            segments.append(
                {
                    "group": group,
                    "label": RATING_CHART_SERIES_LABELS[group],
                    "count": count,
                    "percent": percent,
                    "color": RATING_CHART_SERIES_COLORS[group],
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

    def get_application_type_distribution(
        self, queryset: QuerySet[ProjectApplication]
    ) -> dict:
        """Доли внутренних/внешних заявок."""
        aggregates = queryset.aggregate(
            total=Count("id"),
            external_count=Count("id", filter=Q(is_external=True)),
            internal_count=Count("id", filter=Q(is_external=False)),
        )
        total = aggregates["total"]
        external_count = aggregates["external_count"]
        internal_count = aggregates["internal_count"]

        external_pct = round((external_count / total) * 100, 1) if total else 0.0
        internal_pct = round((internal_count / total) * 100, 1) if total else 0.0

        return {
            "id": "application_type_distribution",
            "title": "Доли заявок по типу",
            "subtitle": "Внутренние vs внешние",
            "type": "pie",
            "segments": [
                {
                    "group": "internal",
                    "label": "Внутренние",
                    "count": internal_count,
                    "percent": internal_pct,
                    "color": "blue",
                },
                {
                    "group": "external",
                    "label": "Внешние",
                    "count": external_count,
                    "percent": external_pct,
                    "color": "teal",
                },
            ],
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
            .prefetch_related("target_institutes__department")
            .annotate(
                last_status_change_at=Subquery(last_status_log.values("changed_at")[:1])
            )
        )

        today = timezone.localdate()
        items: list[dict] = []
        institute_codes = self._get_department_institute_code_map()

        for app in in_progress_qs:
            reference = app.last_status_change_at or app.creation_date
            if isinstance(reference, datetime):
                reference_date = timezone.localtime(reference).date()
            else:
                reference_date = reference
            days = (today - reference_date).days

            department_obj = None
            targets = list(app.target_institutes.all())
            if targets and getattr(targets[0], "department", None) is not None:
                target_department = targets[0].department
                department_obj = self._department_to_dict(
                    target_department,
                    institute_code=institute_codes.get(target_department.id),
                )
            elif app.main_department:
                department_obj = self._department_to_dict(
                    app.main_department,
                    institute_code=institute_codes.get(app.main_department_id),
                )

            items.append(
                {
                    "application_number": app.print_number or f"#{app.pk}",
                    "days": days,
                    "institute_code": department_obj,
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

    @staticmethod
    def _department_to_dict(
        department: Department | None,
        institute_code: str | None = None,
    ) -> dict | None:
        """Преобразует подразделение в JSON-совместимый объект для API."""
        if department is None:
            return None
        return {
            "id": department.id,
            "name": department.name,
            "short_name": department.short_name,
            "parent_id": department.parent_id,
            "code": institute_code,
        }

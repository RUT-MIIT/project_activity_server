"""Репозиторий для проектных треков."""

from __future__ import annotations

from itertools import product

from django.db.models import Count, Q, QuerySet

from showcase.models import Institute, ProjectApplication, ProjectTrack
from teams.domain.institute_access import get_department_ids_for_institute_codes
from teams.models import StudyGroup


class ProjectTrackRepository:
    """Доступ к данным проектных треков."""

    @staticmethod
    def _involved_department_q(institute_codes: list[str], prefix: str = "") -> Q:
        """Q-фильтр: заявка относится к институту по причастным подразделениям."""
        department_ids = get_department_ids_for_institute_codes(institute_codes)
        if not department_ids:
            return Q(pk__in=[])

        return Q(
            **{
                f"{prefix}involved_departments__department_id__in": department_ids,
            }
        )

    @classmethod
    def _application_institute_access_q(
        cls, institute_codes: list[str], prefix: str = ""
    ) -> Q:
        """Q-фильтр: заявка доступна институту по involved_departments/target_institutes."""
        if not institute_codes:
            return Q(pk__in=[])

        involved = cls._involved_department_q(institute_codes, prefix=prefix)
        targets = Q(**{f"{prefix}target_institutes__code__in": institute_codes})
        return involved | targets

    @classmethod
    def _application_matches_institutes_q(cls, institute_codes: list[str]) -> Q:
        """Q-фильтр для queryset ProjectTrack."""
        return cls._application_institute_access_q(
            institute_codes, prefix="project_application__"
        )

    def list_by_institute_and_semester(
        self,
        institute_code: str,
        semester_id: int,
        accessible_institute_codes: list[str] | None,
    ) -> QuerySet[ProjectTrack]:
        """Список треков по институту и семестру."""
        queryset = (
            ProjectTrack.objects.filter(
                semester_id=semester_id,
                study_group__institute_id=institute_code,
                project_application__status__code="approved",
            )
            .filter(self._application_matches_institutes_q([institute_code]))
            .select_related(
                "semester",
                "study_group",
                "project_application",
            )
            .distinct()
            .order_by("study_group__name", "project_application__title")
        )

        if accessible_institute_codes is not None:
            queryset = queryset.filter(
                study_group__institute_id__in=accessible_institute_codes,
            )

        return queryset

    def get_existing_pairs(
        self,
        semester_id: int,
        group_ids: list[int],
        application_ids: list[int],
    ) -> set[tuple[int, int]]:
        """Возвращает уже существующие пары (group_id, application_id)."""
        rows = ProjectTrack.objects.filter(
            semester_id=semester_id,
            study_group_id__in=group_ids,
            project_application_id__in=application_ids,
        ).values_list("study_group_id", "project_application_id")
        return set(rows)

    def bulk_create_tracks(
        self,
        semester_id: int,
        group_ids: list[int],
        application_ids: list[int],
    ) -> None:
        """Создаёт треки для декартова произведения групп и заявок."""
        tracks = [
            ProjectTrack(
                semester_id=semester_id,
                study_group_id=group_id,
                project_application_id=application_id,
            )
            for group_id, application_id in product(group_ids, application_ids)
        ]
        if tracks:
            ProjectTrack.objects.bulk_create(tracks, ignore_conflicts=True)

    def get_groups_by_ids(self, group_ids: list[int]) -> QuerySet[StudyGroup]:
        """Возвращает группы по списку id."""
        return StudyGroup.objects.filter(pk__in=group_ids)

    def get_applications_by_ids(
        self, application_ids: list[int]
    ) -> QuerySet[ProjectApplication]:
        """Возвращает заявки по списку id."""
        return (
            ProjectApplication.objects.filter(pk__in=application_ids)
            .select_related("status", "semester")
            .prefetch_related("involved_departments", "target_institutes")
        )

    def get_by_keys(
        self,
        semester_id: int,
        group_id: int,
        project_application_id: int,
    ) -> ProjectTrack | None:
        """Возвращает трек по семестру, группе и заявке или None."""
        try:
            return (
                ProjectTrack.objects.select_related(
                    "semester",
                    "study_group",
                    "project_application",
                )
                .prefetch_related("project_application__involved_departments")
                .get(
                    semester_id=semester_id,
                    study_group_id=group_id,
                    project_application_id=project_application_id,
                )
            )
        except ProjectTrack.DoesNotExist:
            return None

    def get_by_id(self, track_id: int) -> ProjectTrack | None:
        """Возвращает трек по id или None."""
        try:
            return (
                ProjectTrack.objects.select_related(
                    "semester",
                    "study_group",
                    "project_application",
                )
                .prefetch_related("project_application__involved_departments")
                .get(pk=track_id)
            )
        except ProjectTrack.DoesNotExist:
            return None

    def delete(self, track: ProjectTrack) -> None:
        """Удаляет трек."""
        track.delete()

    def list_groups_with_counts(
        self,
        institute_code: str,
        semester_id: int,
        accessible_institute_codes: list[str] | None,
    ) -> QuerySet[StudyGroup]:
        """Список активных групп института со счётчиком назначенных проектов."""
        queryset = (
            StudyGroup.objects.filter(
                institute_id=institute_code,
                is_end=False,
            )
            .annotate(
                assigned_projects_count=Count(
                    "project_tracks",
                    filter=Q(project_tracks__semester_id=semester_id),
                )
            )
            .select_related("direction")
            .order_by("name")
        )

        if accessible_institute_codes is not None:
            queryset = queryset.filter(
                institute_id__in=accessible_institute_codes,
            )

        return queryset

    def list_projects_with_counts(
        self,
        institute_code: str,
        semester_id: int,
        accessible_institute_codes: list[str] | None,
    ) -> QuerySet[ProjectApplication]:
        """Список одобренных проектов семестра со счётчиком назначенных групп."""
        queryset = (
            ProjectApplication.objects.filter(
                semester_id=semester_id,
                status__code="approved",
            )
            .filter(self._application_institute_access_q([institute_code]))
            .annotate(
                assigned_groups_count=Count(
                    "project_tracks",
                    distinct=True,
                    filter=Q(
                        project_tracks__semester_id=semester_id,
                        project_tracks__study_group__institute_id=institute_code,
                        project_tracks__study_group__is_end=False,
                    ),
                )
            )
            .distinct()
            .order_by("title")
        )

        # Параметр accessible_institute_codes здесь не влияет на результат:
        # доступ валидируется на уровне service по institute_code.
        _ = accessible_institute_codes
        return queryset

    def get_group_by_id(self, group_id: int) -> StudyGroup | None:
        """Возвращает группу по id или None."""
        try:
            return StudyGroup.objects.select_related("direction", "institute").get(
                pk=group_id
            )
        except StudyGroup.DoesNotExist:
            return None

    def get_group_assigned_applications(
        self,
        group_id: int,
        semester_id: int,
        institute_code: str,
    ) -> QuerySet[ProjectApplication]:
        """Одобренные заявки, назначенные группе в семестре."""
        return (
            ProjectApplication.objects.filter(
                project_tracks__study_group_id=group_id,
                project_tracks__semester_id=semester_id,
                status__code="approved",
            )
            .filter(self._application_institute_access_q([institute_code]))
            .distinct()
            .order_by("title")
        )

    def get_application_by_id(
        self, project_id: int, *, institute_code: str | None = None
    ) -> ProjectApplication | None:
        """Возвращает проектную заявку по id или None.

        Если передан institute_code — дополнительно фильтрует по доступности заявки институту.
        """
        try:
            queryset = ProjectApplication.objects.select_related(
                "status", "semester"
            ).prefetch_related("involved_departments", "target_institutes")
            if institute_code is not None:
                queryset = queryset.filter(
                    self._application_institute_access_q([institute_code])
                ).distinct()
            return queryset.get(pk=project_id)
        except ProjectApplication.DoesNotExist:
            return None

    def get_project_assigned_groups(
        self,
        project_id: int,
        semester_id: int,
        institute_code: str,
    ) -> QuerySet[StudyGroup]:
        """Активные группы института, назначенные на проект в семестре."""
        return (
            StudyGroup.objects.filter(
                institute_id=institute_code,
                is_end=False,
                project_tracks__project_application_id=project_id,
                project_tracks__semester_id=semester_id,
            )
            .select_related("direction")
            .distinct()
            .order_by("name")
        )

    def get_statistics(
        self,
        institute_code: str,
        semester_id: int,
        accessible_institute_codes: list[str] | None,
    ) -> dict[str, int | float]:
        """Агрегированная статистика распределения проектов по группам."""
        groups_qs = StudyGroup.objects.filter(
            institute_id=institute_code,
            is_end=False,
        )
        if accessible_institute_codes is not None:
            groups_qs = groups_qs.filter(
                institute_id__in=accessible_institute_codes,
            )

        total_groups = groups_qs.count()

        tracks_qs = ProjectTrack.objects.filter(
            semester_id=semester_id,
            study_group__institute_id=institute_code,
            study_group__is_end=False,
            project_application__status__code="approved",
        ).filter(self._application_matches_institutes_q([institute_code]))

        if accessible_institute_codes is not None:
            tracks_qs = tracks_qs.filter(
                study_group__institute_id__in=accessible_institute_codes,
            )

        total_tracks = tracks_qs.count()
        distributed_projects = (
            tracks_qs.values("project_application_id").distinct().count()
        )

        groups_with_projects = tracks_qs.values("study_group_id").distinct().count()
        groups_without_projects = total_groups - groups_with_projects

        total_projects = (
            ProjectApplication.objects.filter(
                status__code="approved",
                semester_id=semester_id,
            )
            .filter(self._application_institute_access_q([institute_code]))
            .distinct()
            .count()
        )

        average = round(total_tracks / total_groups, 1) if total_groups > 0 else 0.0

        return {
            "total_projects": total_projects,
            "distributed_projects": distributed_projects,
            "average_projects_per_group": average,
            "groups_without_projects": groups_without_projects,
        }

    def get_statistics_overall(self, semester_id: int) -> dict[str, int | float]:
        """Агрегированная статистика по всем активным институтам."""
        groups_qs = StudyGroup.objects.filter(
            is_end=False,
            institute__is_active=True,
        )
        total_groups = groups_qs.count()

        tracks_qs = ProjectTrack.objects.filter(
            semester_id=semester_id,
            study_group__is_end=False,
            study_group__institute__is_active=True,
            project_application__status__code="approved",
        )

        total_tracks = tracks_qs.count()
        distributed_projects = (
            tracks_qs.values("project_application_id").distinct().count()
        )

        groups_with_projects = tracks_qs.values("study_group_id").distinct().count()
        groups_without_projects = total_groups - groups_with_projects

        total_projects = ProjectApplication.objects.filter(
            status__code="approved",
            semester_id=semester_id,
        ).count()

        average = round(total_tracks / total_groups, 1) if total_groups > 0 else 0.0

        return {
            "total_projects": total_projects,
            "distributed_projects": distributed_projects,
            "average_projects_per_group": average,
            "groups_without_projects": groups_without_projects,
        }

    def list_statistics_by_institutes(
        self, semester_id: int
    ) -> list[dict[str, int | float | str]]:
        """Статистика по каждому активному институту."""
        institutes = Institute.objects.filter(is_active=True).order_by("position")
        result: list[dict[str, int | float | str]] = []
        for institute in institutes:
            stats = self.get_statistics(
                institute_code=institute.code,
                semester_id=semester_id,
                accessible_institute_codes=None,
            )
            result.append(
                {
                    "institute_code": institute.code,
                    "institute_name": institute.name,
                    **stats,
                }
            )
        return result

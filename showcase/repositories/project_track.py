"""Репозиторий для проектных треков."""

from __future__ import annotations

from django.db.models import Count, Exists, OuterRef, Prefetch, Q, QuerySet

from showcase.models import (
    Institute,
    ProjectApplication,
    ProjectTrack,
    ProjectTrackApplication,
    ProjectTrackGroup,
)
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
        """Q-фильтр: заявка доступна институту по involved/target institutes."""
        if not institute_codes:
            return Q(pk__in=[])

        involved = cls._involved_department_q(institute_codes, prefix=prefix)
        targets = Q(**{f"{prefix}target_institutes__code__in": institute_codes})
        return involved | targets

    def _track_detail_queryset(self) -> QuerySet[ProjectTrack]:
        """Queryset трека с prefetch связей."""
        return ProjectTrack.objects.select_related(
            "semester",
            "department",
            "author",
        ).prefetch_related(
            Prefetch(
                "group_links",
                queryset=ProjectTrackGroup.objects.select_related(
                    "study_group"
                ).order_by("study_group__name"),
            ),
            Prefetch(
                "application_links",
                queryset=ProjectTrackApplication.objects.select_related(
                    "project_application"
                ).order_by("project_application__title"),
            ),
        )

    def list_tracks(
        self,
        semester_id: int,
        *,
        department_id: int | None = None,
        institute_code: str | None = None,
        accessible_department_ids: list[int] | None = None,
    ) -> QuerySet[ProjectTrack]:
        """Список треков по фильтрам."""
        queryset = self._track_detail_queryset().filter(semester_id=semester_id)

        if department_id is not None:
            queryset = queryset.filter(department_id=department_id)

        if institute_code is not None:
            department_ids = get_department_ids_for_institute_codes([institute_code])
            if not department_ids:
                return ProjectTrack.objects.none()
            queryset = queryset.filter(department_id__in=department_ids)

        if accessible_department_ids is not None:
            queryset = queryset.filter(department_id__in=accessible_department_ids)

        return queryset.order_by("name")

    def get_by_id(self, track_id: int) -> ProjectTrack | None:
        """Возвращает трек по id или None."""
        try:
            return self._track_detail_queryset().get(pk=track_id)
        except ProjectTrack.DoesNotExist:
            return None

    def create(
        self,
        *,
        name: str,
        description: str,
        department_id: int,
        semester_id: int,
        author_id: int,
        max_teams: int,
    ) -> ProjectTrack:
        """Создаёт проектный трек."""
        return ProjectTrack.objects.create(
            name=name,
            description=description,
            department_id=department_id,
            semester_id=semester_id,
            author_id=author_id,
            max_teams=max_teams,
        )

    def update(self, track: ProjectTrack, **fields) -> ProjectTrack:
        """Обновляет поля трека."""
        for field, value in fields.items():
            setattr(track, field, value)
        track.save(update_fields=list(fields.keys()))
        return track

    def delete(self, track: ProjectTrack) -> None:
        """Удаляет трек."""
        track.delete()

    def get_existing_group_ids(self, track_id: int, group_ids: list[int]) -> set[int]:
        """Возвращает id групп, уже привязанных к треку."""
        rows = ProjectTrackGroup.objects.filter(
            project_track_id=track_id,
            study_group_id__in=group_ids,
        ).values_list("study_group_id", flat=True)
        return set(rows)

    def add_groups(self, track_id: int, group_ids: list[int]) -> int:
        """Добавляет группы в трек; возвращает число созданных связей."""
        links = [
            ProjectTrackGroup(project_track_id=track_id, study_group_id=group_id)
            for group_id in group_ids
        ]
        if not links:
            return 0
        created = ProjectTrackGroup.objects.bulk_create(links, ignore_conflicts=True)
        return len(created)

    def remove_group(self, track_id: int, group_id: int) -> bool:
        """Удаляет группу из трека; True если связь была."""
        deleted, _ = ProjectTrackGroup.objects.filter(
            project_track_id=track_id,
            study_group_id=group_id,
        ).delete()
        return deleted > 0

    def get_existing_application_ids(
        self, track_id: int, application_ids: list[int]
    ) -> set[int]:
        """Возвращает id заявок, уже привязанных к треку."""
        rows = ProjectTrackApplication.objects.filter(
            project_track_id=track_id,
            project_application_id__in=application_ids,
        ).values_list("project_application_id", flat=True)
        return set(rows)

    def add_applications(self, track_id: int, application_ids: list[int]) -> int:
        """Добавляет заявки в трек; возвращает число созданных связей."""
        links = [
            ProjectTrackApplication(
                project_track_id=track_id,
                project_application_id=application_id,
            )
            for application_id in application_ids
        ]
        if not links:
            return 0
        created = ProjectTrackApplication.objects.bulk_create(
            links, ignore_conflicts=True
        )
        return len(created)

    def remove_application(self, track_id: int, application_id: int) -> bool:
        """Удаляет заявку из трека; True если связь была."""
        deleted, _ = ProjectTrackApplication.objects.filter(
            project_track_id=track_id,
            project_application_id=application_id,
        ).delete()
        return deleted > 0

    def count_groups(self, track_id: int) -> int:
        """Количество групп в треке."""
        return ProjectTrackGroup.objects.filter(project_track_id=track_id).count()

    def get_groups_by_ids(self, group_ids: list[int]) -> QuerySet[StudyGroup]:
        """Возвращает группы по списку id."""
        return StudyGroup.objects.filter(pk__in=group_ids).select_related(
            "direction", "institute"
        )

    def get_applications_by_ids(
        self, application_ids: list[int]
    ) -> QuerySet[ProjectApplication]:
        """Возвращает заявки по списку id."""
        return (
            ProjectApplication.objects.filter(pk__in=application_ids)
            .select_related("status", "semester")
            .prefetch_related("involved_departments", "target_institutes")
        )

    def list_groups_with_counts(
        self,
        institute_code: str,
        semester_id: int,
        accessible_institute_codes: list[str] | None,
    ) -> QuerySet[StudyGroup]:
        """Список активных групп института со счётчиком назначенных проектов."""
        shared_track_apps = ProjectTrackApplication.objects.filter(
            project_track__semester_id=semester_id,
            project_track__group_links__study_group_id=OuterRef("pk"),
        )

        approved_app_filter = Q(
            track_group_links__project_track__semester_id=semester_id,
            track_group_links__project_track__application_links__project_application__status__code="approved",  # noqa: E501
        )

        queryset = (
            StudyGroup.objects.filter(
                institute_id=institute_code,
                is_end=False,
            )
            .annotate(
                assigned_projects_count=Count(
                    (
                        "track_group_links__project_track__"
                        "application_links__project_application"
                    ),
                    distinct=True,
                    filter=approved_app_filter & Exists(shared_track_apps),
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
        shared_track_groups = ProjectTrackGroup.objects.filter(
            project_track__semester_id=semester_id,
            project_track__application_links__project_application_id=OuterRef("pk"),
        )

        track_group_filter = Q(
            track_application_links__project_track__semester_id=semester_id,
            track_application_links__project_track__group_links__study_group__institute_id=institute_code,  # noqa: E501
            track_application_links__project_track__group_links__study_group__is_end=False,  # noqa: E501
        )

        queryset = (
            ProjectApplication.objects.filter(
                semester_id=semester_id,
                status__code="approved",
            )
            .filter(self._application_institute_access_q([institute_code]))
            .annotate(
                assigned_groups_count=Count(
                    (
                        "track_application_links__project_track__"
                        "group_links__study_group"
                    ),
                    distinct=True,
                    filter=track_group_filter & Exists(shared_track_groups),
                )
            )
            .distinct()
            .order_by("title")
        )

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
        """Одобренные заявки, назначенные группе через общие треки в семестре."""
        track_ids = ProjectTrackGroup.objects.filter(
            study_group_id=group_id,
            project_track__semester_id=semester_id,
            project_track__application_links__isnull=False,
        ).values_list("project_track_id", flat=True)

        return (
            ProjectApplication.objects.filter(
                track_application_links__project_track_id__in=track_ids,
                track_application_links__project_track__group_links__study_group_id=group_id,  # noqa: E501
                status__code="approved",
            )
            .filter(self._application_institute_access_q([institute_code]))
            .distinct()
            .order_by("title")
        )

    def get_application_by_id(
        self, project_id: int, *, institute_code: str | None = None
    ) -> ProjectApplication | None:
        """Возвращает проектную заявку по id или None."""
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
        """Активные группы института, назначенные на проект через общие треки."""
        track_ids = ProjectTrackApplication.objects.filter(
            project_application_id=project_id,
            project_track__semester_id=semester_id,
            project_track__group_links__isnull=False,
        ).values_list("project_track_id", flat=True)

        return (
            StudyGroup.objects.filter(
                institute_id=institute_code,
                is_end=False,
                track_group_links__project_track_id__in=track_ids,
                track_group_links__project_track__application_links__project_application_id=project_id,  # noqa: E501
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

        groups_with_projects = (
            StudyGroup.objects.filter(
                institute_id=institute_code,
                is_end=False,
                track_group_links__project_track__semester_id=semester_id,
                track_group_links__project_track__application_links__isnull=False,
            )
            .distinct()
            .count()
        )
        groups_without_projects = total_groups - groups_with_projects

        distributed_filter = Q(
            track_application_links__project_track__semester_id=semester_id,
            track_application_links__project_track__group_links__study_group__institute_id=institute_code,  # noqa: E501
            track_application_links__project_track__group_links__study_group__is_end=False,  # noqa: E501
        )

        distributed_projects = (
            ProjectApplication.objects.filter(
                status__code="approved",
                semester_id=semester_id,
            )
            .filter(distributed_filter)
            .filter(self._application_institute_access_q([institute_code]))
            .distinct()
            .count()
        )

        total_projects = (
            ProjectApplication.objects.filter(
                status__code="approved",
                semester_id=semester_id,
            )
            .filter(self._application_institute_access_q([institute_code]))
            .distinct()
            .count()
        )

        total_assignments = ProjectTrackGroup.objects.filter(
            project_track__semester_id=semester_id,
            study_group__institute_id=institute_code,
            study_group__is_end=False,
            project_track__application_links__isnull=False,
        ).count()

        average = (
            round(total_assignments / total_groups, 1) if total_groups > 0 else 0.0
        )

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

        groups_with_projects = (
            StudyGroup.objects.filter(
                is_end=False,
                institute__is_active=True,
                track_group_links__project_track__semester_id=semester_id,
                track_group_links__project_track__application_links__isnull=False,
            )
            .distinct()
            .count()
        )
        groups_without_projects = total_groups - groups_with_projects

        distributed_projects = (
            ProjectApplication.objects.filter(
                status__code="approved",
                semester_id=semester_id,
                track_application_links__project_track__semester_id=semester_id,
                track_application_links__project_track__group_links__isnull=False,
            )
            .distinct()
            .count()
        )

        total_projects = ProjectApplication.objects.filter(
            status__code="approved",
            semester_id=semester_id,
        ).count()

        total_assignments = ProjectTrackGroup.objects.filter(
            project_track__semester_id=semester_id,
            study_group__is_end=False,
            study_group__institute__is_active=True,
            project_track__application_links__isnull=False,
        ).count()

        average = (
            round(total_assignments / total_groups, 1) if total_groups > 0 else 0.0
        )

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

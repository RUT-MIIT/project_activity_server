"""Репозиторий для работы с проектными заявками в БД.

Изолирует всю работу с базой данных от бизнес-логики.
"""

from django.contrib.auth import get_user_model
from django.db.models import Max
from django.utils import timezone

from accounts.models import Department
from showcase.dto.application import (
    ProjectApplicationCreateDTO,
    ProjectApplicationUpdateDTO,
)
from showcase.models import ApplicationStatus, Institute, ProjectApplication, Tag

User = get_user_model()


class ProjectApplicationRepository:
    """Репозиторий - вся работа с БД здесь"""

    def create(
        self,
        dto: ProjectApplicationCreateDTO,
        author: User,
        status_code: str,
        is_external: bool = False,
    ) -> ProjectApplication:
        """Создание заявки в БД.

        Принимает DTO и пользователя, возвращает созданную модель.
        Генерирует год заявки, номер внутри года и номер для печати.
        """
        # Получаем статус
        status = ApplicationStatus.objects.get(code=status_code)

        # Определяем год заявки (год создания)
        current_year = timezone.now().year

        # Находим максимальный номер заявки для текущего года
        # Используем aggregate(Max) для получения последнего номера, а не count()
        max_number_result = ProjectApplication.objects.filter(
            application_year=current_year
        ).aggregate(max_number=Max("year_sequence_number"))
        max_number = max_number_result["max_number"]

        # Если заявок в этом году еще нет, начинаем с 1
        # Иначе увеличиваем на 1
        if max_number is None:
            next_number = 1
        else:
            next_number = max_number + 1

        # Генерируем номер для печати: последние две цифры года + тире + номер с ведущими нулями (5 цифр)
        year_short = str(current_year)[-2:]
        print_number = f"{year_short}-{next_number:05d}"

        # Создаем заявку
        application = ProjectApplication.objects.create(
            title=dto.title,
            company=dto.company,
            author=author,
            author_lastname=dto.author_lastname or "",
            author_firstname=dto.author_firstname or "",
            author_middlename=dto.author_middlename or "",
            author_email=dto.author_email or "",
            author_phone=dto.author_phone or "",
            author_role=dto.author_role or "",
            author_division=dto.author_division or "",
            company_contacts=dto.company_contacts,
            project_level=dto.project_level,
            problem_holder=dto.problem_holder or "",
            goal=dto.goal or "",
            barrier=dto.barrier or "",
            existing_solutions=dto.existing_solutions,
            context=dto.context,
            stakeholders=dto.stakeholders,
            recommended_tools=dto.recommended_tools,
            experts=dto.experts,
            additional_materials=dto.additional_materials,
            needs_consultation=dto.needs_consultation,
            main_department=(
                Department.objects.get(pk=dto.main_department_id)
                if dto.main_department_id
                else None
            ),
            status=status,
            application_year=current_year,
            year_sequence_number=next_number,
            print_number=print_number,
            is_external=is_external,
            is_internal_customer=dto.is_internal_customer,
        )

        # Устанавливаем M2M поля
        if dto.target_institutes:
            institutes = Institute.objects.filter(code__in=dto.target_institutes)
            application.target_institutes.set(institutes)

        if dto.tags:
            tags = Tag.objects.filter(id__in=dto.tags)
            application.tags.set(tags)

        return application

    def get_by_id(self, application_id: int) -> ProjectApplication:
        """Получение заявки по ID с оптимизацией запросов.

        Включает все связанные объекты для детального просмотра.
        """
        return (
            ProjectApplication.objects.select_related("status", "author")
            .prefetch_related(
                "target_institutes",
                "tags",
                "involved_users__user",
                "involved_departments__department",
                "status_logs__from_status",
                "status_logs__to_status",
                "status_logs__actor",
                "comments__author",
                "comments__author__role",
                "comments__author__department",
            )
            .get(pk=application_id)
        )

    def get_by_id_simple(self, application_id: int) -> ProjectApplication:
        """Получение заявки по ID без дополнительных связанных объектов.

        Для простых операций, где не нужны все связи.
        """
        return ProjectApplication.objects.select_related(
            "status", "author", "main_department"
        ).get(pk=application_id)

    def filter_by_user(self, user: User) -> list[ProjectApplication]:
        """Получение заявок пользователя, где он является автором.

        Оптимизированный запрос для списка заявок.
        Ранее сюда попадали также заявки, где пользователь был причастным
        через involved_users. Теперь для "Мои заявки" и основного списка
        считаем "заявками пользователя" только те, где он указан автором.
        """
        return list(
            ProjectApplication.objects.filter(author=user)
            .select_related("status", "author")
            .prefetch_related("target_institutes", "tags")
            .order_by("-creation_date")
        )

    def filter_by_user_queryset(self, user: User):
        """Получение QuerySet заявок пользователя для пагинации.

        Возвращает QuerySet вместо списка для поддержки пагинации.
        Ранее сюда попадали также заявки, где пользователь был причастным
        через involved_users. Теперь сюда попадают только заявки, где он
        является автором.
        """
        return (
            ProjectApplication.objects.filter(author=user)
            .select_related("status", "author")
            .prefetch_related("target_institutes", "tags")
            .order_by("-creation_date")
        )

    def filter_coordination_by_user(self, user: User) -> list[ProjectApplication]:
        """Получение заявок для координации пользователя.
        Заявки, где пользователь причастен и статус не approved/rejected.
        """
        from django.db.models import Count

        return list(
            ProjectApplication.objects.filter(involved_users__user=user)
            .select_related("status", "author")
            .prefetch_related("target_institutes")
            .annotate(comments_count=Count("comments"))
            .distinct()
            .order_by("-creation_date")
        )

    def filter_coordination_by_user_queryset(self, user: User):
        """Получение QuerySet заявок для координации пользователя для пагинации."""
        from django.db.models import Count

        return (
            ProjectApplication.objects.filter(involved_users__user=user)
            .select_related("status", "author")
            .prefetch_related("target_institutes")
            .annotate(comments_count=Count("comments"))
            .distinct()
            .order_by("-creation_date")
        )

    def filter_coordination_by_department(self, department) -> list[ProjectApplication]:
        """Получение заявок для координации по причастному подразделению.
        Заявки, где подразделение причастно и статус не approved/rejected.
        """
        return list(
            ProjectApplication.objects.filter(
                involved_departments__department=department
            )
            .select_related("status", "author")
            .prefetch_related("target_institutes", "tags")
            .distinct()
            .order_by("-creation_date")
        )

    def filter_by_status(self, status_code: str) -> list[ProjectApplication]:
        """Получение заявок по статусу.

        Для административных операций.
        """
        return list(
            ProjectApplication.objects.filter(status__code=status_code)
            .select_related("status", "author")
            .prefetch_related("target_institutes", "tags")
            .order_by("-creation_date")
        )

    def filter_by_status_queryset(self, status_code: str):
        """Получение QuerySet заявок по статусу для пагинации."""
        return (
            ProjectApplication.objects.filter(status__code=status_code)
            .select_related("status", "author")
            .prefetch_related("target_institutes", "tags")
            .order_by("-creation_date")
        )

    def filter_all_except_status(self, status_code: str) -> list[ProjectApplication]:
        """Получение всех заявок, кроме указанных по статусу.

        Используется, например, для роли cpds, чтобы видеть все заявки,
        кроме заявок в промежуточном статусе require_assignment.
        """
        return list(
            ProjectApplication.objects.exclude(status__code=status_code)
            .select_related("status", "author")
            .prefetch_related("target_institutes", "tags")
            .order_by("-creation_date")
        )

    def filter_by_company(self, company_name: str) -> list[ProjectApplication]:
        """Получение заявок по компании.

        Для поиска и аналитики.
        """
        return list(
            ProjectApplication.objects.filter(company__icontains=company_name)
            .select_related("status", "author")
            .prefetch_related("target_institutes", "tags")
            .order_by("-creation_date")
        )

    def update(
        self, application: ProjectApplication, dto: ProjectApplicationUpdateDTO
    ) -> ProjectApplication:
        """Обновление заявки.

        Обновляет только переданные поля.
        """
        # Обновляем только переданные поля
        # Автоматически получаем поля из DTO
        update_fields = []

        # Получаем все поля DTO (исключаем приватные и специальные)
        dto_fields = [
            field
            for field in dir(dto)
            if not field.startswith("_")
            and not callable(getattr(dto, field))
            and field not in ("target_institutes", "tags", "main_department_id")
        ]  # M2M поля и ForeignKey обрабатываем отдельно

        for field_name in dto_fields:
            field_value = getattr(dto, field_name, None)
            if field_value is not None:
                # Проверяем, что поле существует в модели
                if hasattr(application, field_name):
                    setattr(application, field_name, field_value)
                    update_fields.append(field_name)

        # Обрабатываем main_department_id отдельно, так как это ForeignKey
        if hasattr(dto, "main_department_id") and dto.main_department_id is not None:
            if dto.main_department_id:
                try:
                    application.main_department = Department.objects.get(
                        pk=dto.main_department_id
                    )
                except Department.DoesNotExist as err:
                    raise ValueError(
                        f"Подразделение с id {dto.main_department_id} не найдено"
                    ) from err
            else:
                # Если передан 0, сбрасываем поле
                application.main_department = None
            update_fields.append("main_department")

        # Обновляем M2M поля
        if dto.target_institutes is not None:
            institutes = Institute.objects.filter(code__in=dto.target_institutes)
            application.target_institutes.set(institutes)

        if dto.tags is not None:
            tags = Tag.objects.filter(id__in=dto.tags)
            application.tags.set(tags)

        # Сохраняем только изменённые поля для оптимизации
        if update_fields:
            application.save(update_fields=update_fields)
        else:
            application.save()

        return application

    def update_status(
        self, application: ProjectApplication, status_code: str
    ) -> ProjectApplication:
        """Обновление статуса заявки.

        Простая операция для изменения статуса.
        """
        status = ApplicationStatus.objects.get(code=status_code)
        application.status = status
        application.save()
        return application

    def delete(self, application: ProjectApplication) -> bool:
        """Удаление заявки.

        Возвращает True если заявка была удалена.
        """
        application_id = application.id
        application.delete()
        return not ProjectApplication.objects.filter(pk=application_id).exists()

    def exists(self, application_id: int) -> bool:
        """Проверка существования заявки.

        Быстрая проверка без загрузки объекта.
        """
        return ProjectApplication.objects.filter(pk=application_id).exists()

    def count_by_user(self, user: User) -> int:
        """Подсчет заявок пользователя.

        Для статистики и ограничений.
        """
        return ProjectApplication.objects.filter(author=user).count()

    def count_by_status(self, status_code: str) -> int:
        """Подсчет заявок по статусу.

        Для аналитики и отчетов.
        """
        return ProjectApplication.objects.filter(status__code=status_code).count()

    def get_recent_applications(self, limit: int = 10) -> list[ProjectApplication]:
        """Получение последних заявок.

        Для дашборда и новостей.
        """
        return list(
            ProjectApplication.objects.select_related("status", "author")
            .prefetch_related("target_institutes")
            .order_by("-creation_date")[:limit]
        )

    def get_all_applications_queryset(self):
        """Получение QuerySet всех заявок для пагинации.

        Для административных операций и общего списка.
        """
        return (
            ProjectApplication.objects.select_related("status", "author")
            .prefetch_related("target_institutes")
            .order_by("-creation_date")
        )

    def filter_external_applications(
        self, status_code: str | None = None
    ) -> list[ProjectApplication]:
        """Получение всех внешних заявок (is_external=True).

        Args:
            status_code: Необязательный код статуса для дополнительной фильтрации.

        Returns:
            list[ProjectApplication]: Список внешних заявок.
        """
        qs = ProjectApplication.objects.filter(is_external=True)
        if status_code:
            qs = qs.filter(status__code=status_code)

        return list(
            qs.select_related("status", "author")
            .prefetch_related("target_institutes", "tags")
            .order_by("-creation_date")
        )

    def filter_external_applications_queryset(self, status_code: str | None = None):
        """Получение QuerySet внешних заявок для пагинации.

        Args:
            status_code: Необязательный код статуса для дополнительной фильтрации.

        Returns:
            QuerySet: QuerySet внешних заявок.
        """
        qs = ProjectApplication.objects.filter(is_external=True)
        if status_code:
            qs = qs.filter(status__code=status_code)

        return (
            qs.select_related("status", "author")
            .prefetch_related("target_institutes", "tags")
            .order_by("-creation_date")
        )

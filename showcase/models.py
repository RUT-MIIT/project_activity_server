from django.conf import settings
from django.db import models


class Institute(models.Model):
    """Справочник институтов/академий для выбора целевых институтов в заявках"""

    code = models.CharField(
        max_length=50, primary_key=True, unique=True, verbose_name="Код института"
    )
    name = models.CharField(
        max_length=100, unique=True, verbose_name="Название института"
    )
    position = models.PositiveIntegerField(verbose_name="Позиция для сортировки")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    department = models.ForeignKey(
        "accounts.Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="institutes",
        verbose_name="Связанное подразделение",
    )

    class Meta:
        verbose_name = "Институт"
        verbose_name_plural = "Институты"
        ordering = ["position"]

    def __str__(self):
        return f"{self.code}: {self.name}"


class ApplicationStatus(models.Model):
    code = models.CharField(
        max_length=50, primary_key=True, unique=True, verbose_name="Код статуса"
    )
    name = models.CharField(
        max_length=100, unique=True, verbose_name="Название статуса"
    )
    position = models.PositiveIntegerField(verbose_name="Позиция")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Статус заявки"
        verbose_name_plural = "Статусы заявок"
        ordering = ["position"]

    @property
    def id(self) -> str:
        """Совместимость с кодом, используемым как первичный ключ."""
        return self.code

    def __str__(self):
        return f"{self.code}: {self.name}"


class Tag(models.Model):
    """Теги для проектных заявок"""

    name = models.CharField(max_length=255, unique=True, verbose_name="Название тега")
    category = models.CharField(max_length=255, verbose_name="Категория тега")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ["category", "name"]

    def __str__(self):
        return f"{self.category}: {self.name}"


class ProjectApplication(models.Model):
    # Базовые поля
    creation_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )
    status = models.ForeignKey(
        ApplicationStatus,
        on_delete=models.PROTECT,
        related_name="applications",
        verbose_name="Статус",
        null=True,
        blank=True,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="project_applications",
        verbose_name="Автор заявки",
    )

    # Раздел "Контактные данные"
    author_lastname = models.CharField(
        max_length=100, verbose_name="Фамилия автора", default=""
    )
    author_firstname = models.CharField(
        max_length=100, verbose_name="Имя автора", default=""
    )
    author_middlename = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Отчество автора"
    )
    author_email = models.EmailField(
        verbose_name="Электронная почта автора", default=""
    )
    author_phone = models.CharField(
        max_length=20, verbose_name="Телефон автора", default=""
    )
    author_role = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Роль автора"
    )
    author_division = models.CharField(
        max_length=200, blank=True, null=True, verbose_name="Подразделение автора"
    )
    main_department = models.ForeignKey(
        "accounts.Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="main_applications",
        verbose_name="Основное подразделение",
    )

    # Раздел "О проекте"
    company = models.CharField(
        max_length=255, verbose_name="Наименование организации-заказчика", default=""
    )
    company_contacts = models.TextField(
        verbose_name="Контактные данные представителя заказчика", default=""
    )
    target_institutes = models.ManyToManyField(
        Institute,
        verbose_name=(
            "Экспертам из какого института или академии стоит "
            "обратить особое внимание на заявку"
        ),
        blank=True,
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name="Теги",
        blank=True,
    )
    project_level = models.CharField(
        max_length=100, verbose_name="Уровень проекта", default=""
    )

    # Раздел "Проблема"
    problem_holder = models.CharField(
        max_length=255, verbose_name="Носитель проблемы", default=""
    )
    goal = models.TextField(verbose_name="Цель", default="")
    barrier = models.TextField(verbose_name="Барьер", default="")
    existing_solutions = models.TextField(
        verbose_name="Существующие решения", default=""
    )

    # Раздел "Контекст"
    context = models.TextField(blank=True, null=True, verbose_name="Контекст")
    stakeholders = models.TextField(
        blank=True, null=True, verbose_name="Другие заинтересованные стороны"
    )
    recommended_tools = models.TextField(
        blank=True, null=True, verbose_name="Рекомендуемые инструменты"
    )
    experts = models.TextField(blank=True, null=True, verbose_name="Эксперты")
    additional_materials = models.TextField(
        blank=True, null=True, verbose_name="Дополнительные материалы"
    )
    title = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Название проекта"
    )
    needs_consultation = models.BooleanField(
        default=False, verbose_name="Нужна консультация"
    )
    is_external = models.BooleanField(default=False, verbose_name="Внешняя заявка")
    is_internal_customer = models.BooleanField(
        default=False, verbose_name="Внутренний заказчик"
    )

    # Нумерация заявок
    application_year = models.PositiveIntegerField(
        verbose_name="Год заявки", null=True, blank=True, db_index=True
    )
    year_sequence_number = models.PositiveIntegerField(
        verbose_name="Номер заявки внутри года", null=True, blank=True
    )
    print_number = models.CharField(
        max_length=10,
        verbose_name="Номер для печати",
        null=True,
        blank=True,
        db_index=True,
    )

    class Meta:
        verbose_name = "Проектная заявка"
        verbose_name_plural = "Проектные заявки"
        ordering = ["-creation_date"]
        unique_together = [("application_year", "year_sequence_number")]

    def __str__(self):
        if self.title:
            return self.title
        return f"Заявка #{self.id} от {self.author_lastname} {self.author_firstname}"


class ProjectApplicationStatusLog(models.Model):
    application = models.ForeignKey(
        ProjectApplication,
        on_delete=models.CASCADE,
        related_name="status_logs",
        verbose_name="Заявка",
    )
    ACTION_TYPES = (
        ("status_change", "Изменение статуса"),
        ("involved_user_added", "Добавлен причастный пользователь"),
        ("involved_user_removed", "Удален причастный пользователь"),
        ("involved_department_added", "Добавлено причастное подразделение"),
        ("involved_department_removed", "Удалено причастное подразделение"),
        ("application_updated", "Обновление заявки"),
    )
    action_type = models.CharField(
        max_length=32,
        choices=ACTION_TYPES,
        default="status_change",
        verbose_name="Тип действия",
    )
    involved_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="involved_user_logs",
        verbose_name="Причастный пользователь",
    )
    involved_department = models.ForeignKey(
        "accounts.Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="involved_department_logs",
        verbose_name="Причастное подразделение",
    )
    changed_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата и время изменения"
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Актор",
        related_name="status_changes",
    )
    from_status = models.ForeignKey(
        ApplicationStatus,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="from_status_logs",
        verbose_name="Был статус",
    )
    to_status = models.ForeignKey(
        ApplicationStatus,
        on_delete=models.PROTECT,
        related_name="to_status_logs",
        verbose_name="Стало статус",
    )
    previous_status_log = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="next_logs",
        verbose_name="Предыдущий лог",
    )

    class Meta:
        verbose_name = "Лог изменения статуса заявки"
        verbose_name_plural = "Логи изменения статусов заявок"
        ordering = ["-changed_at"]

    def __str__(self):
        return (
            f"{self.application} | {self.from_status} → {self.to_status} "
            f"({self.changed_at})"
        )


class ProjectApplicationComment(models.Model):
    application = models.ForeignKey(
        ProjectApplication,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Заявка",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Автор",
        related_name="application_comments",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата и время комментария"
    )
    field = models.CharField(
        max_length=100,
        verbose_name="Поле",
        help_text="Поле, к которому относится комментарий",
    )
    text = models.TextField(verbose_name="Текст комментария")

    class Meta:
        verbose_name = "Комментарий к заявке"
        verbose_name_plural = "Комментарии к заявкам"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.author} ({self.created_at}): {self.field} — {self.text[:30]}..."


class ApplicationInvolvedUser(models.Model):
    """Причастные пользователи к заявке"""

    application = models.ForeignKey(
        ProjectApplication,
        on_delete=models.CASCADE,
        related_name="involved_users",
        verbose_name="Заявка",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="involved_in_applications",
        verbose_name="Пользователь",
    )
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="added_involved_users",
        verbose_name="Добавил",
    )

    class Meta:
        verbose_name = "Причастный пользователь"
        verbose_name_plural = "Причастные пользователи"
        unique_together = [("application", "user")]
        ordering = ["-added_at"]

    def __str__(self):
        return f"{self.application} — {self.user}"


class ApplicationInvolvedDepartment(models.Model):
    """Причастные подразделения к заявке"""

    application = models.ForeignKey(
        ProjectApplication,
        on_delete=models.CASCADE,
        related_name="involved_departments",
        verbose_name="Заявка",
    )
    department = models.ForeignKey(
        "accounts.Department",
        on_delete=models.CASCADE,
        related_name="involved_in_applications",
        verbose_name="Подразделение",
    )
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="added_involved_departments",
        verbose_name="Добавил",
    )

    class Meta:
        verbose_name = "Причастное подразделение"
        verbose_name_plural = "Причастные подразделения"
        unique_together = [("application", "department")]
        ordering = ["-added_at"]

    def __str__(self):
        return f"{self.application} — {self.department}"

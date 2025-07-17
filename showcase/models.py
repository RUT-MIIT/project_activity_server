from django.db import models
from django.conf import settings


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

    def __str__(self):
        return f"{self.code}: {self.name}"


class ProjectApplication(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    company = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(
        ApplicationStatus,
        on_delete=models.PROTECT,
        related_name='applications',
        verbose_name='Статус',
        null=True,
        blank=True,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="project_applications",
    )

    def __str__(self):
        return self.title


class ProjectApplicationStatusLog(models.Model):
    application = models.ForeignKey(
        ProjectApplication,
        on_delete=models.CASCADE,
        related_name='status_logs',
        verbose_name='Заявка',
    )
    changed_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата и время изменения'
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Актор',
        related_name='status_changes',
    )
    from_status = models.ForeignKey(
        ApplicationStatus,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='from_status_logs',
        verbose_name='Был статус',
    )
    to_status = models.ForeignKey(
        ApplicationStatus,
        on_delete=models.PROTECT,
        related_name='to_status_logs',
        verbose_name='Стало статус',
    )
    previous_status_log = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='next_logs',
        verbose_name='Предыдущий лог',
    )

    class Meta:
        verbose_name = 'Лог изменения статуса заявки'
        verbose_name_plural = 'Логи изменения статусов заявок'
        ordering = ['-changed_at']

    def __str__(self):
        return (
            f"{self.application} | {self.from_status} → {self.to_status} "
            f"({self.changed_at})"
        )


class ProjectApplicationComment(models.Model):
    status_log = models.ForeignKey(
        ProjectApplicationStatusLog,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Лог статуса',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Автор',
        related_name='application_comments',
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата и время комментария'
    )
    field = models.CharField(
        max_length=100,
        verbose_name='Поле',
        help_text='Поле, к которому относится комментарий',
    )
    text = models.TextField(verbose_name='Текст комментария')

    class Meta:
        verbose_name = 'Комментарий к изменению статуса заявки'
        verbose_name_plural = 'Комментарии к изменениям статусов заявок'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author} ({self.created_at}): {self.field} — {self.text[:30]}..."

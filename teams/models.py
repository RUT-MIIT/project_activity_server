from django.conf import settings
from django.db import models


class Direction(models.Model):
    """Направление подготовки (ФГОС ВО)."""

    class Level(models.TextChoices):
        BAKALAVRIAT = "бакалавриат", "Бакалавриат"
        SPECIALITET = "специалитет", "Специалитет"

    level = models.CharField(
        max_length=32,
        choices=Level.choices,
        verbose_name="Уровень подготовки",
    )
    code = models.CharField(
        max_length=9,
        primary_key=True,
        verbose_name="Код направления",
    )
    name = models.CharField(max_length=512, verbose_name="Название")

    class Meta:
        verbose_name = "Направление подготовки"
        verbose_name_plural = "Направления подготовки"
        ordering = ("code",)

    def __str__(self) -> str:
        return f"{self.code} ({self.get_level_display()})"


class StudyGroup(models.Model):
    """Учебная группа."""

    name = models.CharField(max_length=255, verbose_name="Название")
    code = models.CharField(
        max_length=64,
        blank=True,
        default="",
        verbose_name="Код",
    )
    direction = models.ForeignKey(
        Direction,
        on_delete=models.PROTECT,
        related_name="study_groups",
        verbose_name="Направление подготовки",
    )
    institute = models.ForeignKey(
        "showcase.Institute",
        on_delete=models.PROTECT,
        related_name="study_groups",
        verbose_name="Институт",
    )
    course_number = models.PositiveIntegerField(
        default=1,
        verbose_name="Номер курса",
    )
    is_end = models.BooleanField(
        default=False,
        verbose_name="Закончили обучение",
    )

    class Meta:
        verbose_name = "Учебная группа"
        verbose_name_plural = "Учебные группы"
        ordering = ("institute", "name")

    def __str__(self) -> str:
        if self.code:
            return f"{self.name} ({self.code})"
        return self.name


class Team(models.Model):
    """Команда участников проектной деятельности."""

    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(blank=True, default="", verbose_name="Описание")
    leader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="led_teams",
        verbose_name="Руководитель",
    )
    project_application = models.ForeignKey(
        "showcase.ProjectApplication",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="teams",
        verbose_name="Проектная заявка",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команды"
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.name


class TeamMember(models.Model):
    """Участник команды."""

    class Role(models.TextChoices):
        LEADER = "leader", "Руководитель"
        MEMBER = "member", "Участник"

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="members",
        verbose_name="Команда",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="team_memberships",
        verbose_name="Пользователь",
    )
    role = models.CharField(
        max_length=16,
        choices=Role.choices,
        default=Role.MEMBER,
        verbose_name="Роль в команде",
    )
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата вступления")

    class Meta:
        verbose_name = "Участник команды"
        verbose_name_plural = "Участники команд"
        ordering = ("role", "joined_at")
        constraints = [
            models.UniqueConstraint(
                fields=["team", "user"],
                name="unique_team_member",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.user} — {self.team} ({self.role})"

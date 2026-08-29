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
    enrollment_year = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Год набора",
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
    profile = models.CharField(
        max_length=512,
        blank=True,
        default="",
        verbose_name="Профиль",
    )
    form = models.CharField(
        max_length=64,
        blank=True,
        default="",
        verbose_name="Форма обучения",
    )
    mentor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mentored_study_groups",
        verbose_name="Наставник",
        limit_choices_to={"role__code": "mentor"},
    )

    class Meta:
        verbose_name = "Учебная группа"
        verbose_name_plural = "Учебные группы"
        ordering = ("institute", "name")

    def __str__(self) -> str:
        if self.code:
            return f"{self.name} ({self.code})"
        return self.name


class StudyGroupSemester(models.Model):
    """Наставники учебной группы в конкретном семестре."""

    study_group = models.ForeignKey(
        StudyGroup,
        on_delete=models.CASCADE,
        related_name="semester_enrollments",
        verbose_name="Учебная группа",
    )
    semester = models.ForeignKey(
        "accounts.Semester",
        on_delete=models.PROTECT,
        related_name="study_group_semesters",
        verbose_name="Семестр",
    )
    mentors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="mentored_group_semesters",
        blank=True,
        verbose_name="Наставники",
    )

    class Meta:
        verbose_name = "Группа в семестре"
        verbose_name_plural = "Группы в семестрах"
        ordering = ("study_group", "semester")
        constraints = [
            models.UniqueConstraint(
                fields=["study_group", "semester"],
                name="unique_study_group_semester",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.study_group} — {self.semester}"


class Team(models.Model):
    """Постоянная команда участников проектной деятельности."""

    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(blank=True, default="", verbose_name="Описание")
    home_study_group = models.ForeignKey(
        StudyGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="home_teams",
        verbose_name="Домашняя учебная группа",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команды"
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.name


class TeamSemester(models.Model):
    """Участие команды в конкретном семестре: проект, наставник, капитан."""

    class Status(models.TextChoices):
        FORMING = "forming", "Формирование"
        ASSEMBLED = "assembled", "Состав подтверждён"

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="semester_enrollments",
        verbose_name="Команда",
    )
    semester = models.ForeignKey(
        "accounts.Semester",
        on_delete=models.PROTECT,
        related_name="team_semesters",
        verbose_name="Семестр",
    )
    project_track = models.ForeignKey(
        "showcase.ProjectTrack",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="team_semesters",
        verbose_name="Проектный трек",
    )
    project_application = models.ForeignKey(
        "showcase.ProjectApplication",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="team_semesters",
        verbose_name="Проектная заявка",
    )
    mentor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mentored_team_semesters",
        verbose_name="Наставник",
        limit_choices_to={"role__code": "mentor"},
    )
    captain = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="captained_team_semesters",
        verbose_name="Капитан",
    )
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.FORMING,
        db_index=True,
        verbose_name="Статус состава",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        verbose_name = "Команда в семестре"
        verbose_name_plural = "Команды в семестрах"
        ordering = ("-created_at",)
        constraints = [
            models.UniqueConstraint(
                fields=["team", "semester"],
                name="unique_team_semester",
            ),
        ]
        indexes = [
            models.Index(
                fields=["project_track", "status"],
                name="team_sem_track_status_idx",
            ),
            models.Index(
                fields=["semester", "project_track"],
                name="team_sem_semester_track_idx",
            ),
            models.Index(
                fields=["semester", "project_track", "project_application"],
                name="team_sem_enroll_lookup_idx",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.team} — {self.semester}"


class TeamSemesterMember(models.Model):
    """Участник команды в конкретном семестре."""

    class Role(models.TextChoices):
        LEADER = "leader", "Руководитель"
        MEMBER = "member", "Участник"

    team_semester = models.ForeignKey(
        TeamSemester,
        on_delete=models.CASCADE,
        related_name="members",
        verbose_name="Команда в семестре",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="team_semester_memberships",
        verbose_name="Пользователь",
    )
    semester = models.ForeignKey(
        "accounts.Semester",
        on_delete=models.PROTECT,
        related_name="team_semester_memberships",
        verbose_name="Семестр",
    )
    role = models.CharField(
        max_length=16,
        choices=Role.choices,
        default=Role.MEMBER,
        verbose_name="Роль в команде",
    )
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата вступления")

    class Meta:
        verbose_name = "Участник команды в семестре"
        verbose_name_plural = "Участники команд в семестрах"
        ordering = ("role", "joined_at")
        constraints = [
            models.UniqueConstraint(
                fields=["team_semester", "user"],
                name="unique_team_semester_member",
            ),
            models.UniqueConstraint(
                fields=["user", "semester"],
                name="unique_user_semester_team",
            ),
        ]

    def save(self, *args, **kwargs) -> None:
        if self.team_semester_id:
            self.semester_id = self.team_semester.semester_id
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.user} — {self.team_semester} ({self.role})"


class TeamJoinRequest(models.Model):
    """Заявка студента на вступление в команду в семестре."""

    class Status(models.TextChoices):
        PENDING = "pending", "Ожидает"
        APPROVED = "approved", "Одобрена"
        REJECTED = "rejected", "Отклонена"
        OBSOLETE = "obsolete", "Не актуальна"

    team_semester = models.ForeignKey(
        TeamSemester,
        on_delete=models.CASCADE,
        related_name="join_requests",
        verbose_name="Команда в семестре",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="team_join_requests",
        verbose_name="Заявитель",
    )
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
        verbose_name="Статус",
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_team_join_requests",
        verbose_name="Рассмотрел",
    )
    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата рассмотрения",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Заявка на вступление в команду"
        verbose_name_plural = "Заявки на вступление в команду"
        ordering = ("-created_at",)
        constraints = [
            models.UniqueConstraint(
                fields=["team_semester", "user"],
                condition=models.Q(status="pending"),
                name="unique_pending_team_join_request",
            ),
        ]
        indexes = [
            models.Index(
                fields=["team_semester", "status"],
                name="join_req_ts_status_idx",
            ),
            models.Index(
                fields=["user", "status"],
                name="join_req_user_status_idx",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.user} → {self.team_semester} ({self.status})"


class TeamInvitation(models.Model):
    """Приглашение капитана студенту вступить в команду."""

    class Status(models.TextChoices):
        PENDING = "pending", "Ожидает"
        ACCEPTED = "accepted", "Принято"
        REJECTED = "rejected", "Отклонено"
        OBSOLETE = "obsolete", "Не актуально"

    team_semester = models.ForeignKey(
        TeamSemester,
        on_delete=models.CASCADE,
        related_name="invitations",
        verbose_name="Команда в семестре",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="team_invitations",
        verbose_name="Приглашённый",
    )
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_team_invitations",
        verbose_name="Кто пригласил",
    )
    role = models.CharField(
        max_length=16,
        choices=TeamSemesterMember.Role.choices,
        default=TeamSemesterMember.Role.MEMBER,
        verbose_name="Роль при вступлении",
    )
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
        verbose_name="Статус",
    )
    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата ответа",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Приглашение в команду"
        verbose_name_plural = "Приглашения в команду"
        ordering = ("-created_at",)
        constraints = [
            models.UniqueConstraint(
                fields=["team_semester", "user"],
                condition=models.Q(status="pending"),
                name="unique_pending_team_invitation",
            ),
        ]
        indexes = [
            models.Index(
                fields=["team_semester", "status"],
                name="invite_ts_status_idx",
            ),
            models.Index(
                fields=["user", "status"],
                name="invite_user_status_idx",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.invited_by} → {self.user} ({self.status})"


class TeamEventLog(models.Model):
    """Лог действий по команде."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="team_event_logs",
        db_index=True,
        verbose_name="Пользователь",
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="event_logs",
        db_index=True,
        verbose_name="Команда",
    )
    team_semester = models.ForeignKey(
        TeamSemester,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="event_logs",
        verbose_name="Команда в семестре",
    )
    text = models.TextField(verbose_name="Текст действия")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата")

    class Meta:
        verbose_name = "Событие команды"
        verbose_name_plural = "События команд"
        ordering = ("-created_at",)
        indexes = [
            models.Index(
                fields=["team_semester", "created_at"],
                name="event_log_ts_created_idx",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.team}: {self.text[:50]}"

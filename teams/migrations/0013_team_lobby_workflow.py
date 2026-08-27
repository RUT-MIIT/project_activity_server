"""Workflow лобби: track/status на TeamSemester, заявки, приглашения, лог."""

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0020_user_mentor_fields"),
        ("showcase", "0036_projecttrack_team_member_limits"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("teams", "0012_remove_legacy_team_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="teamsemester",
            name="project_track",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="team_semesters",
                to="showcase.projecttrack",
                verbose_name="Проектный трек",
            ),
        ),
        migrations.AddField(
            model_name="teamsemester",
            name="status",
            field=models.CharField(
                choices=[
                    ("forming", "Формирование"),
                    ("assembled", "Состав подтверждён"),
                ],
                db_index=True,
                default="forming",
                max_length=16,
                verbose_name="Статус состава",
            ),
        ),
        migrations.AddIndex(
            model_name="teamsemester",
            index=models.Index(
                fields=["project_track", "status"],
                name="team_sem_track_status_idx",
            ),
        ),
        migrations.CreateModel(
            name="TeamJoinRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Ожидает"),
                            ("approved", "Одобрена"),
                            ("rejected", "Отклонена"),
                            ("obsolete", "Не актуальна"),
                        ],
                        db_index=True,
                        default="pending",
                        max_length=16,
                        verbose_name="Статус",
                    ),
                ),
                (
                    "reviewed_at",
                    models.DateTimeField(
                        blank=True,
                        null=True,
                        verbose_name="Дата рассмотрения",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name="Дата создания",
                    ),
                ),
                (
                    "reviewed_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="reviewed_team_join_requests",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Рассмотрел",
                    ),
                ),
                (
                    "team_semester",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="join_requests",
                        to="teams.teamsemester",
                        verbose_name="Команда в семестре",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="team_join_requests",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Заявитель",
                    ),
                ),
            ],
            options={
                "verbose_name": "Заявка на вступление в команду",
                "verbose_name_plural": "Заявки на вступление в команду",
                "ordering": ("-created_at",),
            },
        ),
        migrations.CreateModel(
            name="TeamInvitation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("leader", "Руководитель"),
                            ("member", "Участник"),
                        ],
                        default="member",
                        max_length=16,
                        verbose_name="Роль при вступлении",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Ожидает"),
                            ("accepted", "Принято"),
                            ("rejected", "Отклонено"),
                            ("obsolete", "Не актуально"),
                        ],
                        db_index=True,
                        default="pending",
                        max_length=16,
                        verbose_name="Статус",
                    ),
                ),
                (
                    "reviewed_at",
                    models.DateTimeField(
                        blank=True,
                        null=True,
                        verbose_name="Дата ответа",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name="Дата создания",
                    ),
                ),
                (
                    "invited_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sent_team_invitations",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Кто пригласил",
                    ),
                ),
                (
                    "team_semester",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="invitations",
                        to="teams.teamsemester",
                        verbose_name="Команда в семестре",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="team_invitations",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Приглашённый",
                    ),
                ),
            ],
            options={
                "verbose_name": "Приглашение в команду",
                "verbose_name_plural": "Приглашения в команду",
                "ordering": ("-created_at",),
            },
        ),
        migrations.CreateModel(
            name="TeamEventLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField(verbose_name="Текст действия")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Дата"),
                ),
                (
                    "team",
                    models.ForeignKey(
                        db_index=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="event_logs",
                        to="teams.team",
                        verbose_name="Команда",
                    ),
                ),
                (
                    "team_semester",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="event_logs",
                        to="teams.teamsemester",
                        verbose_name="Команда в семестре",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        db_index=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="team_event_logs",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Событие команды",
                "verbose_name_plural": "События команд",
                "ordering": ("-created_at",),
            },
        ),
        migrations.AddConstraint(
            model_name="teamjoinrequest",
            constraint=models.UniqueConstraint(
                condition=models.Q(("status", "pending")),
                fields=("team_semester", "user"),
                name="unique_pending_team_join_request",
            ),
        ),
        migrations.AddIndex(
            model_name="teamjoinrequest",
            index=models.Index(
                fields=["team_semester", "status"],
                name="join_req_ts_status_idx",
            ),
        ),
        migrations.AddConstraint(
            model_name="teaminvitation",
            constraint=models.UniqueConstraint(
                condition=models.Q(("status", "pending")),
                fields=("team_semester", "user"),
                name="unique_pending_team_invitation",
            ),
        ),
        migrations.AddIndex(
            model_name="teaminvitation",
            index=models.Index(
                fields=["team_semester", "status"],
                name="invite_ts_status_idx",
            ),
        ),
    ]

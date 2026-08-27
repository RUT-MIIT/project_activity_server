# Generated manually for TeamSemester / TeamSemesterMember.

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0020_user_mentor_fields"),
        ("showcase", "0035_projectapplication_team_member_limits"),
        ("teams", "0009_studygroup_mentor"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="team",
            name="home_study_group",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="home_teams",
                to="teams.studygroup",
                verbose_name="Домашняя учебная группа",
            ),
        ),
        migrations.CreateModel(
            name="TeamSemester",
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
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Дата изменения"),
                ),
                (
                    "captain",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="captained_team_semesters",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Капитан",
                    ),
                ),
                (
                    "mentor",
                    models.ForeignKey(
                        blank=True,
                        limit_choices_to={"role__code": "mentor"},
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="mentored_team_semesters",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Наставник",
                    ),
                ),
                (
                    "project_application",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="team_semesters",
                        to="showcase.projectapplication",
                        verbose_name="Проектная заявка",
                    ),
                ),
                (
                    "semester",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="team_semesters",
                        to="accounts.semester",
                        verbose_name="Семестр",
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="semester_enrollments",
                        to="teams.team",
                        verbose_name="Команда",
                    ),
                ),
            ],
            options={
                "verbose_name": "Команда в семестре",
                "verbose_name_plural": "Команды в семестрах",
                "ordering": ("-created_at",),
            },
        ),
        migrations.AddConstraint(
            model_name="teamsemester",
            constraint=models.UniqueConstraint(
                fields=("team", "semester"),
                name="unique_team_semester",
            ),
        ),
        migrations.CreateModel(
            name="TeamSemesterMember",
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
                        choices=[("leader", "Руководитель"), ("member", "Участник")],
                        default="member",
                        max_length=16,
                        verbose_name="Роль в команде",
                    ),
                ),
                (
                    "joined_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата вступления"
                    ),
                ),
                (
                    "semester",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="team_semester_memberships",
                        to="accounts.semester",
                        verbose_name="Семестр",
                    ),
                ),
                (
                    "team_semester",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="members",
                        to="teams.teamsemester",
                        verbose_name="Команда в семестре",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="team_semester_memberships",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Участник команды в семестре",
                "verbose_name_plural": "Участники команд в семестрах",
                "ordering": ("role", "joined_at"),
            },
        ),
        migrations.AddConstraint(
            model_name="teamsemestermember",
            constraint=models.UniqueConstraint(
                fields=("team_semester", "user"),
                name="unique_team_semester_member",
            ),
        ),
        migrations.AddConstraint(
            model_name="teamsemestermember",
            constraint=models.UniqueConstraint(
                fields=("user", "semester"),
                name="unique_user_semester_team",
            ),
        ),
    ]

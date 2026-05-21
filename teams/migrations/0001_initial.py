from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("showcase", "0027_alter_tag_category_blank"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Team",
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
                ("name", models.CharField(max_length=255, verbose_name="Название")),
                (
                    "description",
                    models.TextField(blank=True, default="", verbose_name="Описание"),
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
                    "leader",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="led_teams",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Руководитель",
                    ),
                ),
                (
                    "project_application",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="teams",
                        to="showcase.projectapplication",
                        verbose_name="Проектная заявка",
                    ),
                ),
            ],
            options={
                "verbose_name": "Команда",
                "verbose_name_plural": "Команды",
                "ordering": ("-created_at",),
            },
        ),
        migrations.CreateModel(
            name="TeamMember",
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
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="members",
                        to="teams.team",
                        verbose_name="Команда",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="team_memberships",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Участник команды",
                "verbose_name_plural": "Участники команд",
                "ordering": ("role", "joined_at"),
            },
        ),
        migrations.AddConstraint(
            model_name="teammember",
            constraint=models.UniqueConstraint(
                fields=("team", "user"),
                name="unique_team_member",
            ),
        ),
    ]

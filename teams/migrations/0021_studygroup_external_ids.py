"""Добавляет внешние ID групп из 1С на StudyGroup."""

from django.db import migrations, models
from django.db.models import Q


class Migration(migrations.Migration):

    dependencies = [
        ("teams", "0020_merge_0019_branches"),
    ]

    operations = [
        migrations.AddField(
            model_name="studygroup",
            name="external_group_id",
            field=models.CharField(
                blank=True,
                db_index=True,
                default="",
                max_length=64,
                verbose_name="ID группы (1С)",
            ),
        ),
        migrations.AddField(
            model_name="studygroup",
            name="external_permanent_group_id",
            field=models.CharField(
                blank=True,
                default="",
                max_length=64,
                verbose_name="ID постоянной группы (1С)",
            ),
        ),
        migrations.AddConstraint(
            model_name="studygroup",
            constraint=models.UniqueConstraint(
                condition=Q(("external_group_id__gt", "")),
                fields=("external_group_id",),
                name="unique_studygroup_external_group_id",
            ),
        ),
    ]

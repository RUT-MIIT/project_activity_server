from django.db import migrations, models
import django.db.models.deletion


def clear_study_groups(apps, schema_editor):
    apps.get_model("teams", "StudyGroup").objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("teams", "0005_studygroup_institute_fk"),
    ]

    operations = [
        migrations.RunPython(clear_study_groups, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="studygroup",
            name="direction",
        ),
        # Сначала убираем id (старый PK), иначе PostgreSQL: "multiple primary keys"
        migrations.RemoveField(
            model_name="direction",
            name="id",
        ),
        migrations.AlterField(
            model_name="direction",
            name="code",
            field=models.CharField(
                max_length=9,
                primary_key=True,
                serialize=False,
                verbose_name="Код направления",
            ),
        ),
        migrations.AddField(
            model_name="studygroup",
            name="direction",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="study_groups",
                to="teams.direction",
                verbose_name="Направление подготовки",
            ),
        ),
        migrations.AlterField(
            model_name="studygroup",
            name="direction",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="study_groups",
                to="teams.direction",
                verbose_name="Направление подготовки",
            ),
        ),
    ]

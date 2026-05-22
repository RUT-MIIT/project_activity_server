from django.db import migrations, models


def populate_semester_codes(apps, schema_editor):
    Semester = apps.get_model("accounts", "Semester")
    for semester in Semester.objects.all().order_by("pk"):
        if not semester.code:
            semester.code = f"semester_{semester.pk}"
            semester.save(update_fields=["code"])


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0015_academic_year_settings_semester_fk"),
    ]

    operations = [
        migrations.AddField(
            model_name="semester",
            name="code",
            field=models.CharField(
                max_length=64,
                null=True,
                verbose_name="Код",
            ),
        ),
        migrations.RunPython(populate_semester_codes, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="semester",
            name="code",
            field=models.CharField(max_length=64, unique=True, verbose_name="Код"),
        ),
    ]

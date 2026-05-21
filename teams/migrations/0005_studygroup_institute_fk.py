from django.db import migrations, models
import django.db.models.deletion


def department_to_institute(apps, schema_editor):
    StudyGroup = apps.get_model("teams", "StudyGroup")
    Institute = apps.get_model("showcase", "Institute")
    default = Institute.objects.filter(code="IEF").first()
    for sg in StudyGroup.objects.all():
        inst = None
        if sg.department_id:
            inst = Institute.objects.filter(department_id=sg.department_id).first()
        if inst is None:
            inst = default
        if inst is None:
            raise RuntimeError(
                "Нет института IEF в showcase.Institute для миграции StudyGroup"
            )
        sg.institute_id = inst.code
        sg.save(update_fields=["institute_id"])


class Migration(migrations.Migration):

    dependencies = [
        ("showcase", "0027_alter_tag_category_blank"),
        ("teams", "0004_studygroup_course_is_end"),
    ]

    operations = [
        migrations.AddField(
            model_name="studygroup",
            name="institute",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="study_groups",
                to="showcase.institute",
                verbose_name="Институт",
            ),
        ),
        migrations.RunPython(department_to_institute, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="studygroup",
            name="department",
        ),
        migrations.AlterField(
            model_name="studygroup",
            name="institute",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="study_groups",
                to="showcase.institute",
                verbose_name="Институт",
            ),
        ),
        migrations.AlterModelOptions(
            name="studygroup",
            options={
                "ordering": ("institute", "name"),
                "verbose_name": "Учебная группа",
                "verbose_name_plural": "Учебные группы",
            },
        ),
    ]

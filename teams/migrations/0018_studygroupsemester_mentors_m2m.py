"""M2M-наставники у StudyGroupSemester вместо одиночного FK."""

from django.conf import settings
from django.db import migrations, models


def copy_mentor_fk_to_m2m(apps, schema_editor):
    StudyGroupSemester = apps.get_model("teams", "StudyGroupSemester")
    for enrollment in StudyGroupSemester.objects.exclude(mentor_id=None).iterator():
        enrollment.mentors.add(enrollment.mentor_id)


class Migration(migrations.Migration):

    dependencies = [
        ("teams", "0017_copy_studygroup_mentors_to_semester"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="studygroupsemester",
            name="mentors",
            field=models.ManyToManyField(
                blank=True,
                limit_choices_to={"role__code": "mentor"},
                related_name="mentored_group_semesters",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Наставники",
            ),
        ),
        migrations.RunPython(copy_mentor_fk_to_m2m, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="studygroupsemester",
            name="mentor",
        ),
    ]

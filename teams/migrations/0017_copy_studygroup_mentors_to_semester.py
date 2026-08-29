"""Перенос StudyGroup.mentor в StudyGroupSemester для актуального семестра."""

from django.db import migrations


def copy_mentors_to_active_semester(apps, schema_editor):
    StudyGroup = apps.get_model("teams", "StudyGroup")
    StudyGroupSemester = apps.get_model("teams", "StudyGroupSemester")
    Semester = apps.get_model("accounts", "Semester")
    Settings = apps.get_model("accounts", "Settings")

    try:
        setting = Settings.objects.get(code="active_semester_code")
        semester_code = (setting.value or "").strip()
    except Settings.DoesNotExist:
        return

    if not semester_code:
        return

    semester = Semester.objects.filter(code=semester_code).first()
    if semester is None:
        return

    for group in StudyGroup.objects.exclude(mentor_id=None).iterator():
        StudyGroupSemester.objects.get_or_create(
            study_group_id=group.id,
            semester_id=semester.id,
            defaults={"mentor_id": group.mentor_id},
        )


class Migration(migrations.Migration):

    dependencies = [
        ("teams", "0016_studygroupsemester"),
    ]

    operations = [
        migrations.RunPython(
            copy_mentors_to_active_semester,
            migrations.RunPython.noop,
        ),
    ]

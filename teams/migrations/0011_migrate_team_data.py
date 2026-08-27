# Data migration: Team.leader / TeamMember → TeamSemester / TeamSemesterMember.

import logging

from django.db import migrations

logger = logging.getLogger(__name__)


def forwards(apps, schema_editor):
    Team = apps.get_model("teams", "Team")
    TeamMember = apps.get_model("teams", "TeamMember")
    TeamSemester = apps.get_model("teams", "TeamSemester")
    TeamSemesterMember = apps.get_model("teams", "TeamSemesterMember")
    Semester = apps.get_model("accounts", "Semester")
    Settings = apps.get_model("accounts", "Settings")

    try:
        setting = Settings.objects.get(code="active_semester_code")
        semester_code = (setting.value or "").strip()
    except Settings.DoesNotExist:
        semester_code = ""

    semester = None
    if semester_code:
        semester = Semester.objects.filter(code=semester_code).first()

    if semester is None:
        if Team.objects.exists():
            logger.warning(
                "Активный семестр не настроен: существующие Team не перенесены "
                "в TeamSemester. Привяжите команды вручную в admin."
            )
        return

    for team in Team.objects.all():
        team_semester, _created = TeamSemester.objects.get_or_create(
            team=team,
            semester=semester,
            defaults={
                "captain_id": team.leader_id,
                "project_application_id": team.project_application_id,
            },
        )
        for member in TeamMember.objects.filter(team=team):
            TeamSemesterMember.objects.get_or_create(
                team_semester=team_semester,
                user_id=member.user_id,
                defaults={
                    "semester_id": semester.pk,
                    "role": member.role,
                    "joined_at": member.joined_at,
                },
            )


def backwards(apps, schema_editor):
    TeamSemester = apps.get_model("teams", "TeamSemester")
    TeamSemesterMember = apps.get_model("teams", "TeamSemesterMember")
    TeamSemesterMember.objects.all().delete()
    TeamSemester.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("teams", "0010_team_semester_models"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]

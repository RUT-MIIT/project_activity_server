"""Проставляет project_track командам без трека при единственном треке группы."""

from __future__ import annotations

from django.db import migrations


def backfill_team_semester_track(apps, schema_editor) -> None:
    """Для TeamSemester без трека проставляет единственный трек home-группы."""
    TeamSemester = apps.get_model("teams", "TeamSemester")
    ProjectTrackGroup = apps.get_model("showcase", "ProjectTrackGroup")

    qs = TeamSemester.objects.filter(project_track__isnull=True).select_related("team")
    for team_semester in qs.iterator():
        home_group_id = team_semester.team.home_study_group_id
        if home_group_id is None:
            continue
        track_ids = list(
            ProjectTrackGroup.objects.filter(
                study_group_id=home_group_id,
                project_track__semester_id=team_semester.semester_id,
            )
            .values_list("project_track_id", flat=True)
            .distinct()
        )
        if len(track_ids) != 1:
            continue
        team_semester.project_track_id = track_ids[0]
        team_semester.save(update_fields=["project_track_id"])


def noop_reverse(apps, schema_editor) -> None:
    """Откат data-миграции не восстанавливает NULL-треки."""
    return None


class Migration(migrations.Migration):

    dependencies = [
        ("teams", "0021_studygroup_external_ids"),
        ("showcase", "0040_institute_semester_settings"),
    ]

    operations = [
        migrations.RunPython(backfill_team_semester_track, noop_reverse),
    ]

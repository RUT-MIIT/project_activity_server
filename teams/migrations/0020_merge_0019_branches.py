"""Слияние параллельных миграций 0019 в teams."""

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("teams", "0019_alter_studygroupsemester_mentors"),
        ("teams", "0019_studygroupprojectteacher"),
    ]

    operations = []

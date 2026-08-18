"""Тесты команды import_institutes."""

from __future__ import annotations

from pathlib import Path

from django.core.management import call_command
import pytest

from showcase.models import Institute


def _write_institutes_csv(path: Path, rows: list[tuple[str, str, int]]) -> None:
    lines = ["code,name,position"]
    for code, name, position in rows:
        lines.append(f"{code},{name},{position}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


@pytest.mark.django_db
def test_import_institutes_is_idempotent(tmp_path: Path) -> None:
    csv_path = tmp_path / "institutes.csv"
    _write_institutes_csv(
        csv_path,
        [
            ("IEF", "ИЭФ", 10),
            ("VISH", "ВИШ", 5),
        ],
    )

    call_command("import_institutes", file=str(csv_path))
    call_command("import_institutes", file=str(csv_path))

    assert Institute.objects.count() == 2
    assert Institute.objects.get(code="IEF").name == "ИЭФ"


@pytest.mark.django_db
def test_import_institutes_updates_existing(tmp_path: Path) -> None:
    Institute.objects.create(
        code="IEF",
        name="Старое название",
        position=99,
        is_active=True,
    )
    csv_path = tmp_path / "institutes.csv"
    _write_institutes_csv(csv_path, [("IEF", "ИЭФ", 10)])

    call_command("import_institutes", file=str(csv_path))

    institute = Institute.objects.get(code="IEF")
    assert institute.name == "ИЭФ"
    assert institute.position == 10
    assert Institute.objects.count() == 1


@pytest.mark.django_db
def test_import_institutes_clear_removes_missing(tmp_path: Path) -> None:
    Institute.objects.create(
        code="OLD",
        name="Старый институт",
        position=99,
        is_active=True,
    )

    csv_path = tmp_path / "institutes.csv"
    _write_institutes_csv(csv_path, [("IEF", "ИЭФ", 10)])

    call_command("import_institutes", file=str(csv_path), clear=True)

    assert not Institute.objects.filter(code="OLD").exists()
    assert Institute.objects.filter(code="IEF").exists()

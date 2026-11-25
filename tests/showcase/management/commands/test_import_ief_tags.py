from io import StringIO
from zipfile import ZipFile

from django.core.management import call_command
from django.core.management.base import CommandError
import pytest

from showcase.management.commands.import_ief_tags import DEFAULT_FILE, read_tags
from showcase.models import Institute, ProjectApplication, Tag


def write_docx(path, paragraphs):
    from xml.etree.ElementTree import Element, SubElement, tostring

    ns = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    root = Element(f"{{{ns}}}document")
    body = SubElement(root, f"{{{ns}}}body")
    for value in paragraphs:
        p = SubElement(body, f"{{{ns}}}p")
        r = SubElement(p, f"{{{ns}}}r")
        SubElement(r, f"{{{ns}}}t").text = value
    with ZipFile(path, "w") as doc:
        doc.writestr("word/document.xml", tostring(root, encoding="utf-8"))


def test_original_document():
    tags = read_tags(DEFAULT_FILE)
    assert len(tags) == 94
    assert len({category for _, category in tags}) == 17
    assert tags[0] == ("Транспорт", "Транспорт и логистика")
    assert all(not name.startswith("#") for name, _ in tags)


@pytest.mark.django_db
def test_import_and_repeat_preserve_existing_data(departments):
    department = departments["parent"]
    Institute.objects.create(code="IEF", name="ИЭФ", position=1, department=department)
    existing = Tag.objects.create(name="ТРАНСПОРТ", category="Старая", is_base=False)
    existing.departments.add(department, departments["child"])
    shared = Tag.objects.create(name="Логистика", category="Общий", is_base=True)
    other = Tag.objects.create(name="ЖДПеревозки", category="Другой")
    other.departments.add(departments["child"])
    project = ProjectApplication.objects.create(title="Проект")
    project.tags.add(existing, shared, other)

    output = StringIO()
    call_command("import_ief_tags", stdout=output)
    count = Tag.objects.count()
    call_command("import_ief_tags", stdout=output)

    assert Tag.objects.count() == count
    assert "Создано тегов: 0; пропущено: 94" in output.getvalue()
    assert existing.category == "Старая"
    assert set(existing.departments.values_list("id", flat=True)) == {
        department.id, departments["child"].id
    }
    assert set(project.tags.values_list("id", flat=True)) == {existing.id, shared.id, other.id}
    for name in ("Логистика", "ЖДПеревозки"):
        imported = Tag.objects.get(name=name, departments=department)
        assert imported.category == "Транспорт и логистика"
        assert not imported.is_base


@pytest.mark.django_db
@pytest.mark.parametrize("make_institute", [False, True])
def test_missing_institute_or_department(make_institute):
    if make_institute:
        Institute.objects.create(code="IEF", name="ИЭФ", position=1)
    with pytest.raises(CommandError, match="подразделение"):
        call_command("import_ief_tags")
    assert Tag.objects.count() == 0


@pytest.mark.django_db
def test_invalid_document_has_no_side_effects(tmp_path, departments):
    Institute.objects.create(code="IEF", name="ИЭФ", position=1, department=departments["parent"])
    path = tmp_path / "invalid.docx"
    write_docx(path, ["#БезКатегории"])
    with pytest.raises(CommandError, match="категория"):
        call_command("import_ief_tags", file=path)
    assert Tag.objects.count() == 0


@pytest.mark.django_db
def test_write_error_rolls_back(tmp_path, departments, monkeypatch):
    Institute.objects.create(code="IEF", name="ИЭФ", position=1, department=departments["parent"])
    path = tmp_path / "tags.docx"
    write_docx(path, ["Категория", "#Один", "#Два"])
    original = Tag.objects.create

    def fail_second(**kwargs):
        if kwargs["name"] == "Два":
            raise ValueError("ошибка записи")
        return original(**kwargs)

    monkeypatch.setattr(Tag.objects, "create", fail_second)
    with pytest.raises(CommandError, match="ошибка записи"):
        call_command("import_ief_tags", file=path)
    assert Tag.objects.count() == 0

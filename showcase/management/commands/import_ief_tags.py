"""Импорт специальных тегов ИЭФ из документа в репозитории."""

from pathlib import Path
from xml.etree import ElementTree
from zipfile import BadZipFile, ZipFile

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from showcase.models import Institute, Tag

DEFAULT_FILE = Path(__file__).resolve().parents[3] / "data" / "Хэштеги для ИЭФ.docx"
WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def read_tags(path: Path) -> list[tuple[str, str]]:
    """Прочитать пары (название, категория) в порядке документа."""
    try:
        with ZipFile(path) as document:
            root = ElementTree.fromstring(document.read("word/document.xml"))
    except (OSError, BadZipFile, KeyError, ElementTree.ParseError) as exc:
        raise CommandError(f"Не удалось прочитать документ {path}: {exc}") from exc

    tags = []
    category = None
    for paragraph in root.iter(f"{{{WORD_NS}}}p"):
        value = "".join(
            node.text or "" for node in paragraph.iter(f"{{{WORD_NS}}}t")
        ).strip()
        if not value:
            continue
        if not value.startswith("#"):
            if len(value) > 255:
                raise CommandError(f"Слишком длинное название категории: {value}")
            category = value
            continue
        name = value[1:].strip()
        if not category or not name or len(name) > 255 or name.startswith("#"):
            raise CommandError(f"Некорректный тег или отсутствует категория: {value}")
        tags.append((name, category))
    if not tags:
        raise CommandError("Документ не содержит тегов")
    return tags


class Command(BaseCommand):
    help = "Импортировать специальные теги ИЭФ из документа DOCX"

    def add_arguments(self, parser):
        parser.add_argument("--file", type=Path, default=DEFAULT_FILE, help="Путь к DOCX")

    def handle(self, *args, **options):
        tags = read_tags(options["file"])
        institute = Institute.objects.filter(pk="IEF").select_related("department").first()
        if institute is None or institute.department_id is None:
            raise CommandError("Институт IEF не найден или его подразделение не настроено")

        created = skipped = 0
        try:
            with transaction.atomic():
                existing = {
                    name.casefold()
                    for name in Tag.objects.filter(
                        departments=institute.department
                    ).values_list("name", flat=True)
                }
                for name, category in tags:
                    key = name.casefold()
                    if key in existing:
                        skipped += 1
                        continue
                    tag = Tag.objects.create(name=name, category=category, is_base=False)
                    tag.departments.add(institute.department)
                    existing.add(key)
                    created += 1
        except Exception as exc:
            raise CommandError(f"Ошибка импорта тегов ИЭФ: {exc}") from exc

        self.stdout.write(self.style.SUCCESS(f"Создано тегов: {created}; пропущено: {skipped}."))

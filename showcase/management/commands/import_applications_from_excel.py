"""Импорт проектных заявок из Excel-файла."""

from __future__ import annotations

from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
import pandas as pd

from accounts.models import Semester
from showcase.domain.application import ProjectApplicationDomain
from showcase.domain.application_import import (
    iter_application_import_rows,
    parse_author_name,
)
from showcase.models import Institute, Tag
from showcase.repositories.application import ProjectApplicationRepository
from showcase.services.involved_service import InvolvedManagementService
from showcase.services.logging_service import ApplicationLoggingService

User = get_user_model()

DEFAULT_FILE = "data/Заявки ИМТК 31.08.2026.xlsx"
DEFAULT_STATUS = "await_cpds"
DEFAULT_INSTITUTE = "IMTK"
DEFAULT_AUTHOR = "Иванов Мария"


class Command(BaseCommand):
    help = (
        "Импорт проектных заявок из Excel. "
        "По умолчанию создаёт заявки в статусе «На согласовании в ЦПДС»."
    )

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--file",
            type=str,
            default=DEFAULT_FILE,
            help=f"Путь к Excel-файлу (по умолчанию: {DEFAULT_FILE})",
        )
        parser.add_argument(
            "--status",
            type=str,
            default=DEFAULT_STATUS,
            help=f"Код статуса заявки (по умолчанию: {DEFAULT_STATUS})",
        )
        parser.add_argument(
            "--institute",
            type=str,
            default=DEFAULT_INSTITUTE,
            help=(
                "Код института для main_department "
                f"(по умолчанию: {DEFAULT_INSTITUTE})"
            ),
        )
        parser.add_argument(
            "--author",
            type=str,
            default=DEFAULT_AUTHOR,
            help=f"Автор заявок: «Фамилия Имя» (по умолчанию: {DEFAULT_AUTHOR})",
        )
        parser.add_argument(
            "--author-email",
            type=str,
            default=None,
            help="Email автора для однозначного поиска пользователя",
        )
        parser.add_argument(
            "--semester-id",
            type=int,
            default=None,
            help="ID семестра (по умолчанию — следующий активный семестр)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Только проверить файл и показать, что будет импортировано",
        )

    def handle(self, *args, **options) -> None:
        path = Path(options["file"]).resolve()
        if not path.is_file():
            raise CommandError(f"Файл не найден: {path}")

        institute = self._get_institute(options["institute"])
        author = self._get_author(
            author_name=options["author"],
            author_email=options.get("author_email"),
        )
        semester_id = options.get("semester_id")
        if semester_id is None:
            semester = Semester.get_next()
            semester_id = semester.id if semester else None

        main_department_id = (
            institute.department_id if institute.department_id else author.department_id
        )
        author_fields = self._build_author_fields(author)

        df = pd.read_excel(path)
        import_rows = iter_application_import_rows(
            df,
            author_fields=author_fields,
            default_institute_code=institute.code,
            main_department_id=main_department_id,
            semester_id=semester_id,
        )
        if not import_rows:
            raise CommandError("В файле не найдено строк с заявками для импорта")

        self.stdout.write(
            f"Файл: {path}\n"
            f"Строк к импорту: {len(import_rows)}\n"
            f"Статус: {options['status']}\n"
            f"Институт: {institute.code} ({institute.name})\n"
            f"Автор: {author.get_full_name()} <{author.email}>"
        )

        if options["dry_run"]:
            for item in import_rows:
                tag_suffix = f", тег: {item.tag_name}" if item.tag_name else ""
                self.stdout.write(
                    f"  #{item.row_number}: {item.dto.title or '(без названия)'} "
                    f"— {item.dto.company} "
                    f"[{'внешняя' if item.is_external else 'внутренняя'}]"
                    f"{tag_suffix}"
                )
            self.stdout.write(
                self.style.WARNING("Dry-run: изменения в БД не вносились")
            )
            return

        repository = ProjectApplicationRepository()
        involved_service = InvolvedManagementService()
        logging_service = ApplicationLoggingService()
        status_code = options["status"]
        created_count = 0
        warnings: list[str] = []

        with transaction.atomic():
            for item in import_rows:
                validation = ProjectApplicationDomain.validate_create(item.dto)
                if not validation.is_valid:
                    raise CommandError(
                        f"Строка {item.row_number}: "
                        + "; ".join(
                            f"{key}: {value}"
                            for key, value in validation.errors.items()
                        )
                    )

                application = repository.create(
                    item.dto,
                    author,
                    status_code,
                    is_external=item.is_external,
                )
                involved_service.add_user_and_departments(
                    application=application,
                    user=author,
                    actor=author,
                )
                if institute.department_id:
                    involved_service.add_department_by_short_name(
                        application=application,
                        short_name=institute.department.short_name,
                        actor=author,
                    )
                cpds_added = involved_service.add_department_by_short_name(
                    application=application,
                    short_name="ЦПДС",
                    actor=author,
                )
                if not cpds_added:
                    warnings.append(
                        f"Строка {item.row_number}: подразделение ЦПДС не найдено"
                    )

                if item.tag_name:
                    tag = Tag.objects.filter(name__iexact=item.tag_name).first()
                    if tag:
                        application.tags.add(tag)
                    else:
                        warnings.append(
                            "Строка "
                            f"{item.row_number}: тег «{item.tag_name}» не найден"
                        )

                logging_service.log_status_change(
                    application=application,
                    from_status=None,
                    to_status=application.status,
                    actor=author,
                )
                created_count += 1
                self.stdout.write(
                    f"Создана заявка #{item.row_number}: "
                    f"{application.print_number} — {application.title}"
                )

        self.stdout.write(self.style.SUCCESS(f"Импортировано заявок: {created_count}"))
        for warning in warnings:
            self.stdout.write(self.style.WARNING(warning))

    def _get_institute(self, code: str) -> Institute:
        try:
            return Institute.objects.select_related("department").get(code=code)
        except Institute.DoesNotExist as err:
            raise CommandError(f"Институт с кодом {code!r} не найден") from err

    def _get_author(self, *, author_name: str, author_email: str | None) -> User:
        last_name, first_name = parse_author_name(author_name)
        queryset = User.objects.select_related("role", "department").filter(
            last_name=last_name,
            first_name=first_name,
        )
        if author_email:
            queryset = queryset.filter(email__iexact=author_email)

        users = list(queryset)
        if not users:
            raise CommandError(
                f"Пользователь не найден: {author_name}"
                + (f" ({author_email})" if author_email else "")
            )
        if len(users) > 1:
            emails = ", ".join(user.email for user in users)
            raise CommandError(
                f"Найдено несколько пользователей «{author_name}»: {emails}. "
                "Уточните поиск через --author-email"
            )
        return users[0]

    def _build_author_fields(self, author: User) -> dict[str, str | None]:
        """Формирует контактные поля автора для DTO из пользователя системы."""
        return {
            "author_lastname": author.last_name or "",
            "author_firstname": author.first_name or "",
            "author_middlename": getattr(author, "middle_name", None),
            "author_email": author.email or "",
            "author_phone": getattr(author, "phone", None) or "",
            "author_role": author.role.name if author.role else None,
            "author_division": author.department.name if author.department else None,
        }

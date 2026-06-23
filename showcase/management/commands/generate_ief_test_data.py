"""Генерация тестовых одобренных проектов и учебных групп для института IEF."""

from __future__ import annotations

import itertools
import random
from typing import Sequence

from django.core.management.base import BaseCommand, CommandError
from django.db import models, transaction

from accounts.models import Semester
from showcase.models import ApplicationStatus, Institute, ProjectApplication, Tag
from teams.models import Direction, StudyGroup

INSTITUTE_CODE = "IEF"
PROJECT_TITLE_PREFIX = "Тестовый проект IEF"
GROUP_CODE_PREFIX = "gen-ief-grp-"
GROUP_NAME_PREFIX = "ТГ-IEF"
TEST_APPLICATION_YEAR = 2099

# Направления, используемые в реальных группах IEF (см. teams/data/ief_study_groups.csv).
IEF_DIRECTION_CODES: tuple[str, ...] = (
    "38.03.05",
    "38.03.02",
    "09.03.03",
    "42.03.01",
    "38.03.03",
    "38.03.01",
    "38.05.01",
)

COMPANIES: tuple[str, ...] = (
    "ООО «ТрансЛогистик»",
    "АО «РЖД-Технологии»",
    "ПАО «Ростелеком»",
    "ООО «Цифровой вокзал»",
    "АО «Сколково Транспорт»",
    "ООО «Умная инфраструктура»",
)


class Command(BaseCommand):
    help = (
        "Создаёт тестовые одобренные проекты с тегами и учебные группы "
        f"для института {INSTITUTE_CODE}."
    )

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--projects",
            type=int,
            default=100,
            help="Количество одобренных проектов (по умолчанию: 100)",
        )
        parser.add_argument(
            "--groups",
            type=int,
            default=50,
            help="Количество учебных групп (по умолчанию: 50)",
        )
        parser.add_argument(
            "--semester-id",
            type=int,
            help="ID семестра для проектов (по умолчанию: активный семестр)",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Удалить ранее сгенерированные тестовые данные перед созданием",
        )
        parser.add_argument(
            "--seed",
            type=int,
            default=42,
            help="Seed для случайного распределения тегов (по умолчанию: 42)",
        )

    def handle(self, *args, **options) -> None:
        projects_count: int = options["projects"]
        groups_count: int = options["groups"]
        if projects_count < 1:
            raise CommandError("--projects должен быть >= 1")
        if groups_count < 1:
            raise CommandError("--groups должен быть >= 1")

        institute = self._get_institute()
        semester = self._resolve_semester(options.get("semester_id"))
        approved_status = self._get_approved_status()
        tags = list(Tag.objects.all())
        if not tags:
            raise CommandError(
                "В справочнике нет тегов. Сначала выполните: python manage.py import_tags"
            )

        directions = self._get_directions()
        random.seed(options["seed"])

        with transaction.atomic():
            if options["clear"]:
                self._clear_generated_data()

            created_projects = self._create_projects(
                count=projects_count,
                institute=institute,
                semester=semester,
                approved_status=approved_status,
                tags=tags,
            )
            created_groups = self._create_study_groups(
                count=groups_count,
                institute=institute,
                directions=directions,
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Готово: создано {created_projects} проектов и "
                f"{created_groups} учебных групп для {INSTITUTE_CODE} "
                f"(семестр: {semester.code}, id={semester.pk})."
            )
        )

    def _get_institute(self) -> Institute:
        try:
            return Institute.objects.get(code=INSTITUTE_CODE)
        except Institute.DoesNotExist as exc:
            raise CommandError(
                f"Институт {INSTITUTE_CODE} не найден. "
                "Сначала выполните: python manage.py import_institutes"
            ) from exc

    def _resolve_semester(self, semester_id: int | None) -> Semester:
        if semester_id is not None:
            semester = Semester.objects.filter(pk=semester_id).first()
            if semester is None:
                raise CommandError(f"Семестр с id={semester_id} не найден")
            return semester

        semester = Semester.get_active()
        if semester is not None:
            return semester

        semester = Semester.objects.order_by("-position").first()
        if semester is None:
            raise CommandError(
                "Семестры не найдены. Создайте семестр или передайте --semester-id"
            )
        self.stdout.write(
            self.style.WARNING(
                f"Активный семестр не настроен, используется: {semester.code}"
            )
        )
        return semester

    def _get_approved_status(self) -> ApplicationStatus:
        try:
            return ApplicationStatus.objects.get(code="approved")
        except ApplicationStatus.DoesNotExist as exc:
            raise CommandError(
                "Статус approved не найден. Сначала выполните: python manage.py import_statuses"
            ) from exc

    def _get_directions(self) -> list[Direction]:
        directions = list(Direction.objects.filter(code__in=IEF_DIRECTION_CODES))
        found_codes = {direction.code for direction in directions}
        missing = [code for code in IEF_DIRECTION_CODES if code not in found_codes]
        if missing:
            raise CommandError(
                "Не найдены направления: "
                f"{', '.join(missing)}. Сначала выполните: python manage.py import_directions"
            )
        return directions

    def _clear_generated_data(self) -> None:
        deleted_projects, _ = ProjectApplication.objects.filter(
            print_number__startswith=f"{TEST_APPLICATION_YEAR % 100:02d}-gen-"
        ).delete()
        deleted_groups, _ = StudyGroup.objects.filter(
            code__startswith=GROUP_CODE_PREFIX
        ).delete()
        self.stdout.write(
            f"Удалено: {deleted_projects} проектов, {deleted_groups} учебных групп"
        )

    def _create_projects(
        self,
        *,
        count: int,
        institute: Institute,
        semester: Semester,
        approved_status: ApplicationStatus,
        tags: Sequence[Tag],
    ) -> int:
        year_short = TEST_APPLICATION_YEAR % 100
        start_sequence = (
            ProjectApplication.objects.filter(
                application_year=TEST_APPLICATION_YEAR
            ).aggregate(max_seq=models.Max("year_sequence_number"))["max_seq"]
            or 0
        )

        created = 0
        for index in range(1, count + 1):
            sequence_number = start_sequence + index
            print_number = f"{year_short}-gen-{sequence_number:05d}"
            if ProjectApplication.objects.filter(print_number=print_number).exists():
                continue

            application = ProjectApplication.objects.create(
                title=f"{PROJECT_TITLE_PREFIX} {index:03d}",
                company=COMPANIES[(index - 1) % len(COMPANIES)],
                author_lastname="Тестов",
                author_firstname=f"Автор{index:03d}",
                author_email=f"ief.test.author{index:03d}@example.com",
                author_phone="+7-900-000-00-00",
                semester=semester,
                status=approved_status,
                application_year=TEST_APPLICATION_YEAR,
                year_sequence_number=sequence_number,
                print_number=print_number,
                project_level="local",
                problem_holder=f"Носитель проблемы #{index}",
                goal=(
                    f"Цель тестового проекта {index}: разработка решения "
                    "для демонстрации функционала витрины проектов."
                ),
                barrier=(
                    f"Барьер тестового проекта {index}: недостаток данных "
                    "и ограниченные ресурсы для пилотного внедрения."
                ),
                existing_solutions="Существующие решения на рынке не покрывают потребности полностью.",
            )
            application.target_institutes.add(institute)

            tag_count = random.randint(1, min(3, len(tags)))
            selected_tags = random.sample(tags, k=tag_count)
            application.tags.set(selected_tags)

            created += 1
            if created % 25 == 0:
                self.stdout.write(f"  проектов создано: {created}/{count}")

        return created

    def _create_study_groups(
        self,
        *,
        count: int,
        institute: Institute,
        directions: Sequence[Direction],
    ) -> int:
        courses = (1, 2, 3, 4)
        direction_cycle = itertools.cycle(directions)
        created = 0

        for index in range(1, count + 1):
            code = f"{GROUP_CODE_PREFIX}{index:04d}"
            if StudyGroup.objects.filter(code=code).exists():
                continue

            direction = next(direction_cycle)
            course_number = courses[(index - 1) % len(courses)]
            direction_suffix = direction.code.replace(".", "")

            StudyGroup.objects.create(
                name=f"{GROUP_NAME_PREFIX}-{direction_suffix}-{course_number}{index % 100:02d}",
                code=code,
                direction=direction,
                institute=institute,
                course_number=course_number,
                is_end=False,
            )
            created += 1

        return created

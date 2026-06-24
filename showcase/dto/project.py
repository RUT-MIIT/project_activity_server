"""DTO для списка проектов."""

from typing import Any

from accounts.models import Department
from accounts.utils import get_root_department
from showcase.models import ProjectApplication


class ProjectListDTO:
    """DTO для списка проектов."""

    def __init__(self, application: ProjectApplication):
        self.id = application.id
        self.title = application.title or ""
        self.company = application.company
        self.author_name = (
            f"{application.author_lastname} {application.author_firstname}".strip()
        )
        self.author_email = application.author_email
        self.tags = [{"id": tag.id, "name": tag.name} for tag in application.tags.all()]
        self.print_number = application.print_number or ""
        self.img = ""
        self.status = self._status_dict(application)
        self.main_department = self._top_level_involved_department_dict(application)
        self.author = self._author_dict(application)
        self.creation_date = application.creation_date

    @staticmethod
    def _status_dict(application: ProjectApplication) -> dict[str, str] | None:
        status = getattr(application, "status", None)
        if not status:
            return None
        return {"code": status.code, "name": status.name}

    @staticmethod
    def _top_level_involved_department(
        application: ProjectApplication,
    ) -> Department | None:
        """Возвращает причастное подразделение верхнего уровня (без родителя)."""
        for involved in application.involved_departments.all():
            department = involved.department
            if department.parent is None:
                return department

        for involved in application.involved_departments.all():
            root = get_root_department(involved.department)
            if root is not None:
                return root

        return None

    @staticmethod
    def _top_level_involved_department_dict(
        application: ProjectApplication,
    ) -> dict[str, Any] | None:
        department = ProjectListDTO._top_level_involved_department(application)
        if not department:
            return None
        return {
            "id": department.id,
            "name": department.name,
            "short_name": department.short_name,
        }

    @staticmethod
    def _author_dict(application: ProjectApplication) -> dict[str, Any] | None:
        author = getattr(application, "author", None)
        if author is not None:
            return {
                "id": author.id,
                "full_name": author.get_full_name(),
                "email": author.email,
            }
        if application.author_lastname or application.author_firstname:
            return {
                "id": None,
                "full_name": (
                    f"{application.author_lastname} {application.author_firstname}"
                ).strip(),
                "email": application.author_email or "",
            }
        return None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "company": self.company,
            "author_name": self.author_name,
            "author_email": self.author_email,
            "tags": self.tags,
            "print_number": self.print_number,
            "img": self.img,
            "status": self.status,
            "main_department": self.main_department,
            "author": self.author,
            "creation_date": self.creation_date.isoformat(),
        }

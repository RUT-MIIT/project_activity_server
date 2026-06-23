"""DTO для списка пользователей."""

from __future__ import annotations

from typing import Any

from accounts.models import User


class UserListDTO:
    """DTO для элемента списка пользователей."""

    def __init__(self, user: User, *, include_authored_projects: bool = False):
        self.id = user.id
        self.full_name = user.get_full_name()
        self.email = user.email
        self.phone = user.phone or ""
        self.role = self._role_dict(user)
        self.department = self._department_dict(user)
        self.authored_projects_count = getattr(user, "authored_projects_count", 0)
        self._include_authored_projects = include_authored_projects
        self._user = user

    @staticmethod
    def _role_dict(user: User) -> dict[str, str] | None:
        if not user.role:
            return None
        return {"code": user.role.code, "name": user.role.name}

    @staticmethod
    def _department_dict(user: User) -> dict[str, Any] | None:
        department = getattr(user, "department", None)
        if not department:
            return None
        return {
            "id": department.id,
            "name": department.name,
            "short_name": department.short_name,
        }

    def _authored_projects_list(self) -> list[dict[str, Any]]:
        projects = getattr(self._user, "prefetched_authored_projects", None)
        if projects is None:
            return []

        result = []
        for project in projects:
            status = project.status
            result.append(
                {
                    "id": project.id,
                    "title": project.title or "",
                    "status": (
                        {
                            "code": status.code,
                            "name": status.name,
                        }
                        if status
                        else None
                    ),
                }
            )
        return result

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "role": self.role,
            "department": self.department,
            "authored_projects_count": self.authored_projects_count,
        }
        if self._include_authored_projects:
            data["authored_projects"] = self._authored_projects_list()
        return data

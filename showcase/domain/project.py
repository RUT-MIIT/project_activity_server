"""Доменная логика для списка проектов."""

from accounts.models import User
from teams.domain.institute_access import get_accessible_institute_codes, get_role_code


class ProjectDomain:
    """Правила доступа и фильтрации для списка проектов."""

    LIST_ROLES = frozenset({"admin", "cpds", "institute_validator"})

    @staticmethod
    def can_list_projects(user: User) -> tuple[bool, str]:
        """Проверяет, может ли пользователь получать список проектов."""
        if not user or not user.is_authenticated:
            return False, "Требуется авторизация"

        if user.is_staff:
            return True, ""

        role_code = get_role_code(user)
        if role_code in ProjectDomain.LIST_ROLES:
            return True, ""

        return False, "Недостаточно прав для просмотра проектов"

    @staticmethod
    def get_institute_codes_for_user(user: User) -> list[str] | None:
        """Коды институтов для фильтрации; None — без ограничения."""
        return get_accessible_institute_codes(user)

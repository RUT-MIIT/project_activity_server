"""Доменная логика для проектных заявок - чистые функции без эффектов."""

from showcase.dto.application import (
    ProjectApplicationCreateDTO,
    ProjectApplicationUpdateDTO,
)
from showcase.dto.validation import ValidationResult


class ProjectApplicationDomain:
    """Чистая бизнес-логика - только функции, никаких эффектов"""

    @staticmethod
    def validate_create(dto: ProjectApplicationCreateDTO) -> ValidationResult:
        """Валидация бизнес-правил для создания заявки.

        Чистая функция - принимает данные, возвращает результат валидации.
        Никаких обращений к БД, файлам, сети.

        ВАЖНО: Техническая валидация (типы, форматы, обязательные поля)
        выполняется в сериализаторе DRF. Здесь только бизнес-правила.
        """
        result = ValidationResult()

        # Бизнес-правило: название проекта обязательно и минимум 5 символов
        if not dto.title or not dto.title.strip():
            result.add_error("title", "Название проекта обязательно")
        elif len(dto.title.strip()) < 5:
            result.add_error(
                "title", "Название проекта должно содержать минимум 5 символов"
            )

        # Бизнес-правило: наименование организации-заказчика обязательно и минимум 2 символа
        if not dto.company or not dto.company.strip():
            result.add_error(
                "company", "Наименование организации-заказчика обязательно"
            )
        elif len(dto.company.strip()) < 2:
            result.add_error(
                "company",
                "Наименование организации-заказчика должно содержать минимум 2 символа",
            )

        # Бизнес-правило: цель проекта обязательна и минимум 10 символов
        if not dto.goal or not dto.goal.strip():
            result.add_error("goal", "Цель обязательна")
        elif len(dto.goal.strip()) < 10:
            result.add_error("goal", "Цель должна содержать минимум 10 символов")

        # Бизнес-правило: носитель проблемы и барьер могут быть пустыми на черновых шагах.
        # Проверяем только при наличии значения.
        if dto.problem_holder not in (None, ""):
            if len(dto.problem_holder.strip()) < 5:
                result.add_error(
                    "problem_holder",
                    "Носитель проблемы должен содержать минимум 5 символов",
                )

        if dto.barrier not in (None, ""):
            if len(dto.barrier.strip()) < 10:
                result.add_error(
                    "barrier",
                    "Барьер должен содержать минимум 10 символов",
                )

        # Бизнес-правило: существующие решения и контакты заказчика допускаются пустыми
        # для упрощённой подачи. Валидируем только если переданы непустые строки.
        if dto.existing_solutions not in (None, ""):
            if not dto.existing_solutions.strip():
                result.add_error(
                    "existing_solutions", "Существующие решения обязательны"
                )

        if dto.company_contacts not in (None, ""):
            if not dto.company_contacts.strip():
                result.add_error(
                    "company_contacts",
                    "Контактные данные представителя заказчика обязательны",
                )

        # Бизнес-правило: email автора, если задан, должен быть достаточно длинным
        # (подробная проверка формата выполняется на уровне сериализатора)
        if dto.author_email is not None:
            if not dto.author_email or len(dto.author_email.strip()) < 5:
                result.add_error(
                    "author_email", "Email автора должен содержать минимум 5 символов"
                )

        if dto.author_lastname is not None:
            if not dto.author_lastname or not dto.author_lastname.strip():
                result.add_error("author_lastname", "Фамилия автора обязательна")
            elif len(dto.author_lastname.strip()) < 2:
                result.add_error(
                    "author_lastname",
                    "Фамилия автора должна содержать минимум 2 символа",
                )

        if dto.author_firstname is not None:
            if not dto.author_firstname or not dto.author_firstname.strip():
                result.add_error("author_firstname", "Имя автора обязательно")
            elif len(dto.author_firstname.strip()) < 2:
                result.add_error(
                    "author_firstname",
                    "Имя автора должно содержать минимум 2 символа",
                )

        if dto.author_phone is not None:
            if not dto.author_phone or not dto.author_phone.strip():
                result.add_error("author_phone", "Телефон автора обязателен")
            elif len(dto.author_phone.strip()) < 10:
                result.add_error(
                    "author_phone",
                    "Телефон автора должен содержать минимум 10 символов",
                )

        return result

    @staticmethod
    def validate_update(dto: ProjectApplicationUpdateDTO) -> ValidationResult:
        """Валидация бизнес-правил для обновления заявки.

        Чистая функция - проверяет только переданные поля.
        """
        result = ValidationResult()

        # Валидируем только переданные поля
        if dto.title is not None:
            if not dto.title or not dto.title.strip():
                result.add_error("title", "Название проекта обязательно")
            elif len(dto.title.strip()) < 5:
                result.add_error(
                    "title",
                    "Название проекта должно содержать минимум 5 символов",
                )

        if dto.author_email is not None and (
            not dto.author_email or "@" not in dto.author_email
        ):
            result.add_error("author_email", "Некорректный email")

        if dto.goal is not None:
            if not dto.goal or not dto.goal.strip():
                result.add_error("goal", "Цель обязательна")

        if dto.problem_holder is not None:
            if not dto.problem_holder or not dto.problem_holder.strip():
                result.add_error("problem_holder", "Носитель проблемы обязателен")

        if dto.barrier is not None:
            if not dto.barrier or not dto.barrier.strip():
                result.add_error("barrier", "Барьер обязателен")

        if dto.company is not None:
            if not dto.company or not dto.company.strip():
                result.add_error(
                    "company", "Наименование организации-заказчика обязательно"
                )

        if dto.author_lastname is not None:
            if not dto.author_lastname or not dto.author_lastname.strip():
                result.add_error("author_lastname", "Фамилия автора обязательна")

        if dto.author_firstname is not None:
            if not dto.author_firstname or not dto.author_firstname.strip():
                result.add_error("author_firstname", "Имя автора обязательно")

        if dto.author_phone is not None:
            if not dto.author_phone or not dto.author_phone.strip():
                result.add_error("author_phone", "Телефон автора обязателен")

        return result

    @staticmethod
    def calculate_initial_status(user_role: str) -> str:
        """Определение начального статуса на основе роли пользователя.

        Чистая функция - принимает роль, возвращает статус.
        """
        # Бизнес-правило: админы и CPDS сразу создают одобренные заявки
        if user_role in ["admin", "cpds"]:
            return "approved"

        # Бизнес-правило: валидаторы подразделений создают заявки в статусе "ожидает института"
        if user_role == "department_validator":
            return "await_institute"

        # Бизнес-правило: валидаторы институтов создают заявки в статусе "ожидает CPDS"
        if user_role == "institute_validator":
            return "await_cpds"

        # Бизнес-правило: в ином случае - "ожидает подразделения"
        return "await_department"

    @staticmethod
    def can_change_status(
        current_status: str, new_status: str, user_role: str
    ) -> tuple[bool, str]:
        """Проверка возможности изменения статуса.

        Чистая функция - принимает параметры, возвращает решение.
        """
        # Бизнес-правило: только определенные переходы разрешены
        allowed_transitions = {
            "created": [
                "await_department",
                "rejected",
                "rejected_department",
                "returned_author",
            ],
            "await_department": [
                "approved_department",
                "rejected",
                "rejected_department",
                "returned_department",
                "returned_institute",
                "returned_author",
            ],
            "await_institute": [
                "approved_institute",
                "rejected",
                "rejected_institute",
                "returned_institute",
                "returned_author",
            ],
            "await_cpds": [
                "approved",
                "rejected",
                "rejected_cpds",
                "returned_cpds",
                "await_institute",
                "returned_author",
            ],
            "require_assignment": [
                "await_institute",
                "returned_author",
            ],
            "returned_department": [
                "await_department",
                "returned_department",
                "rejected_department",
                "approved_department",
                "rejected_department",
                "returned_author",
            ],
            "returned_institute": [
                "await_department",
                "await_institute",
                "returned_institute",
                "approved_department",
                "approved_institute",
                "rejected_department",
                "returned_author",
            ],
            "returned_cpds": [
                "await_cpds",
                "await_institute",
                "await_department",
                "returned_cpds",
                "approved",
                "approved_department",
                "approved_institute",
                "rejected_department",
                "rejected_institute",
                "rejected_cpds",
                "returned_author",
            ],
            "returned_author": [
                "await_department",
                "await_institute",
                "await_cpds",
                "require_assignment",
            ],
            "approved_department": ["await_institute", "rejected"],
            "approved_institute": ["await_cpds", "rejected"],
            "approved": ["rejected"],
            "rejected": ["created"],
            "rejected_department": ["rejected", "created"],
            "rejected_institute": ["rejected", "created"],
            "rejected_cpds": ["rejected", "created"],
        }

        if new_status not in allowed_transitions.get(current_status, []):
            return False, f"Переход {current_status} → {new_status} запрещен"

        # Бизнес-правило: только админы могут отклонять одобренные заявки
        if (
            current_status == "approved"
            and new_status == "rejected"
            and user_role != "admin"
        ):
            return False, "Только администратор может отклонять одобренные заявки"

        return True, ""

    @staticmethod
    def can_user_access_application(
        user_role: str, application_author_id: int, user_id: int
    ) -> bool:
        """Проверка доступа пользователя к заявке.

        Чистая функция - принимает параметры, возвращает решение.
        """
        # Бизнес-правило: автор всегда имеет доступ
        if application_author_id == user_id:
            return True

        # Бизнес-правило: админы, модераторы и валидаторы имеют доступ ко всем заявкам
        if user_role in [
            "admin",
            "moderator",
            "cpds",
            "department_validator",
            "institute_validator",
        ]:
            return True

        # Бизнес-правило: обычные пользователи видят только свои заявки
        return False

    @staticmethod
    def should_require_consultation(dto: ProjectApplicationCreateDTO) -> bool:
        """Определение необходимости консультации на основе данных заявки.

        Чистая функция - принимает данные, возвращает решение.
        """
        # Бизнес-правило: если не указан уровень проекта, нужна консультация
        if not dto.project_level or dto.project_level.strip() == "":
            return True

        # Бизнес-правило: если не указаны целевые институты, нужна консультация
        if not dto.target_institutes or len(dto.target_institutes) == 0:
            return True

        # Бизнес-правило: если цель проекта слишком короткая, нужна консультация
        if len(dto.goal.strip()) < 50:
            return True

        return False

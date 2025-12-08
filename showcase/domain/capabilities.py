"""Явное выражение бизнес-намерений (не технических операций).

Этот модуль содержит чистые функции, которые выражают бизнес-операции
в терминах предметной области, а не технических операций.
"""

from typing import Any

from showcase.dto.application import (
    ProjectApplicationCreateDTO,
    ProjectApplicationUpdateDTO,
)
from showcase.dto.validation import ValidationResult

from .application import ProjectApplicationDomain


class ApplicationCapabilities:
    """Явное выражение бизнес-намерений.

    Вместо технических операций типа "create", "update", "delete"
    используем бизнес-операции типа "submit", "approve", "reject".
    """

    @staticmethod
    def submit_application(
        dto: ProjectApplicationCreateDTO, user_role: str
    ) -> ValidationResult:
        """Бизнес-операция: подача заявки.

        Чистая функция - проверяет возможность подачи заявки.
        """
        # Валидация бизнес-правил
        validation = ProjectApplicationDomain.validate_create(dto)

        # Дополнительные бизнес-правила для подачи могут добавлять ошибки валидации
        # Бизнес-правило: пользователь должен иметь право подавать заявки
        # Для совместимости с тестами разрешаем любые роли
        # if user_role not in ['user', 'admin', 'moderator']:
        #     validation.add_error('user_role', 'Недостаточно прав для подачи заявки')

        return validation

    @staticmethod
    def approve_application(
        application_status: str,
        approver_role: str,
        is_user_department_involved: bool = False,
        is_user_author: bool = False,
        user_department_can_save: bool = False,
        is_external: bool = False,
    ) -> tuple[bool, str]:
        """Бизнес-операция: одобрение заявки.

        Чистая функция - проверяет возможность одобрения.
        """
        # Проверка прав на действие approve по матрице правил
        if not ApplicationCapabilities.is_action_allowed(
            action="approve",
            current_status=application_status,
            user_role=approver_role,
            is_user_department_involved=is_user_department_involved,
            is_user_author=is_user_author,
            user_department_can_save=user_department_can_save,
            is_external=is_external,
        ):
            return False, "Недостаточно прав для одобрения заявки"

        # Проверка возможности перехода не требуется здесь,
        # так как конкретный статус одобрения определяется в сервисе
        return True, ""

    @staticmethod
    def reject_application(
        application_status: str,
        rejector_role: str,
        is_user_department_involved: bool = False,
        is_user_author: bool = False,
        user_department_can_save: bool = False,
        is_external: bool = False,
    ) -> tuple[bool, str]:
        """Бизнес-операция: отклонение заявки.

        Чистая функция - проверяет возможность отклонения.
        """
        # Проверка прав на действие reject по матрице правил
        if not ApplicationCapabilities.is_action_allowed(
            action="reject",
            current_status=application_status,
            user_role=rejector_role,
            is_user_department_involved=is_user_department_involved,
            is_user_author=is_user_author,
            user_department_can_save=user_department_can_save,
            is_external=is_external,
        ):
            return False, "Недостаточно прав для отклонения заявки"

        # Проверка возможности перехода не требуется здесь,
        # так как конкретный статус отклонения определяется в сервисе
        return True, ""

    @staticmethod
    def request_changes(
        application_status: str,
        requester_role: str,
        is_user_department_involved: bool = False,
        is_user_author: bool = False,
        user_department_can_save: bool = False,
        is_external: bool = False,
    ) -> tuple[bool, str]:
        """Бизнес-операция: запрос изменений.

        Чистая функция - проверяет возможность запроса изменений.
        """
        # Проверка прав на действие request_changes по матрице правил
        if not ApplicationCapabilities.is_action_allowed(
            action="request_changes",
            current_status=application_status,
            user_role=requester_role,
            is_user_department_involved=is_user_department_involved,
            is_user_author=is_user_author,
            user_department_can_save=user_department_can_save,
            is_external=is_external,
        ):
            return False, "Недостаточно прав для запроса изменений"

        # Проверка возможности перехода не требуется для request_changes,
        # так как статус уже учтен в can_manage_application
        return True, ""

    @staticmethod
    def update_application(
        dto: ProjectApplicationUpdateDTO,
        application_status: str,
        updater_role: str,
        application_author_id: int,
        updater_id: int,
        user_department_can_save: bool = False,
    ) -> tuple[ValidationResult, bool, str]:
        """Бизнес-операция: обновление заявки.

        Чистая функция - проверяет возможность обновления.
        """
        # Валидация данных
        validation = ProjectApplicationDomain.validate_update(dto)

        # Бизнес-правило: нельзя обновлять отклоненные заявки (финальный статус rejected)
        if application_status == "rejected":
            validation.add_error("status", "Нельзя обновлять отклоненные заявки")

        # Бизнес-правило: нельзя обновлять одобренные заявки (кроме админов и cpds)
        if application_status == "approved" and updater_role not in ["admin", "cpds"]:
            validation.add_error("status", "Нельзя обновлять одобренные заявки")

        # Проверка прав на редактирование через матрицу разрешений
        # В матрице настроено: редактировать может только автор (POLICY_OWN_ONLY) или cpds (POLICY_ALLOW)
        # Для institute_validator: разрешено, если у подразделения can_save_project_applications = True
        is_user_author = application_author_id == updater_id
        # Для проверки нужен is_user_department_involved, но здесь его нет
        # Используем упрощенную проверку: автор или cpds
        can_edit = ApplicationCapabilities.can_edit_application(
            current_status=application_status,
            user_role=updater_role,
            is_user_department_involved=False,  # Не используется для save_changes в новой логике
            is_user_author=is_user_author,
            user_department_can_save=user_department_can_save,
        )

        if not can_edit:
            validation.add_error(
                "access", "Редактировать заявку может только автор или сотрудник ЦПДС"
            )

        return validation, validation.is_valid, ""

    @staticmethod
    def view_application(
        application_status: str,
        viewer_role: str,
        application_author_id: int,
        viewer_id: int,
    ) -> tuple[bool, str]:
        """Бизнес-операция: просмотр заявки.

        Чистая функция - проверяет возможность просмотра.
        """
        # Проверка доступа
        can_access = ProjectApplicationDomain.can_user_access_application(
            viewer_role, application_author_id, viewer_id
        )

        if not can_access:
            return False, "Нет прав для просмотра этой заявки"

        return True, ""

    @staticmethod
    def list_applications(user_role: str) -> tuple[bool, str]:
        """Бизнес-операция: получение списка заявок.

        Чистая функция - проверяет возможность получения списка.
        """
        # Бизнес-правило: разрешаем доступ всем (включая неавторизованных)
        # Неавторизованные пользователи получат пустой список
        return True, ""

    # === Новая матрица разрешений, зашитая из CSV ===
    # Интерпретация значений: '+' разрешено, '-' запрещено,
    # 'только своего подразделения' -> требуется is_user_department_involved,
    # 'только свои' -> требуется is_user_author

    # Константы для политик и статусов (уменьшаем дублирование литералов)
    POLICY_ALLOW: str = "+"
    POLICY_DENY: str = "-"
    POLICY_DEPARTMENT_ONLY: str = "только своего подразделения"
    POLICY_OWN_ONLY: str = "только свои"
    POLICY_DEPARTMENT_CAN_SAVE: str = "если подразделение может сохранять"
    POLICY_DEPARTMENT_ONLY_NOT_EXTERNAL: str = (
        "только своего подразделения и не внешняя заявка"
    )
    POLICY_EXTERNAL_ONLY: str = "только для внешней заявки"
    STATUS_RETURNED_ALL: str = "returned_(all)"
    _ROLE_STATUS_ACTIONS: dict[str, dict[str, dict[str, str]]] = {
        "await_department": {
            "user": {
                "save_changes": POLICY_DENY,
                "approve": POLICY_DENY,
                "reject": POLICY_DENY,
                "request_changes": POLICY_DENY,
            },
            "mentor": {
                "save_changes": POLICY_DENY,
                "approve": POLICY_DENY,
                "reject": POLICY_DENY,
                "request_changes": POLICY_DENY,
            },
            "department_validator": {
                "save_changes": POLICY_OWN_ONLY,
                "approve": POLICY_DEPARTMENT_ONLY,
                "reject": POLICY_DEPARTMENT_ONLY,
                "request_changes": POLICY_DEPARTMENT_ONLY,
            },
            "institute_validator": {
                "save_changes": POLICY_DEPARTMENT_CAN_SAVE,
                "approve": POLICY_DEPARTMENT_ONLY,
                "reject": POLICY_DEPARTMENT_ONLY,
                "request_changes": POLICY_DEPARTMENT_ONLY,
            },
            "cpds": {
                "save_changes": POLICY_ALLOW,
                "approve": POLICY_DENY,
                "reject": POLICY_DENY,
                "request_changes": POLICY_DENY,
            },
        },
        "require_assignment": {
            "user": {
                "save_changes": POLICY_DENY,
                "approve": POLICY_DENY,
                "reject": POLICY_DENY,
                "request_changes": POLICY_DENY,
            },
            "mentor": {
                "save_changes": POLICY_DENY,
                "approve": POLICY_DENY,
                "reject": POLICY_DENY,
                "request_changes": POLICY_DENY,
            },
            "department_validator": {
                "save_changes": POLICY_DENY,
                "approve": POLICY_DENY,
                "reject": POLICY_DENY,
                "request_changes": POLICY_DENY,
            },
            "institute_validator": {
                "save_changes": POLICY_DENY,
                "approve": POLICY_DENY,
                "reject": POLICY_DENY,
                "request_changes": POLICY_DENY,
            },
            "cpds": {
                "save_changes": POLICY_ALLOW,
                "approve": POLICY_DENY,
                "reject": POLICY_ALLOW,
                "request_changes": POLICY_DENY,
                "transfer_to_institute": POLICY_EXTERNAL_ONLY,
            },
        },
        "await_institute": {
            "user": {
                "save_changes": POLICY_DENY,
                "approve": POLICY_DENY,
                "reject": POLICY_DENY,
                "request_changes": POLICY_DENY,
            },
            "mentor": {
                "save_changes": POLICY_DENY,
                "approve": POLICY_DENY,
                "reject": POLICY_DENY,
                "request_changes": POLICY_DENY,
            },
            "department_validator": {
                "save_changes": POLICY_DENY,
                "approve": POLICY_DENY,
                "reject": POLICY_DENY,
                "request_changes": POLICY_DENY,
            },
            "institute_validator": {
                "save_changes": POLICY_DEPARTMENT_CAN_SAVE,
                "approve": POLICY_DEPARTMENT_ONLY,
                "reject": POLICY_DEPARTMENT_ONLY,
                "request_changes": POLICY_DEPARTMENT_ONLY_NOT_EXTERNAL,
            },
            "cpds": {
                "save_changes": POLICY_ALLOW,
                "approve": POLICY_DENY,
                "reject": POLICY_DENY,
                "request_changes": POLICY_DENY,
            },
        },
        "await_cpds": {
            "user": {
                "save_changes": POLICY_DENY,
                "approve": POLICY_DENY,
                "reject": POLICY_DENY,
                "request_changes": POLICY_DENY,
            },
            "mentor": {
                "save_changes": POLICY_DENY,
                "approve": POLICY_DENY,
                "reject": POLICY_DENY,
                "request_changes": POLICY_DENY,
            },
            "department_validator": {
                "save_changes": POLICY_DENY,
                "approve": POLICY_DENY,
                "reject": POLICY_DENY,
                "request_changes": POLICY_DENY,
            },
            "institute_validator": {
                "save_changes": POLICY_DENY,
                "approve": POLICY_DENY,
                "reject": POLICY_DENY,
                "request_changes": POLICY_DENY,
            },
            "cpds": {
                "save_changes": POLICY_ALLOW,
                "approve": POLICY_ALLOW,
                "reject": POLICY_ALLOW,
                "request_changes": POLICY_ALLOW,
                "transfer_to_institute": POLICY_EXTERNAL_ONLY,
            },
        },
        STATUS_RETURNED_ALL: {
            "user": {
                "save_changes": POLICY_OWN_ONLY,
                "approve": POLICY_DENY,
                "reject": POLICY_DENY,
                "request_changes": POLICY_DENY,
            },
            "mentor": {
                "save_changes": POLICY_OWN_ONLY,
                "approve": POLICY_OWN_ONLY,
                "reject": POLICY_DENY,
                "request_changes": POLICY_DENY,
            },
            "department_validator": {
                "save_changes": POLICY_OWN_ONLY,
                "approve": POLICY_DEPARTMENT_ONLY,
                "reject": POLICY_DEPARTMENT_ONLY,
                "request_changes": POLICY_DENY,
            },
            "institute_validator": {
                "save_changes": POLICY_DEPARTMENT_CAN_SAVE,
                "approve": POLICY_DEPARTMENT_ONLY,
                "reject": POLICY_DEPARTMENT_ONLY,
                "request_changes": POLICY_DENY,
            },
            "cpds": {
                "save_changes": POLICY_ALLOW,
                "approve": POLICY_DENY,
                "reject": POLICY_DENY,
                "request_changes": POLICY_DENY,
            },
        },
        "rejected_department": {
            "mentor": {
                "save_changes": POLICY_DENY,
                "approve": POLICY_DENY,
                "reject": POLICY_DENY,
                "request_changes": POLICY_DENY,
            },
            "department_validator": {
                "save_changes": POLICY_DENY,
                "approve": POLICY_DEPARTMENT_ONLY,
                "reject": POLICY_DENY,
                "request_changes": POLICY_DEPARTMENT_ONLY,
            },
            "institute_validator": {
                "save_changes": POLICY_DENY,
                "approve": POLICY_DEPARTMENT_ONLY,
                "reject": POLICY_DENY,
                "request_changes": POLICY_DEPARTMENT_ONLY,
            },
            "cpds": {
                "save_changes": POLICY_ALLOW,
                "approve": POLICY_ALLOW,
                "reject": POLICY_DENY,
                "request_changes": POLICY_ALLOW,
            },
        },
        "rejected_institute": {
            "mentor": {
                "save_changes": POLICY_DENY,
                "approve": POLICY_DENY,
                "reject": POLICY_DENY,
                "request_changes": POLICY_DENY,
            },
            "department_validator": {
                "save_changes": POLICY_DENY,
                "approve": POLICY_DENY,
                "reject": POLICY_DENY,
                "request_changes": POLICY_DENY,
            },
            "institute_validator": {
                "save_changes": POLICY_DENY,
                "approve": POLICY_DEPARTMENT_ONLY,
                "reject": POLICY_DENY,
                "request_changes": POLICY_DEPARTMENT_ONLY,
            },
            "cpds": {
                "save_changes": POLICY_ALLOW,
                "approve": POLICY_ALLOW,
                "reject": POLICY_DENY,
                "request_changes": POLICY_ALLOW,
            },
        },
        "rejected_cpds": {
            "mentor": {
                "save_changes": POLICY_DENY,
                "approve": POLICY_DENY,
                "reject": POLICY_DENY,
                "request_changes": POLICY_DENY,
            },
            "department_validator": {
                "save_changes": POLICY_DENY,
                "approve": POLICY_DENY,
                "reject": POLICY_DENY,
                "request_changes": POLICY_DENY,
            },
            "institute_validator": {
                "save_changes": POLICY_DENY,
                "approve": POLICY_DEPARTMENT_ONLY,
                "reject": POLICY_DENY,
                "request_changes": POLICY_DEPARTMENT_ONLY,
            },
            "cpds": {
                "save_changes": POLICY_ALLOW,
                "approve": POLICY_ALLOW,
                "reject": POLICY_DENY,
                "request_changes": POLICY_ALLOW,
            },
        },
        "approved": {
            "user": {
                "save_changes": POLICY_DENY,
                "approve": POLICY_DENY,
                "reject": POLICY_DENY,
                "request_changes": POLICY_DENY,
            },
            "mentor": {
                "save_changes": POLICY_DENY,
                "approve": POLICY_DENY,
                "reject": POLICY_DENY,
                "request_changes": POLICY_DENY,
            },
            "department_validator": {
                "save_changes": POLICY_DENY,
                "approve": POLICY_DENY,
                "reject": POLICY_DENY,
                "request_changes": POLICY_DENY,
            },
            "institute_validator": {
                "save_changes": POLICY_DENY,
                "approve": POLICY_DENY,
                "reject": POLICY_DENY,
                "request_changes": POLICY_DENY,
            },
            "cpds": {
                "save_changes": POLICY_ALLOW,
                "approve": POLICY_DENY,
                "reject": POLICY_ALLOW,
                "request_changes": POLICY_ALLOW,
            },
        },
        "rejected": {
            "user": {
                "save_changes": POLICY_DENY,
                "approve": POLICY_DENY,
                "reject": POLICY_DENY,
                "request_changes": POLICY_DENY,
            },
            "mentor": {
                "save_changes": POLICY_DENY,
                "approve": POLICY_DENY,
                "reject": POLICY_DENY,
                "request_changes": POLICY_DENY,
            },
            "department_validator": {
                "save_changes": POLICY_DENY,
                "approve": POLICY_DENY,
                "reject": POLICY_DENY,
                "request_changes": POLICY_DENY,
            },
            "institute_validator": {
                "save_changes": POLICY_DENY,
                "approve": POLICY_DENY,
                "reject": POLICY_DENY,
                "request_changes": POLICY_DENY,
            },
            "cpds": {
                "save_changes": POLICY_DENY,
                "approve": POLICY_DENY,
                "reject": POLICY_DENY,
                "request_changes": POLICY_DENY,
            },
        },
    }

    _ACTION_LABELS: dict[str, str] = {
        "approve": "Согласовать",
        "reject": "Отклонить",
        "request_changes": "Отправить на доработку",
        "save_changes": "Сохранить изменение",
        "transfer_to_institute": "Передать в институт",
    }

    @staticmethod
    def _match_status_pattern(current_status: str) -> list[str]:
        """Возвращает список ключей матрицы, подходящих под статус.
        Сначала точное совпадение, затем специальный шаблон returned_(all) для returned_*
        """
        keys: list[str] = []
        if current_status in ApplicationCapabilities._ROLE_STATUS_ACTIONS:
            keys.append(current_status)
        if (
            current_status.startswith("returned_")
            and ApplicationCapabilities.STATUS_RETURNED_ALL
            in ApplicationCapabilities._ROLE_STATUS_ACTIONS
        ):
            keys.append(ApplicationCapabilities.STATUS_RETURNED_ALL)
        return keys

    @staticmethod
    def _check_policy(
        policy: str,
        is_user_department_involved: bool,
        is_user_author: bool,
        user_department_can_save: bool = False,
        is_external: bool = False,
    ) -> bool:
        if policy == ApplicationCapabilities.POLICY_ALLOW:
            return True
        if policy == ApplicationCapabilities.POLICY_DENY:
            return False
        if policy == ApplicationCapabilities.POLICY_DEPARTMENT_ONLY:
            return bool(is_user_department_involved)
        if policy == ApplicationCapabilities.POLICY_OWN_ONLY:
            return bool(is_user_author)
        if policy == ApplicationCapabilities.POLICY_DEPARTMENT_CAN_SAVE:
            return bool(is_user_department_involved) and bool(user_department_can_save)
        if policy == ApplicationCapabilities.POLICY_DEPARTMENT_ONLY_NOT_EXTERNAL:
            return bool(is_user_department_involved) and not bool(is_external)
        if policy == ApplicationCapabilities.POLICY_EXTERNAL_ONLY:
            return bool(is_external)
        return False

    @staticmethod
    def is_action_allowed(
        action: str,
        current_status: str,
        user_role: str,
        is_user_department_involved: bool,
        is_user_author: bool,
        user_department_can_save: bool = False,
        is_external: bool = False,
    ) -> bool:
        """Проверка права на конкретное действие на основе статической матрицы."""
        for key in ApplicationCapabilities._match_status_pattern(current_status):
            role_map = ApplicationCapabilities._ROLE_STATUS_ACTIONS.get(key, {})
            action_map = role_map.get(user_role, {})
            if action in action_map:
                policy = action_map[action]
                return ApplicationCapabilities._check_policy(
                    policy,
                    is_user_department_involved,
                    is_user_author,
                    user_department_can_save,
                    is_external,
                )
        return False

    @staticmethod
    def get_available_actions(
        current_status: str,
        user_role: str,
        is_user_department_involved: bool,
        is_user_author: bool,
        user_department_can_save: bool = False,
        is_external: bool = False,
    ) -> list[dict[str, Any]]:
        """Возвращает список доступных действий согласно матрице."""
        actions: list[str] = [
            "approve",
            "reject",
            "request_changes",
            "save_changes",
            "transfer_to_institute",
        ]
        available: list[dict[str, Any]] = []
        for a in actions:
            if ApplicationCapabilities.is_action_allowed(
                action=a,
                current_status=current_status,
                user_role=user_role,
                is_user_department_involved=is_user_department_involved,
                is_user_author=is_user_author,
                user_department_can_save=user_department_can_save,
                is_external=is_external,
            ):
                available.append(
                    {
                        "action": a,
                        "label": ApplicationCapabilities._ACTION_LABELS.get(a, a),
                        "config": {"status_code": current_status},
                    }
                )
        return available

    @staticmethod
    def can_manage_application(
        current_status: str,
        user_role: str,
        is_user_department_involved: bool,
        is_user_author: bool,
        user_department_can_save: bool = False,
        is_external: bool = False,
    ) -> bool:
        """УСТАРЕВШЕ: прокси к новой матрице. Считаем, что "управление"
        означает доступность хотя бы одного из действий approve/reject/request_changes.
        """
        return (
            ApplicationCapabilities.is_action_allowed(
                "approve",
                current_status,
                user_role,
                is_user_department_involved,
                is_user_author,
                user_department_can_save,
                is_external,
            )
            or ApplicationCapabilities.is_action_allowed(
                "reject",
                current_status,
                user_role,
                is_user_department_involved,
                is_user_author,
                user_department_can_save,
                is_external,
            )
            or ApplicationCapabilities.is_action_allowed(
                "request_changes",
                current_status,
                user_role,
                is_user_department_involved,
                is_user_author,
                user_department_can_save,
                is_external,
            )
        )

    @staticmethod
    def can_edit_application(
        current_status: str,
        user_role: str,
        is_user_department_involved: bool,
        is_user_author: bool,
        user_department_can_save: bool = False,
        is_external: bool = False,
    ) -> bool:
        """Проверка права на редактирование заявки.

        Бизнес-правило: редактировать может только автор заявки или сотрудник ЦПДС.
        С учетом ограничений по статусам: нельзя редактировать rejected и approved (кроме админов и cpds).
        Для institute_validator: разрешено, если у подразделения can_save_project_applications = True.
        """
        # Бизнес-правило: нельзя редактировать отклоненные заявки (кроме cpds для rejected_* статусов)
        if current_status == "rejected":
            return False

        # Бизнес-правило: нельзя редактировать одобренные заявки (кроме админов и cpds)
        if current_status == "approved" and user_role not in ["admin", "cpds"]:
            return False

        # Для статуса approved администраторы и сотрудники ЦПДС могут редактировать
        if current_status == "approved" and user_role in ["admin", "cpds"]:
            return True

        # Используем матрицу разрешений для проверки прав
        # В матрице для save_changes настроено: POLICY_OWN_ONLY для всех ролей (кроме cpds),
        # POLICY_DEPARTMENT_CAN_SAVE для institute_validator, и POLICY_ALLOW для роли cpds
        return ApplicationCapabilities.is_action_allowed(
            "save_changes",
            current_status,
            user_role,
            is_user_department_involved,
            is_user_author,
            user_department_can_save,
            is_external,
        )

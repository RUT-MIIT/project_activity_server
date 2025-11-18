"""Unit-тесты для DTO доступных действий showcase.dto.available_actions.

Проверяем создание, преобразование в словари, работу с действиями.
"""

from showcase.dto.available_actions import AvailableActionDTO, AvailableActionsDTO


class TestAvailableActionDTO:
    """Тесты для AvailableActionDTO."""

    def test_available_action_dto_creation(self):
        """Создание DTO действия с полными данными."""
        action = AvailableActionDTO(
            action="approve",
            label="Согласовать",
            config={"status_code": "await_department"},
        )

        assert action.action == "approve"
        assert action.label == "Согласовать"
        assert action.config == {"status_code": "await_department"}

    def test_available_action_dto_to_dict(self):
        """to_dict преобразует DTO действия в словарь для JSON."""
        action = AvailableActionDTO(
            action="reject",
            label="Отклонить",
            config={"reason": "required"},
        )

        result = action.to_dict()

        assert result == {
            "action": "reject",
            "label": "Отклонить",
            "config": {"reason": "required"},
        }

    def test_available_action_dto_empty_config(self):
        """DTO действия может иметь пустой config."""
        action = AvailableActionDTO(action="save", label="Сохранить", config={})

        assert action.config == {}
        result = action.to_dict()
        assert result["config"] == {}


class TestAvailableActionsDTO:
    """Тесты для AvailableActionsDTO."""

    def test_available_actions_dto_creation(self):
        """Создание DTO списка действий."""
        actions = [
            AvailableActionDTO(action="approve", label="Согласовать", config={}),
            AvailableActionDTO(action="reject", label="Отклонить", config={}),
        ]

        dto = AvailableActionsDTO(actions=actions)

        assert len(dto.actions) == 2
        assert dto.actions[0].action == "approve"
        assert dto.actions[1].action == "reject"

    def test_available_actions_dto_to_dict(self):
        """to_dict преобразует список действий в словарь с ключом available_actions."""
        actions = [
            AvailableActionDTO(action="approve", label="Согласовать", config={}),
            AvailableActionDTO(action="reject", label="Отклонить", config={}),
        ]

        dto = AvailableActionsDTO(actions=actions)
        result = dto.to_dict()

        assert "available_actions" in result
        assert len(result["available_actions"]) == 2
        assert result["available_actions"][0]["action"] == "approve"
        assert result["available_actions"][1]["action"] == "reject"

    def test_available_actions_dto_empty_list(self):
        """DTO может содержать пустой список действий."""
        dto = AvailableActionsDTO(actions=[])

        assert len(dto.actions) == 0
        result = dto.to_dict()
        assert result["available_actions"] == []

    def test_available_actions_dto_from_actions_list(self):
        """from_actions_list создаёт DTO из списка словарей действий."""
        actions_list = [
            {
                "action": "approve",
                "label": "Согласовать",
                "config": {"status_code": "await_department"},
            },
            {
                "action": "reject",
                "label": "Отклонить",
                "config": {"status_code": "await_department"},
            },
            {
                "action": "request_changes",
                "label": "Отправить на доработку",
                "config": {},
            },
        ]

        dto = AvailableActionsDTO.from_actions_list(actions_list)

        assert len(dto.actions) == 3
        assert dto.actions[0].action == "approve"
        assert dto.actions[0].label == "Согласовать"
        assert dto.actions[0].config == {"status_code": "await_department"}

        assert dto.actions[1].action == "reject"
        assert dto.actions[2].action == "request_changes"

    def test_available_actions_dto_from_actions_list_with_missing_fields(self):
        """from_actions_list использует значения по умолчанию для отсутствующих полей."""
        actions_list = [
            {"action": "approve"},  # Отсутствуют label и config
            {"action": "reject", "label": "Отклонить"},  # Отсутствует config
        ]

        dto = AvailableActionsDTO.from_actions_list(actions_list)

        assert dto.actions[0].action == "approve"
        assert dto.actions[0].label == ""  # По умолчанию пустая строка
        assert dto.actions[0].config == {}  # По умолчанию пустой словарь

        assert dto.actions[1].action == "reject"
        assert dto.actions[1].label == "Отклонить"
        assert dto.actions[1].config == {}

    def test_available_actions_dto_from_actions_list_empty(self):
        """from_actions_list работает с пустым списком."""
        dto = AvailableActionsDTO.from_actions_list([])

        assert len(dto.actions) == 0

    def test_available_actions_dto_from_actions_list_complex_config(self):
        """from_actions_list корректно обрабатывает сложные конфигурации."""
        actions_list = [
            {
                "action": "approve",
                "label": "Согласовать",
                "config": {
                    "status_code": "await_department",
                    "requires_reason": False,
                    "notifications": ["email", "sms"],
                },
            },
        ]

        dto = AvailableActionsDTO.from_actions_list(actions_list)

        assert dto.actions[0].config["status_code"] == "await_department"
        assert dto.actions[0].config["requires_reason"] is False
        assert dto.actions[0].config["notifications"] == ["email", "sms"]

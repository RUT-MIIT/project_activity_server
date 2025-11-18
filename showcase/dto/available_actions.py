"""DTO для представления доступных действий с заявками."""

from dataclasses import dataclass
from typing import Any


@dataclass
class AvailableActionDTO:
    """DTO для представления одного доступного действия."""

    action: str  # Код действия (approve, reject, etc.)
    label: str  # Человекочитаемое название
    config: dict[str, Any]  # Конфигурация действия

    def to_dict(self) -> dict[str, Any]:
        """Преобразование в словарь для JSON ответа."""
        return {"action": self.action, "label": self.label, "config": self.config}


@dataclass
class AvailableActionsDTO:
    """DTO для представления списка доступных действий."""

    actions: list[AvailableActionDTO]

    def to_dict(self) -> dict[str, Any]:
        """Преобразование в словарь для JSON ответа."""
        return {"available_actions": [action.to_dict() for action in self.actions]}

    @classmethod
    def from_actions_list(
        cls, actions_list: list[dict[str, Any]]
    ) -> "AvailableActionsDTO":
        """Создание DTO из списка действий.

        Args:
            actions_list: Список действий в формате словарей

        Returns:
            AvailableActionsDTO

        """
        action_dtos = []
        for action_data in actions_list:
            action_dto = AvailableActionDTO(
                action=action_data.get("action", ""),
                label=action_data.get("label", ""),
                config=action_data.get("config", {}),
            )
            action_dtos.append(action_dto)

        return cls(actions=action_dtos)

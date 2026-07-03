"""DTO для дашборда проектных заявок."""

from __future__ import annotations

from typing import Any


class ApplicationDashboardDTO:
    """DTO полного ответа дашборда."""

    def __init__(
        self,
        filters_applied: dict[str, Any],
        summary_cards: dict[str, Any],
        rating_chart: dict[str, Any],
        external_share_chart: dict[str, Any],
        status_distribution: dict[str, Any],
        application_type_distribution: dict[str, Any],
        daily_dynamics: dict[str, Any],
        oldest_in_progress: dict[str, Any],
    ) -> None:
        self.filters_applied = filters_applied
        self.summary_cards = summary_cards
        self.rating_chart = rating_chart
        self.external_share_chart = external_share_chart
        self.status_distribution = status_distribution
        self.application_type_distribution = application_type_distribution
        self.daily_dynamics = daily_dynamics
        self.oldest_in_progress = oldest_in_progress

    def to_dict(self) -> dict[str, Any]:
        """Преобразует DTO в словарь для API."""
        return {
            "filters_applied": self.filters_applied,
            "summary_cards": self.summary_cards,
            "rating_chart": self.rating_chart,
            "external_share_chart": self.external_share_chart,
            "status_distribution": self.status_distribution,
            "application_type_distribution": self.application_type_distribution,
            "daily_dynamics": self.daily_dynamics,
            "oldest_in_progress": self.oldest_in_progress,
        }


class SummaryCardsDTO:
    """DTO блока KPI-карточек."""

    def __init__(self, summary_data: dict[str, Any]) -> None:
        total = summary_data["total"]
        approved = summary_data["approved_count"]
        rejected = summary_data["rejected_count"]
        recent = summary_data["recent_count"]
        in_work = max(total - approved - rejected, 0)

        approved_pct = round((approved / total) * 100, 1) if total else 0.0
        rejected_pct = round((rejected / total) * 100, 1) if total else 0.0
        in_work_pct = round((in_work / total) * 100, 1) if total else 0.0

        self.cards = [
            {
                "id": "total",
                "label": "ВСЕГО ЗАЯВОК",
                "value": total,
                "subtext": f"+{recent} за последние 7 дней",
            },
            {
                "id": "approved",
                "label": "СОГЛАСОВАНО",
                "value": approved,
                "subtext": f"{approved_pct}% от общего числа",
            },
            {
                "id": "in_work",
                "label": "В РАБОТЕ",
                "value": in_work,
                "subtext": f"{in_work_pct}% от общего числа",
            },
            {
                "id": "rejected",
                "label": "ОТКЛОНЕНО",
                "value": rejected,
                "subtext": f"{rejected_pct}% от общего числа",
            },
            {
                "id": "avg_resolution_days",
                "label": "СР. ВРЕМЯ ДО РЕШЕНИЯ",
                "value": summary_data["avg_resolution_days"],
                "unit": "дн.",
                "subtext": (
                    f"Медиана: {summary_data['median_resolution_days']} дн. "
                    "(только завершённые)"
                ),
            },
        ]

    def to_dict(self) -> dict[str, Any]:
        """Преобразует DTO в словарь для API."""
        return {"cards": self.cards}

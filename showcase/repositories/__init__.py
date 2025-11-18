"""Repository слой для изоляции работы с базой данных.

Этот слой содержит все операции с БД, изолируя их от бизнес-логики.
"""

from .application import ProjectApplicationRepository

__all__ = [
    "ProjectApplicationRepository",
]

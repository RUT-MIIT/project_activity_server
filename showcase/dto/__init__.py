"""
DTO (Data Transfer Object) слой для передачи данных между слоями.

Этот слой содержит только структуры данных без бизнес-логики.
"""

from .application import (
    ProjectApplicationCreateDTO,
    ProjectApplicationUpdateDTO,
    ProjectApplicationReadDTO,
    ProjectApplicationListDTO,
)
from .validation import ValidationResult

__all__ = [
    'ProjectApplicationCreateDTO',
    'ProjectApplicationUpdateDTO', 
    'ProjectApplicationReadDTO',
    'ProjectApplicationListDTO',
    'ValidationResult',
]

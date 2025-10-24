"""
Результаты валидации для DTO.
"""

from typing import Dict, List


class ValidationResult:
    """Результат валидации данных"""
    
    def __init__(self):
        self.errors: Dict[str, str] = {}
    
    @property
    def is_valid(self) -> bool:
        """Проверка, что валидация прошла успешно"""
        return len(self.errors) == 0
    
    def add_error(self, field: str, message: str):
        """Добавление ошибки валидации"""
        self.errors[field] = message
    
    def add_errors(self, errors: Dict[str, str]):
        """Добавление нескольких ошибок"""
        self.errors.update(errors)
    
    def get_errors_list(self) -> List[str]:
        """Получение списка ошибок для отображения"""
        return [f"{field}: {message}" for field, message in self.errors.items()]
    
    def __str__(self):
        if self.is_valid:
            return "Validation successful"
        return f"Validation failed: {', '.join(self.get_errors_list())}"

"""Unit-тесты для ValidationResult showcase.dto.validation.

Проверяем добавление ошибок, проверку валидности, преобразование в строку.
"""

from showcase.dto.validation import ValidationResult


class TestValidationResult:
    """Тесты для ValidationResult."""

    def test_validation_result_init(self):
        """Инициализация ValidationResult создаёт пустой словарь ошибок."""
        result = ValidationResult()

        assert result.errors == {}
        assert result.is_valid is True

    def test_validation_result_is_valid_true_when_empty(self):
        """is_valid возвращает True когда нет ошибок."""
        result = ValidationResult()

        assert result.is_valid is True

    def test_validation_result_is_valid_false_when_has_errors(self):
        """is_valid возвращает False когда есть ошибки."""
        result = ValidationResult()
        result.add_error("title", "Название обязательно")

        assert result.is_valid is False

    def test_validation_result_add_error(self):
        """add_error добавляет ошибку в словарь."""
        result = ValidationResult()
        result.add_error("title", "Название обязательно")

        assert "title" in result.errors
        assert result.errors["title"] == "Название обязательно"

    def test_validation_result_add_multiple_errors(self):
        """add_error позволяет добавлять несколько ошибок для разных полей."""
        result = ValidationResult()
        result.add_error("title", "Название обязательно")
        result.add_error("goal", "Цель слишком короткая")
        result.add_error("company", "Компания обязательна")

        assert len(result.errors) == 3
        assert result.errors["title"] == "Название обязательно"
        assert result.errors["goal"] == "Цель слишком короткая"
        assert result.errors["company"] == "Компания обязательна"

    def test_validation_result_add_error_overwrites_existing(self):
        """add_error перезаписывает существующую ошибку для того же поля."""
        result = ValidationResult()
        result.add_error("title", "Первая ошибка")
        result.add_error("title", "Вторая ошибка")

        assert result.errors["title"] == "Вторая ошибка"
        assert len(result.errors) == 1

    def test_validation_result_add_errors(self):
        """add_errors добавляет несколько ошибок из словаря."""
        result = ValidationResult()
        errors_dict = {
            "title": "Название обязательно",
            "goal": "Цель слишком короткая",
            "company": "Компания обязательна",
        }
        result.add_errors(errors_dict)

        assert len(result.errors) == 3
        assert result.errors["title"] == "Название обязательно"
        assert result.errors["goal"] == "Цель слишком короткая"

    def test_validation_result_add_errors_merges_with_existing(self):
        """add_errors объединяет новые ошибки с существующими."""
        result = ValidationResult()
        result.add_error("title", "Существующая ошибка")

        new_errors = {"goal": "Новая ошибка", "company": "Ещё одна"}
        result.add_errors(new_errors)

        assert len(result.errors) == 3
        assert result.errors["title"] == "Существующая ошибка"
        assert result.errors["goal"] == "Новая ошибка"

    def test_validation_result_get_errors_list(self):
        """get_errors_list возвращает список строк в формате 'поле: сообщение'."""
        result = ValidationResult()
        result.add_error("title", "Название обязательно")
        result.add_error("goal", "Цель слишком короткая")

        errors_list = result.get_errors_list()

        assert len(errors_list) == 2
        assert "title: Название обязательно" in errors_list
        assert "goal: Цель слишком короткая" in errors_list

    def test_validation_result_get_errors_list_empty(self):
        """get_errors_list возвращает пустой список когда нет ошибок."""
        result = ValidationResult()

        errors_list = result.get_errors_list()

        assert errors_list == []

    def test_validation_result_str_valid(self):
        """__str__ возвращает 'Validation successful' когда валидация прошла."""
        result = ValidationResult()

        assert str(result) == "Validation successful"

    def test_validation_result_str_invalid(self):
        """__str__ возвращает сообщение с ошибками когда валидация не прошла."""
        result = ValidationResult()
        result.add_error("title", "Название обязательно")
        result.add_error("goal", "Цель слишком короткая")

        str_result = str(result)

        assert "Validation failed" in str_result
        assert "title: Название обязательно" in str_result
        assert "goal: Цель слишком короткая" in str_result

    def test_validation_result_str_invalid_single_error(self):
        """__str__ корректно форматирует сообщение при одной ошибке."""
        result = ValidationResult()
        result.add_error("title", "Название обязательно")

        str_result = str(result)

        assert "Validation failed" in str_result
        assert "title: Название обязательно" in str_result

    def test_validation_result_multiple_errors_same_field(self):
        """Когда одно поле имеет ошибку, затем добавляется другая, последняя остаётся."""
        result = ValidationResult()
        result.add_error("field1", "Первая ошибка")
        result.add_error("field2", "Вторая ошибка")
        result.add_error("field1", "Обновлённая ошибка")  # Перезаписывает

        assert result.errors["field1"] == "Обновлённая ошибка"
        assert result.errors["field2"] == "Вторая ошибка"

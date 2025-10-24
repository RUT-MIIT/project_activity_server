"""
Правила автоматических переходов статусов.

Формат: код_текущего_статуса -> код_целевого_статуса.
Хранится в коде, легко расширяется.
"""

# Простые правила 1→1
AUTO_TRANSITION_RULES = {
    'rejected_institute': 'rejected',
    'rejected_cpds': 'rejected',
    'rejected_department': 'rejected',
}

# Тексты комментариев по умолчанию для автопереходов (опционально)
AUTO_TRANSITION_COMMENTS = {
    'rejected_institute': 'Автопереход: статус "{from_name}" → "{to_name}"',
    'rejected_cpds': 'Автопереход: статус "{from_name}" → "{to_name}"',
    'rejected_department': 'Автопереход: статус "{from_name}" → "{to_name}"',
}



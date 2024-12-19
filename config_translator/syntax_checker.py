# config_translator/syntax_checker.py

import re


class SyntaxChecker:
    def __init__(self):
        # Можете добавить какие-то настройки, если они понадобятся в будущем
        pass

    # Функция для проверки, что строка соответствует имени (ключу)
    @staticmethod
    def is_valid_name(name):
        return bool(re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name))

    # Функция для проверки синтаксиса словаря
    def check_dict_structure(self, data):
        if not isinstance(data, dict):
            raise ValueError("Expected a dictionary")

        for key, value in data.items():
            if not self.is_valid_name(key):
                raise ValueError(f"Invalid key name: {key}")
            # Проверяем, что значения корректны
            self.check_value_structure(value)

    # Функция для проверки синтаксиса массивов
    def check_array_structure(self, data):
        if not isinstance(data, list):
            raise ValueError("Expected a list")

        for item in data:
            self.check_value_structure(item)

    # Функция для проверки синтаксиса значений (чисел, строк, словарей, массивов)
    def check_value_structure(self, value):
        if isinstance(value, dict):
            self.check_dict_structure(value)
        elif isinstance(value, list):
            self.check_array_structure(value)
        elif isinstance(value, (int, float)):  # Проверяем числа
            pass
        elif isinstance(value, str):  # Проверяем строки
            pass
        else:
            raise ValueError(f"Invalid value type: {type(value)}")

    # Главная функция для синтаксической проверки данных
    def check_syntax(self, data):
        try:
            self.check_value_structure(data)
        except ValueError as e:
            print(f"Syntax error: {e}")
            raise

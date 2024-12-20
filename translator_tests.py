import unittest
from translator import ConfigLanguageTranslator

class TestConfigLanguageTranslator(unittest.TestCase):
    def setUp(self):
        self.translator = ConfigLanguageTranslator()

    def test_simple_constant(self):
        """Тест объявления и использования константы."""
        self.translator.constants = {"PI": 3.14}
        self.assertEqual(self.translator.evaluate_constant("PI"), "3.14")

    def test_nested_constants(self):
        """Тест константы внутри словаря."""
        self.translator.constants = {"value": 42}
        input_data = {"data": "?(value)"}
        output = self.translator.translate(input_data)
        expected = "{\n    data -> 42.\n}"
        self.assertEqual(output, expected)

    def test_array_translation(self):
        """Тест преобразования массива."""
        input_data = ["value1", "value2", 123]
        output = self.translator.translate(input_data)
        expected = "[ value1 value2 123 ]"
        self.assertEqual(output, expected)

    def test_nested_dictionary(self):
        """Тест вложенных словарей."""
        input_data = {
            "level1": {
                "level2": {
                    "value": 10
                }
            }
        }
        output = self.translator.translate(input_data)
        expected = "{\n    level1 -> {\n        level2 -> {\n            value -> 10.\n        }.\n    }.\n}"
        self.assertEqual(output, expected)

    def test_syntax_error_invalid_name(self):
        """Тест ошибки синтаксиса при некорректном имени."""
        input_data = {"1invalid": 10}
        with self.assertRaises(SyntaxError):
            self.translator.translate(input_data)

    def test_syntax_error_constant_not_defined(self):
        """Тест ошибки обращения к неопределенной константе."""
        input_data = {"value": "?(undefined)"}
        with self.assertRaises(NameError):
            self.translator.translate(input_data)

    def test_remove_comments(self):
        """Тест удаления однострочных комментариев."""
        lines = [
            '! This is a comment',
            '{"key": "value"}',
            '    ! Another comment'
        ]
        expected = ['{"key": "value"}']
        cleaned = self.translator.remove_comments(lines)
        self.assertEqual(cleaned, expected)

if __name__ == "__main__":
    unittest.main()
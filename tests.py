import unittest
from config_translator.parser import parse_json

class TestParser(unittest.TestCase):
    def test_valid_json(self):
        input_json = '{"key1": "value1", "key2": [1, 2, 3]}'
        expected_output = {
            "key1": "value1",
            "key2": [1, 2, 3]
        }
        result = parse_json(input_json)
        self.assertEqual(result, expected_output)

    def test_invalid_json(self):
        input_json = '{"key1": "value1", "key2": [1, 2, 3]'  # Отсутствует закрывающая скобка
        with self.assertRaises(ValueError):
            parse_json(input_json)

if __name__ == '__main__':
    unittest.main()
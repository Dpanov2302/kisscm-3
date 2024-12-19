import unittest
from config_translator.transformer import transform_to_config_language

class TestTransformer(unittest.TestCase):
    def test_transform_number(self):
        self.assertEqual(transform_to_config_language(100), "100")

    def test_transform_string(self):
        self.assertEqual(transform_to_config_language("value1"), '"value1"')

    def test_transform_list(self):
        self.assertEqual(transform_to_config_language([1, 2, 3]), '[ 1 2 3 ]')

    def test_transform_dict(self):
        data = {
            "key1": "value1",
            "key2": [1, 2, 3],
        }
        expected_output = '{\n  key1 -> "value1".\n  key2 -> [ 1 2 3 ].\n}'
        self.assertEqual(transform_to_config_language(data), expected_output)

    def test_transform_constant(self):
        # Проверка на выражение с константой
        self.assertEqual(transform_to_config_language("?CONST_ONE"), '?(CONST_ONE)')

if __name__ == '__main__':
    unittest.main()

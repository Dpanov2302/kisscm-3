# tests.py
import unittest
from unittest.mock import patch, MagicMock
import json
from main import main

class TestMain(unittest.TestCase):
    @patch("sys.argv", new=["main.py", "output.txt"])  # Патчим sys.argv первым
    @patch("builtins.open", new_callable=unittest.mock.mock_open)  # Патчим open вторым
    def test_main(self, mock_argv, mock_file):  # Порядок аргументов соответствует декораторам
        # Подготовим пример JSON данных
        input_data = {
            "key1": "value1",
            "key2": [1, 2, 3],
            "key3": {"subkey1": "subvalue1"}
        }

        # Патчим open, чтобы вернуть наши данные в качестве содержимого файла
        mock_file.return_value.read.return_value = json.dumps(input_data)

        # Вызов главной функции
        main()

        # Проверяем, что файл был открыт для записи
        mock_file.assert_called_once_with("output.txt", "w")
        mock_file().write.assert_called_once_with(
            '''{
  key1 -> "value1".
  key2 -> [ 1 2 3 ].
  key3 -> {
    subkey1 -> "subvalue1".
  }.
}'''
        )

if __name__ == '__main__':
    unittest.main()

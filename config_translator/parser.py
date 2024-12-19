import json

def parse_json(input_json: str):
    """
    Преобразует строку JSON в структуру данных Python.
    :param input_json: Строка в формате JSON.
    :return: Структура данных Python (словарь, список).
    :raises ValueError: Если формат JSON некорректен.
    """
    try:
        return json.loads(input_json)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")

# Пример
def main():
    input_json = '{"key1": "value1", "key2": [1, 2, 3]}'
    parsed_data = parse_json(input_json)
    print(parsed_data)

if __name__ == "__main__":
    main()
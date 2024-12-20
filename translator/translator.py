import argparse
import json
import re
import sys

class ConfigLanguageTranslator:
    def __init__(self):
        self.constants = {}

    def translate(self, data):
        if isinstance(data, dict):
            return self._translate_dict(data)
        elif isinstance(data, list):
            return self._translate_list(data)
        elif isinstance(data, str) and data.startswith("?("):
            # Обработка константного выражения
            return self.evaluate_constant(data[2:-1].strip())
        else:
            return str(data)

    def _translate_dict(self, data):
        items = []
        for key, value in data.items():
            if not self._is_valid_name(key):
                raise SyntaxError(f"Invalid name: {key}")
            translated_value = self.translate(value)
            items.append(f"{key} -> {translated_value}.")
        return "{\n" + "\n".join(items) + "\n}"

    def _translate_list(self, data):
        translated_items = [self.translate(item) for item in data]
        return "[ " + " ".join(translated_items) + " ]"

    def _is_valid_name(self, name):
        return re.match(r'^[_a-zA-Z][_a-zA-Z0-9]*$', name) is not None

    def parse_constants(self, json_data):
        for key, value in json_data.items():
            if isinstance(value, (int, float, str)):
                if not self._is_valid_name(key):
                    raise SyntaxError(f"Invalid constant name: {key}")
                self.constants[key] = value

    def evaluate_constant(self, name):
        # Проверка, есть ли такая константа
        if name not in self.constants:
            raise NameError(f"Constant '{name}' is not defined")
        return str(self.constants[name])

def main():
    parser = argparse.ArgumentParser(description="JSON to configuration language translator")
    parser.add_argument("input_file", help="Path to the input JSON file")
    parser.add_argument("output_file", help="Path to the output text file")
    args = parser.parse_args()

    try:
        with open(args.input_file, "r") as f:
            input_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}", file=sys.stderr)
        sys.exit(1)

    translator = ConfigLanguageTranslator()
    try:
        # Извлекаем и обрабатываем константы
        if "constants" in input_data:
            translator.parse_constants(input_data["constants"])
            del input_data["constants"]

        # Переводим JSON в конфигурационный язык
        translated = translator.translate(input_data)
    except (SyntaxError, NameError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(translator.constants)

    try:
        with open(args.output_file, "w") as f:
            f.write(translated)
        print(f"Translation successful. Output written to {args.output_file}")
    except IOError as e:
        print(f"Error writing to file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

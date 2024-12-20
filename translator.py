import re

class ConfigLanguageTranslator:
    def __init__(self):
        self.constants = {}

    def translate(self, data, indent_level=0):
        if isinstance(data, dict):
            return self._translate_dict(data, indent_level)
        elif isinstance(data, list):
            return self._translate_list(data)
        elif isinstance(data, str) and data.startswith("?("):
            return self.evaluate_constant(data[2:-1].strip())
        else:
            return str(data)

    def _translate_dict(self, data, indent_level=0):
        items = []
        indent = "    " * indent_level  # 4 пробела для табуляции
        inner_indent = "    " * (indent_level + 1)

        for key, value in data.items():
            if not self._is_valid_name(key):
                raise SyntaxError(f"Invalid name: {key}")
            translated_value = self.translate(value, indent_level + 1) if isinstance(value,
                                                                                     (dict, list)) else self.translate(
                value)
            items.append(f"{inner_indent}{key} -> {translated_value}.")

        return "{\n" + "\n".join(items) + f"\n{indent}}}"

    def _translate_list(self, data):
        data_no_comments = self.remove_comments(data)
        translated_items = [self.translate(item) for item in data_no_comments]
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

    def remove_comments(self, lines):
        """Удаляет однострочные комментарии из входных строк."""
        result = []
        for line in lines:
            if isinstance(line, str):
                if not (line.strip().startswith('"!') or line.strip().startswith('!')):
                    result.append(line)
            else:
                result.append(line)
        return result

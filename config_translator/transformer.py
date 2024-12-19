class ConfigLanguageTransformer:
    """
    Класс для преобразования данных в формат учебного конфигурационного языка.
    Он обрабатывает массивы, словари, строки, числа, а также добавляет комментарии.
    """

    def transform(self, data):
        """
        Преобразует данные в формат конфигурационного языка.
        Обрабатывает массивы, словари и константы.
        """
        if isinstance(data, dict):
            return self.transform_dict(data)
        elif isinstance(data, list):
            return self.transform_list(data)
        elif isinstance(data, str):
            return data
        elif isinstance(data, (int, float)):
            return str(data)
        else:
            raise ValueError(f"Unsupported data type: {type(data)}")

    def transform_dict(self, data):
        """
        Преобразует словарь в формат конфигурационного языка.
        """
        result = []
        for key, value in data.items():
            key_str = self.transform(key)
            value_str = self.transform(value)
            result.append(f"{key_str} -> {value_str}")
        return "{\n" + "\n".join(result) + "\n}"

    def transform_list(self, data):
        """
        Преобразует список в формат конфигурационного языка.
        """
        return "[ " + ", ".join(self.transform(item) for item in data) + " ]"

    def add_comment(self, comment):
        """
        Добавляет комментарий в нужном формате.
        """
        return f"! {comment}"
import argparse
import json
from config_translator.syntax_checker import SyntaxChecker
from config_translator.transformer import ConfigLanguageTransformer


def parse_args():
    # Создаем парсер командной строки
    parser = argparse.ArgumentParser(description="Tool for converting JSON to custom configuration format.")

    # Добавляем аргументы для входного и выходного файлов
    parser.add_argument(
        'input_file',
        help='Path to the input JSON file'
    )
    parser.add_argument(
        'output_file',
        help='Path to the output configuration file'
    )

    return parser.parse_args()


def main():
    # Разбираем аргументы командной строки
    args = parse_args()

    # Открываем и загружаем входной JSON файл
    with open(args.input_file, 'r') as infile:
        input_data = json.load(infile)

    # Создаем экземпляр класса SyntaxChecker
    checker = SyntaxChecker()
    transformer = ConfigLanguageTransformer()

    # Проверяем синтаксис данных
    checker.check_syntax(input_data)

    # Трансформируем данные в нужный формат
    transformed_data = transformer.transform(input_data)

    # Записываем результат в выходной файл
    with open(args.output_file, 'w') as outfile:
        outfile.write(transformed_data)


if __name__ == "__main__":
    main()

import argparse
import json
import sys
from translator import ConfigLanguageTranslator


def main():
    parser = argparse.ArgumentParser(description="JSON to configuration language translator")
    parser.add_argument("input_file", help="Path to the input JSON file")
    parser.add_argument("output_file", help="Path to the output text file")
    args = parser.parse_args()

    try:
        with open(args.input_file, "r") as f:
            # Считываем строки и удаляем комментарии
            lines = f.readlines()
            lines = ConfigLanguageTranslator().remove_comments(lines)
            input_data = json.loads("".join(lines))
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

    try:
        with open(args.output_file, "w") as f:
            f.write(translated)
        print(f"Translation successful. Output written to {args.output_file}")
    except IOError as e:
        print(f"Error writing to file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()

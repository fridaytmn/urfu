import csv
import re


def clean_text(text):
    """Удаляет HTML теги и лишние пробелы, нормализует строки."""
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def process_value(value):
    """Обрабатывает значение для вложенных списков и пустых значений."""
    if not value.strip():
        return "Нет данных"

    parts = [clean_text(part) for part in value.split("\n") if part.strip()]

    return "; ".join(parts) if parts else "Нет данных"


def parse_csv(file_name):
    with open(file_name, mode="r", encoding="utf-8-sig") as file:
        filtered_data = []
        reader = csv.reader(file)

        headers = next(reader)
        min_filled = (len(headers) + 1) // 2

        for rows in reader:
            filled_fields = sum(1 for field in rows if field)

            if filled_fields >= min_filled:
                row_dict = {}
                for header, row in zip(headers, rows):
                    row_dict[header] = process_value(row)

                filtered_data.append(row_dict)

    return filtered_data


def main():
    filtered_data = parse_csv(input("Enter the filename: "))

    for i, entry in enumerate(filtered_data):
        print(*(f"{k}: {v}" for k, v in entry.items()), sep="\n")
        if i < len(filtered_data) - 1:
            print()


if __name__ == "__main__":
    main()

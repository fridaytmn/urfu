import csv
from prettytable import PrettyTable

TRANSLATION_DICT = {
    "name": "Название",
    "description": "Описание",
    "key_skills": "Навыки",
    "experience_id": "Опыт работы",
    "premium": "Премиум-вакансия",
    "employer_name": "Компания",
    "salary_from": "Нижняя граница вилки оклада",
    "salary_to": "Верхняя граница вилки оклада",
    "salary_gross": "Оклад указан до вычета налогов",
    "salary_currency": "Идентификатор валюты оклада",
    "area_name": "Название региона",
    "published_at": "Дата публикации вакансии",
    "noExperience": "Нет опыта",
    "between1And3": "От 1 года до 3 лет",
    "between3And6": "От 3 до 6 лет",
    "moreThan6": "Более 6 лет",
    "AZN": "Манаты",
    "BYR": "Белорусские рубли",
    "EUR": "Евро",
    "GEL": "Грузинский лари",
    "KGS": "Киргизский сом",
    "KZT": "Тенге",
    "RUR": "Рубли",
    "UAH": "Гривны",
    "USD": "Доллары",
    "UZS": "Узбекский сум",
    "True": "Да",
    "False": "Нет",
}


def csv_reader(file_name):
    """
    Чтение CSV-файла. Возвращает заголовки полей и список данных о вакансиях.
    """
    with open(file_name, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames  # Заголовки полей CSV
        vacancies = [row for row in reader]  # Данные вакансий
    return headers, vacancies


def translate_value(value):
    """
    Замена значений и кодов на понятные описания.
    """
    return TRANSLATION_DICT.get(value, value)


def truncate_text(text, max_length=100):
    """
    Обрезает текст до заданной длины и добавляет троеточие, если текст длиннее.
    """
    return text[:max_length] + "..." if len(text) > max_length else text


def format_salary(salary_from, salary_to, currency, gross):
    """
    Форматирует зарплату в виде строки.
    """
    try:
        salary_from = (
            f"{int(float(salary_from)):,}".replace(",", " ")
            if salary_from
            else "Не указано"
        )
        salary_to = (
            f"{int(float(salary_to)):,}".replace(",", " ")
            if salary_to
            else "Не указано"
        )
    except ValueError:
        salary_from, salary_to = "Не указано", "Не указано"
    gross_text = "Без вычета налогов" if gross == "True" else "С вычетом налогов"
    currency = TRANSLATION_DICT.get(currency, currency)
    return f"{salary_from} - {salary_to} ({currency}) ({gross_text})"


def formatter(row):
    """
    Форматирует строку вакансии для отображения.
    """
    formatted_row = {}
    for key, value in row.items():
        value = value.strip() if value else ""
        if key == "experience_id":
            formatted_row["Опыт работы"] = translate_value(value)
        elif key == "premium":
            formatted_row["Премиум-вакансия"] = translate_value(value)
        elif key == "key_skills":
            formatted_row["Навыки"] = truncate_text(
                ", ".join(skill.strip() for skill in value.splitlines()), 100
            )
        elif key.startswith("salary"):
            formatted_row["Оклад"] = format_salary(
                row.get("salary_from", ""),
                row.get("salary_to", ""),
                row.get("salary_currency", ""),
                row.get("salary_gross", ""),
            )
        else:
            translated_key = TRANSLATION_DICT.get(key, key)
            formatted_row[translated_key] = truncate_text(value, 100)
    return formatted_row


def print_vacancies_as_table(vacancies, start=None, end=None, columns=None):
    """
    Выводит данные о вакансиях в виде таблички с учетом фильтров и выбранных столбцов.
    """
    if not vacancies:
        print("Нет данных")
        return

    if start is not None:
        vacancies = vacancies[start - 1 :]
    if end is not None:
        vacancies = vacancies[: end - start + 1] if start else vacancies[:end]

    all_columns = [
        "№",
        "Название",
        "Описание",
        "Навыки",
        "Опыт работы",
        "Премиум-вакансия",
        "Компания",
        "Оклад",
        "Название региона",
        "Дата публикации вакансии",
    ]
    selected_columns = ["№"] + columns if columns else all_columns

    table = PrettyTable()
    table.field_names = all_columns
    table.align = "l"
    table.max_width = 20
    table.hrules = True

    for index, vacancy in enumerate(vacancies, start=start or 1):
        formatted_row = formatter(vacancy)
        row = [index]
        for column in all_columns[1:]:
            value = formatted_row.get(column, "")
            row.append(truncate_text(value))
        table.add_row(row)

    print(table.get_string(fields=selected_columns))


def main():
    file_name = input()
    range_input = input()
    columns_input = input()

    headers, vacancies = csv_reader(file_name)

    start, end = None, None
    if range_input:
        range_parts = range_input.split()
        start = int(range_parts[0]) if len(range_parts) > 0 else None
        end = int(range_parts[1]) if len(range_parts) > 1 else None

    columns = None
    if columns_input:
        columns = [col.strip() for col in columns_input.split(",")]

    print_vacancies_as_table(vacancies, start=start, end=end, columns=columns)


if __name__ == "__main__":
    main()

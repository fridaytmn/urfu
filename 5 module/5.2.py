import csv

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
        headers = reader.fieldnames
        vacancies = [row for row in reader]
    return headers, vacancies


def translate_header(header):
    """
    Перевод заголовков полей на русский язык.
    """
    return TRANSLATION_DICT.get(header, header)


def translate_value(value):
    """
    Замена значений и кодов на понятные описания.
    """
    return TRANSLATION_DICT.get(value, value)


def format_salary_field(row):
    """
    Форматирует строку с зарплатой из нескольких полей.
    """
    salary_from = format_salary(row.get("salary_from", "").strip())
    salary_to = format_salary(row.get("salary_to", "").strip())
    salary_currency = translate_value(row.get("salary_currency", "").strip())
    salary_gross = (
        "Без вычета налогов"
        if row.get("salary_gross", "").strip() == "True"
        else "С вычетом налогов"
    )
    salary_range = f"{salary_from} - {salary_to}".strip(" -")
    return f"{salary_range} ({salary_currency}) ({salary_gross})"


def format_salary(salary):
    """
    Форматирует числовое значение зарплаты с разделением разрядов.
    """
    try:
        return f"{int(float(salary)):,}".replace(",", " ")
    except ValueError:
        return salary


def formatter(row):
    """
    Форматирует строку вакансии для печати, преобразуя значения согласно правилам.
    """
    formatted_row = {}

    for key, value in row.items():
        if key == "experience_id":
            formatted_row["Опыт работы"] = translate_value(value)
        elif key == "premium":
            formatted_row["Премиум-вакансия"] = (
                "Да" if value.strip() == "True" else "Нет"
            )
        elif key == "key_skills":
            formatted_row["Навыки"] = ", ".join(
                skill.strip() for skill in value.splitlines()
            )
        elif key.startswith("salary"):
            formatted_row["Оклад"] = format_salary_field(row)
        else:
            translated_key = translate_header(key)
            formatted_row[translated_key] = value.strip()

    return formatted_row


def print_vacancies(vacancies, headers):
    """
    Выводит данные о вакансиях с форматированием.
    """
    formatted_output = []
    for vacancy in vacancies:
        formatted_row = formatter(vacancy)
        formatted_vacancy = "\n".join(
            f"{key}: {value}" for key, value in formatted_row.items()
        )
        formatted_output.append(formatted_vacancy)

    print("\n\n".join(formatted_output))


file_name = input()
headers, vacancies = csv_reader(file_name)
print_vacancies(vacancies, headers)

import csv

# Словарь для перевода заголовков и значений
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
    "published_at": "Дата и время публикации вакансии",
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


def translate_header(header):
    """
    Перевод заголовков полей на русский язык.
    """
    return TRANSLATION_DICT.get(header, header)


def translate_value(value):
    """
    Замена значений True/False на Да/Нет.
    """
    return TRANSLATION_DICT.get(value, value)


def format_vacancy(vacancy, headers):
    """
    Форматирует вакансию в соответствии с требуемым шаблоном.
    """
    formatted_vacancy = []
    for header in headers:
        translated_header = translate_header(header)
        value = vacancy[header]
        translated_value = translate_value(value.strip())

        # Обработка списка навыков
        if header == "key_skills":
            skills = translated_value.splitlines()
            translated_value = ", ".join(skill.strip() for skill in skills)

        formatted_vacancy.append(f"{translated_header}: {translated_value}")

    return "\n".join(formatted_vacancy)


def print_vacancies(vacancies, headers):
    """
    Выводит данные о вакансиях с переводом заголовков и значений True/False,
    добавляя пустую строку между вакансиями.
    """
    formatted_output = []
    for vacancy in vacancies:
        formatted_vacancy = format_vacancy(vacancy, headers)
        formatted_output.append(formatted_vacancy)

    # Вывод вакансий с разделением пустыми строками
    print("\n\n".join(formatted_output))


# Пример использования
file_name = "vacancies.csv"  # input(vacancies.csv)
headers, vacancies = csv_reader(file_name)
print_vacancies(vacancies, headers)

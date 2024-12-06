import json
import re


def process_description(text):
    """Обработка поля description."""
    sentences = text.split(". ")
    processed_sentences = [
        sentence.strip().capitalize() for sentence in sentences if sentence
    ]
    result = ". ".join(processed_sentences)
    if result.endswith((".", ";")):
        result = result[:-1]
    return result.strip()


def process_salary(value):
    """Округление до двух знаков после запятой."""
    return f"{float(value):.2f}"


def process_key_phrase(text):
    """Все буквы заглавные и добавление восклицательного знака."""
    return text.upper() + "!"


def process_addition(text):
    """Все буквы строчные с добавлением точек в начале и конце."""
    i = len(text)
    while not text[i - 1 : i].isalpha():
        i -= 1
    return f"..{text[:i].lower()}.."


def process_company_info(text):
    """Удаление скобочных конструкций и текста внутри них."""
    text = re.sub(r"\(.+\)|\)|\(", "  ", text)
    return text


def process_key_skills(text):
    """Замена HTML-кодов &nbsp на пробелы."""
    i = len(text)
    while not text[:i].isalpha():
        i -= 1
    return text.replace("&nbsp", " ")


def parse_fields(input_line):
    """Разбивает строку с полями на словарь."""
    fields = {}
    for pair in input_line.split("; "):
        key, value = pair.split(": ", 1)
        fields[key.strip()] = value.strip()
    return fields


def process_vacancy(input_line, fields_to_process):
    """Обрабатывает указанные поля вакансии и выводит их в формате JSON."""
    fields = parse_fields(input_line)
    result = {}

    for field in fields_to_process.split(", "):
        if field in fields:
            value = fields[field]
            if field == "description":
                result[field] = process_description(value)
            elif field == "salary":
                result[field] = process_salary(value)
            elif field == "key_phrase":
                result[field] = process_key_phrase(value)
            elif field == "addition":
                result[field] = process_addition(value)
            elif field == "company_info":
                result[field] = process_company_info(value)
            elif field == "key_skills":
                result[field] = process_key_skills(value)

    return json.dumps(result, ensure_ascii=False)


input_line = input()
fields_to_process = input()

print(process_vacancy(input_line, fields_to_process))

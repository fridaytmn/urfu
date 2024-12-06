from var_dump import var_dump
import csv


class Salary:
    def __init__(self, salary_from, salary_to, salary_gross, salary_currency):
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_gross = salary_gross
        self.salary_currency = salary_currency


class Vacancy:
    def __init__(self, name, description, key_skills, experience_id, premium, employer_name, salary, area_name, published_at):
        self.name = name
        self.description = description
        self.key_skills = key_skills
        self.experience_id = experience_id
        self.premium = premium
        self.employer_name = employer_name
        self.salary = salary
        self.area_name = area_name
        self.published_at = published_at


def read_csv_and_parse(filename: str) -> list[Vacancy]:
    vacancies = []
    with open(filename, encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            salary = Salary(
                salary_from=row['salary_from'],
                salary_to=row['salary_to'],
                salary_gross=row['salary_gross'],
                salary_currency=row['salary_currency']
            )
            vacancy = Vacancy(
                name=row['name'],
                description=row['description'],
                key_skills=row['key_skills'],
                experience_id=row['experience_id'],
                premium=row['premium'],
                employer_name=row['employer_name'],
                salary=salary,
                area_name=row['area_name'],
                published_at=row['published_at']
            )
            vacancies.append(vacancy)
    return vacancies

if __name__ == "__main__":
    filename = input()
    vacancies = read_csv_and_parse(filename)
    var_dump(vacancies)
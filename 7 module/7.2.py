import csv
from prettytable import PrettyTable


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


class DataSet:
    def __init__(self, filename):
        self.filename = filename
        self.vacancies = self._read_csv()

    def _read_csv(self):
        vacancies = []
        with open(self.filename, encoding='utf-8-sig') as file:
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


class Utils:

    def truncate_text(text, max_length=100):
        return text[:max_length] + "..." if len(text) > max_length else text

    @staticmethod
    def create_table(dataset):
        table = PrettyTable()

        table.field_names = [
            "№", "name", "description", "key_skills", "experience_id",
            "premium", "employer_name", "salary_from", "salary_to",
            "salary_gross", "salary_currency", "area_name", "published_at"
        ]
        table.align = "l"
        table.max_width = 20
        table.hrules = True

        for i, vacancy in enumerate(dataset.vacancies, 1):
            table.add_row([
                i,
                Utils.truncate_text(vacancy.name),
                Utils.truncate_text(vacancy.description),
                Utils.truncate_text(vacancy.key_skills),
                Utils.truncate_text(vacancy.experience_id),
                Utils.truncate_text(vacancy.premium),
                Utils.truncate_text(vacancy.employer_name),
                vacancy.salary.salary_from,
                vacancy.salary.salary_to,
                vacancy.salary.salary_gross,
                vacancy.salary.salary_currency,
                Utils.truncate_text(vacancy.area_name),
                Utils.truncate_text(vacancy.published_at)
            ])
        return table


def main():
    filename = input()
    dataset = DataSet(filename)
    table = Utils.create_table(dataset)
    print(table)


if __name__ == '__main__':
    main()
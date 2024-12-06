import csv
from collections import defaultdict
from datetime import datetime

currency_to_rub = {
    "Манаты": 35.68,
    "Белорусские рубли": 23.91,
    "Евро": 59.90,
    "Грузинский лари": 21.74,
    "Киргизский сом": 0.76,
    "Тенге": 0.13,
    "Рубли": 1,
    "Гривны": 1.64,
    "Доллары": 60.66,
    "Узбекский сум": 0.0055,
}

class Salary:
    def __init__(self, salary_from, salary_to, salary_currency):
        self.salary_from = float(salary_from) if salary_from else 0
        self.salary_to = float(salary_to) if salary_to else 0
        self.salary_currency = salary_currency

    def to_rub(self):
        average_salary = (self.salary_from + self.salary_to) / 2 if self.salary_from and self.salary_to else 0
        return average_salary * currency_to_rub.get(self.salary_currency, 0)

class Vacancy:
    def __init__(self, name, salary, area_name, published_at):
        self.name = name
        self.salary = salary
        self.area_name = area_name
        self.published_at = datetime.strptime(published_at, '%H:%M:%S %d/%m/%Y').year

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
                    salary_currency=row['salary_currency']
                )
                vacancy = Vacancy(
                    name=row['name'],
                    salary=salary,
                    area_name=row['area_name'],
                    published_at=row['published_at']
                )
                vacancies.append(vacancy)
        return vacancies

class Statistics:
    def __init__(self, dataset):
        self.dataset = dataset

    def get_stats(self, profession_name):
        salary_by_year = defaultdict(list)
        count_by_year = defaultdict(int)
        salary_by_profession = defaultdict(list)
        count_by_profession = defaultdict(int)
        salary_by_city = defaultdict(list)
        count_by_city = defaultdict(int)

        # Обработка вакансий
        for vacancy in self.dataset.vacancies:
            year = vacancy.published_at
            city = vacancy.area_name
            salary_rub = vacancy.salary.to_rub()

            # Общая статистика по годам
            salary_by_year[year].append(salary_rub)
            count_by_year[year] += 1

            # Статистика по профессии
            if profession_name.lower() in vacancy.name.lower():
                salary_by_profession[year].append(salary_rub)
                count_by_profession[year] += 1

            # Статистика по городам
            salary_by_city[city].append(salary_rub)
            count_by_city[city] += 1

        # Агрегация данных
        average_salary_by_year = {year: int(round(sum(salaries) / len(salaries))) for year, salaries in salary_by_year.items()}
        average_salary_by_profession = {year: int(round(sum(salaries) / len(salaries))) for year, salaries in salary_by_profession.items()}
        average_salary_by_city = {city: int(round(sum(salaries) / len(salaries))) for city, salaries in salary_by_city.items()}
        total_vacancies = sum(count_by_city.values())
        share_by_city = {city: round(count / total_vacancies, 4) for city, count in count_by_city.items()}

        # Сортировка данных
        average_salary_by_year = dict(sorted(average_salary_by_year.items(), key=lambda x: x[0]))
        count_by_year = dict(sorted(count_by_year.items(), key=lambda x: x[0]))
        average_salary_by_profession = dict(sorted(average_salary_by_profession.items(), key=lambda x: x[0]))
        count_by_profession = dict(sorted(count_by_profession.items(), key=lambda x: x[0]))
        top_cities_salary = dict(sorted(average_salary_by_city.items(), key=lambda x: x[1], reverse=True)[:10])
        top_cities_share = dict(sorted(share_by_city.items(), key=lambda x: x[1], reverse=True)[:10])

        print(f"Средняя зарплата по годам: {average_salary_by_year}")
        print(f"Количество вакансий по годам: {count_by_year}")
        print(f"Средняя зарплата по годам для профессии '{profession_name}': {average_salary_by_profession}")
        print(f"Количество вакансий по годам для профессии '{profession_name}': {count_by_profession}")
        print(f"Средняя зарплата по городам: {top_cities_salary}")
        print(f"Доля вакансий по городам: {top_cities_share}")

def main():
    filename = input()
    profession_name = input()
    dataset = DataSet(filename)
    statistics = Statistics(dataset)
    statistics.get_stats(profession_name)

if __name__ == '__main__':
    main()
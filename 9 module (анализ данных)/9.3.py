import pandas as pd

vacancies = pd.read_csv('vacancies_small.csv')

vacancies_rur = vacancies[vacancies['salary_currency'] == 'RUR']

city_salaries = {}

for _, row in vacancies_rur.iterrows():
    city = row['area_name']
    salary_from = row['salary_from']
    salary_to = row['salary_to']

    if pd.notna(salary_from) and pd.notna(salary_to):
        avg_salary = (salary_from + salary_to) / 2
    elif pd.notna(salary_from):
        avg_salary = salary_from
    elif pd.notna(salary_to):
        avg_salary = salary_to
    else:
        continue

    avg_salary = round(avg_salary)

    if city not in city_salaries:
        city_salaries[city] = []
    city_salaries[city].append(avg_salary)

city_avg_salaries = {}
for city, salaries in city_salaries.items():
    city_avg_salaries[city] = round(sum(salaries) / len(salaries))

sorted_city_avg_salaries = dict(sorted(city_avg_salaries.items(), key=lambda x: (-x[1], x[0])))

print(sorted_city_avg_salaries)
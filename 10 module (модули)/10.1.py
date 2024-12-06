from cProfile import label
from operator import index

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Border, Side, Font
import matplotlib.pyplot as plt

def load_data(filename):
    """Загрузка данных из CSV файла и подготовка столбцов."""
    vacancies = pd.read_csv(filename, header=None)
    vacancies.columns = ['name', 'salary_from', 'salary_to', 'currency', 'city', 'date']
    vacancies['salary'] = vacancies[['salary_from', 'salary_to']].mean(axis=1)
    return vacancies

def calculate_yearly_statistics(vacancies):
    """Вычисление статистики по годам (средняя зарплата, количество вакансий)."""
    vacancies['year'] = pd.to_datetime(vacancies['date'], utc=True, errors='coerce').dt.year
    years = range(2007, 2023)
    avg_salaries = []
    vacancy_counts = []

    for year in years:
        year_data = vacancies[vacancies['year'] == year]
        avg_salary = year_data['salary'].mean()
        vacancy_count = len(year_data)
        avg_salaries.append(int(round(avg_salary)))
        vacancy_counts.append(vacancy_count)

    return years, avg_salaries, vacancy_counts

def write_city_statistics(sheet, valid_cities):
    """Записывает статистику по городам в лист Excel."""
    sheet.append(['Город', 'Уровень зарплат', '', 'Город', 'Доля вакансий, %'])

    sorted_by_salary = valid_cities.sort_values(by='average_salary', ascending=False)
    sorted_by_vacancies = valid_cities.sort_values(by='vacancy_share', ascending=False)

    for i in range(min(len(sorted_by_salary), 10)):
        city_salary = sorted_by_salary.index[i]
        city_vacancy = sorted_by_vacancies.index[i]

        avg_salary_city = sorted_by_salary.loc[city_salary, 'average_salary']
        vacancy_share = sorted_by_vacancies.loc[city_vacancy, 'vacancy_share'] * 100

        sheet.append([city_salary, int(round(avg_salary_city)), '', city_vacancy, round(vacancy_share, 2)])

def write_yearly_statistics(sheet, years, avg_salaries, vacancy_counts):
    """Записывает статистику по годам в лист Excel."""
    sheet.append(['Год', 'Средняя зарплата', 'Количество вакансий'])
    for i, year in enumerate(years):
        sheet.append([year, avg_salaries[i], vacancy_counts[i]])

def calculate_city_statistics(vacancies):
    """Вычисление статистики по городам (средняя зарплата, доля вакансий)."""
    city_salary = vacancies.groupby('city')['salary'].mean()
    city_vacancies = vacancies['city'].value_counts(normalize=True)

    city_stats = pd.DataFrame({
        'average_salary': city_salary,
        'vacancy_share': city_vacancies
    })

    valid_cities = city_stats[city_stats['vacancy_share'] > 0.01].sort_values(by='vacancy_share', ascending=False)

    return valid_cities

def adjust_column_widths(sheet, A, B, C, D, E):
    """Регулирует ширину столбцов в листе Excel."""
    column_widths = {
        'A': A,
        'B': B,
        'C': C,
        'D': D,
        'E': E,
    }

    for col, width in column_widths.items():
        sheet.column_dimensions[col].width = width

def set_thin_borders_for_non_empty_cells(sheet, start_row, end_row):
    """Устанавливает тонкие границы только для ячеек с данными в указанной строке."""
    thin_border = Border(
        left=Side(border_style="thin", color="000000"),
        right=Side(border_style="thin", color="000000"),
        top=Side(border_style="thin", color="000000"),
        bottom=Side(border_style="thin", color="000000")
    )

    for row in range(start_row, end_row + 1):
        for cell in sheet[row]:
            cell.border = thin_border

def set_bold_headers(sheet, header_row):
    """Делает заголовки жирным шрифтом в строке header_row."""
    bold_font = Font(bold=True)

    for cell in sheet[header_row]:
        cell.font = bold_font

def create_report():
    """Основная функция для создания отчета."""
    vacancies = load_data('vacancies.csv')

    wb = Workbook()

    sheet1 = wb.active
    sheet1.title = 'Статистика по годам'
    adjust_column_widths(sheet1, 6, 20, 20, 8, 8)
    years, avg_salaries, vacancy_counts = calculate_yearly_statistics(vacancies)
    write_yearly_statistics(sheet1, years, avg_salaries, vacancy_counts)
    set_bold_headers(sheet1, 1)
    set_thin_borders_for_non_empty_cells(sheet1, 1, 17)

    sheet2 = wb.create_sheet('Статистика по городам')
    adjust_column_widths(sheet2, 20, 20,2, 20, 20)
    valid_cities = calculate_city_statistics(vacancies)
    write_city_statistics(sheet2, valid_cities)
    set_bold_headers(sheet2, 1)
    set_thin_borders_for_non_empty_cells(sheet2, 1, 11)

    wb.save('report.xlsx')

def get_statistic_from_file(excel_file, vac):
    # Чтение данных из Excel
    all_stats = pd.read_csv(excel_file, header=None)
    all_stats.columns = ['name', 'salary_from', 'salary_to', 'currency', 'city', 'date']
    all_stats['avg_salary'] = all_stats[['salary_from', 'salary_to']].mean(axis=1)
    all_stats['avg_salary_name'] = all_stats['avg_salary']
    all_stats['year'] = pd.to_datetime(all_stats['date'], utc=True).dt.year

    # Извлекаем статистику по годам
    avg_salary_by_year = all_stats[['year', 'avg_salary']].groupby('year')['avg_salary'].apply(list)
    for year, salary in avg_salary_by_year.items():
        avg_salary_by_year[year] = int(round(sum(salary) / len(salary)))

    avg_salary_by_name = all_stats[all_stats['name'].str.contains(vac, case=False, na=False)].groupby('year')['avg_salary_name'].apply(list)
    for year, salary in avg_salary_by_name.items():
        avg_salary_by_name[year] = int(round(sum(salary) / len(salary)))
    # avg_salary_by_name = avg_salary_by_name[['avg_salary','year']].set_index('year')
    df_name_year = pd.merge(avg_salary_by_year, avg_salary_by_name, how="left", on=["year"])

    # vacancy_count_by_year = all_stats[['Год', 'Количество вакансий']].set_index('Год')

    # Извлекаем статистику по городам
    # city_salary = cities_df[['Город', 'Уровень зарплат']].set_index('Город').sort_values(by='Уровень зарплат', ascending=True)
    # city_vacancies = cities_df[['Город', 'Доля вакансий, %']].set_index('Город').sort_values(by='Доля вакансий, %', ascending=False)

    return df_name_year, avg_salary_by_year.fillna(0), avg_salary_by_name.fillna(0), [], [] # city_salary.fillna(0), city_vacancies.fillna(0)

def create_plot():
    csv_file = 'vacancies.csv'
    vac = "Python-разработчик" # input("Введите название профессии: ")

    # Получаем статистику
    df_name_year, avg_salary_by_year, avg_salary_by_name, city_salary, city_vacancies = get_statistic_from_file(csv_file, vac)

    # Фигура для подграфиков
    fig, sub = plt.subplots(2, 2)

    df_name = pd.DataFrame({
        "years": df_name_year.index.tolist(),
        "avg_salary_name": df_name_year['avg_salary_name'].tolist(),
        "avg_salary": df_name_year['avg_salary'].tolist()
    })

    # plt.barh(x=df_name["years"], y=df_name['avg_salary'], width=0.9, align='center')

    # 1. График: Уровень зарплат по годам
    X_axis = np.arange(len(X))
    sub[0, 0].bar(len(df_name.index.tolist())-0.2,
                  df_name['avg_salary'].tolist(),
                  label()
                  df_name.index,
                  label='Общий уровень зарплаты',
                  color='b')
    sub[0, 0].set_title("Уровень зарплат по годам")
    sub[0, 0].set_xlabel("Год")
    sub[0, 0].set_ylabel("Средняя зарплата")
    sub[0, 0].tick_params(axis='x', labelrotation=90)
    sub[0, 0].grid(True, axis='y')
    sub[0, 0].legend(loc='upper left')

    # 2. График: Количество вакансий по годам
    # sub[0, 1].plot(vacancy_count_by_year.index, vacancy_count_by_year['Количество вакансий'], label='Общее количество вакансий', color='green', marker='o')
    # sub[0, 1].set_title("Количество вакансий по годам")
    # sub[0, 1].set_xlabel("Год")
    # sub[0, 1].set_ylabel("Количество вакансий")
    # sub[0, 1].tick_params(axis='x', labelrotation=90)
    # sub[0, 1].grid(True)
    # sub[0, 1].legend(loc='upper left')

    # 3. График: Уровень зарплат по городам (горизонтальная диаграмма)
    # top_cities_salary = city_salary.head(10)
    #
    # sub[1, 0].barh(top_cities_salary.index, top_cities_salary["Уровень зарплат"], color='blue')
    # sub[1, 0].set_title("Уровень зарплат по городам")
    # sub[1, 0].tick_params(axis='y', labelsize=6)
    # sub[1, 0].tick_params(axis='x', labelsize=8)
    # sub[1, 0].grid(True, axis='x')

    # 4. График: Круговая диаграмма - количество вакансий по городам
    # other_vacancies = city_vacancies[10:].sum()
    # city_vacancies_top_10 = city_vacancies[:10]
    # city_vacancies_top_10 = pd.concat([city_vacancies_top_10, pd.Series({'Другие': other_vacancies})], ignore_index=True)
    #
    # # sub[1, 1].pie(city_vacancies_top_10['Доля вакансий, %'], labels=city_vacancies_top_10.index)
    # sub[1, 1].set_title("Количество вакансий по городам")

    # Отображение
    plt.tight_layout()
    plt.show()

    # return sub

create_plot()
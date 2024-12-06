import pandas as pd

# Загружаем данные
vacancies = pd.read_csv('vacancies_small.csv')

# Параметры фильтрации и сортировки
column = "area_name"  # input()
key = "Екатеринбург"  # input()
sort_by = "salary_from"  # input()
type_sort = "asc"  # input()

# Фильтрация строк по заданной подстроке (регистр не учитывается)
filtered_vacancies = vacancies[vacancies[column].str.contains(key, case=False, na=False)].copy()

ascending = type_sort == "asc"

# Сортировка по указанному столбцу и индексу
filtered_vacancies = filtered_vacancies.sort_values(
    by=[sort_by],  # Сначала сортируем по значению
    ascending=[ascending],  # Указанный порядок
    kind='mergesort'  # Используем стабильный алгоритм сортировки
)

# Если значения равны, используем сортировку по индексу
filtered_vacancies['original_index'] = filtered_vacancies.index
filtered_vacancies = filtered_vacancies.sort_values(
    by=[sort_by, 'original_index'],
    ascending=[ascending, True]
)

result = filtered_vacancies['name'].tolist()

print(result)
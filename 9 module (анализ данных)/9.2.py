# import pandas as pd
# from collections import Counter
#
# vacancies = pd.read_csv('vacancies_small.csv')
#
# name = input()
# sort_order = input()
#
# filtered_vacancies = vacancies[vacancies['name'].str.contains(name, case=False, na=False)]
#
# def print_sorter_skills(vacancies):
#
#     all_skills = []
#     for skills in vacancies['key_skills'].dropna():
#         all_skills.extend(skills.split('\r\n'))
#
#     skill_counts = Counter(all_skills)
#
#     sorted_skills = sorted(
#         skill_counts.items(),
#         key=lambda x: (x[1]) if sort_order == 'asc' else (-x[1])
#     )
#
#     print(sorted_skills[-6:])
#
# print_sorter_skills(filtered_vacancies)

import pandas as pd
from collections import Counter

# Чтение данных из CSV файла
vacancies = pd.read_csv('vacancies_small.csv')

# Ввод профессии и порядка сортировки
name = "программист"  # input("Введите название профессии: ")
sort_order = "asc" # input("Введите порядок сортировки (asc/desc): ")

# Фильтрация вакансий по заданной профессии (регистр не учитывается)
filtered_vacancies = vacancies[vacancies['name'].str.contains(name, case=False, na=False)].copy()

# Добавление столбца index с индексом строки
filtered_vacancies['index'] = filtered_vacancies.index

# Преобразуем столбец key_skills в список, разделяя по символу '\n'
filtered_vacancies['key_skills'] = filtered_vacancies['key_skills'].apply(lambda x: x.split('\n') if isinstance(x, str) else [])

# Собираем все скиллы и запоминаем первый индекс их появления
all_skills = []
skill_first_index = {}  # Словарь для хранения индекса первого появления скилла

for idx, skills in filtered_vacancies['key_skills'].items():
    for skill in skills:
        all_skills.append(skill)
        if skill not in skill_first_index:
            skill_first_index[skill] = idx

# Подсчитываем количество каждого скилла
skill_counts = Counter(all_skills)

# Сортировка скиллов
sorted_skills = sorted(
    skill_counts.items(),
    key=lambda x: (x[1], skill_first_index[x[0]]),  # Сортировка по частоте, затем по индексу первого появления
    reverse=(sort_order == 'asc')  # Если 'desc', то сортировка по убыванию
)

# Выводим топ-5 скиллов
top_skills = sorted_skills[:5]

print("Топ-5 скиллов:")
for skill, count in top_skills:
    print(f"{skill}: {count}")

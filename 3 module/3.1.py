import csv

headers, rows = [], []

with open("vacancies_for_learn_demo.csv", mode="r", encoding="utf-8-sig") as csvfile:

    csvreader = csv.reader(csvfile, delimiter=",")

    headers = next(csvreader)

    for row in csvreader:
        if len(row) == len(headers):
            rows.append(row)


print(headers)
print(rows)

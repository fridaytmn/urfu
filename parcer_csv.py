import csv

headers = []
rows = []

with open(input(), mode="r", encoding="utf-8-sig") as csvfile:
    csvreader = csv.reader(csvfile)

    headers = next(csvreader)

    for row in csvreader:
        if all(row):
            rows.append(row)

print(headers)
print(rows)

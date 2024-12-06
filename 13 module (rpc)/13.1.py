from xmlrpc.server import SimpleXMLRPCServer
import pandas as pd

data = pd.read_csv('vacancies.csv')
data["index"] = data.index
data.columns = ["name", "salary_from", "salary_to", "valute", "city", "date", "ID"]

def get_vacancy_by_id(id):
    vacancy = data[data["ID"] == vacancy_id]
    if not vacancy.empty:
        row = vacancy.iloc[0]
        return {
            "Название вакансии": row["name"],
            "Зарплата от": row["salary_from"],
            "Зарплата до": row["salary_to"],
            "Город": row["city"]
        }
    return "Вакансия с указанным ID не найдена."

def get_vacancies_by_city(city):
    vacancies = data[data["city"] == city]
    if not vacancies.empty:
        result = {}
        for _, row in vacancies.iterrows():
            print(row[0])
            result[str(row["ID"])] = {
                "Название вакансии": row["name"],
                "Зарплата от": row["salary_from"],
                "Зарплата до": row["salary_to"],
                "Город": row["city"]
            }
        return result
    return "Вакансии в указанном городе не найдены."

def get_vacancies_by_min_salary(salary):
    vacancies = data[data["salary_from"] >= min_salary]
    if not vacancies.empty:
        result = {}
        for _, row in vacancies.iterrows():
            result[str(row["ID"])] = {
                "Название вакансии": row["name"],
                "Зарплата от": row["salary_from"],
                "Зарплата до": row["salary_to"],
                "Город": row["city"]
            }
        return result
    return "Вакансии с указанной минимальной зарплатой не найдены."

def exit_server():
    print("Сервер завершает работу.")
    server.shutdown()
    return True

def start_server():

    server = SimpleXMLRPCServer(("localhost", 8000))

    server.register_function(get_vacancy_by_id, "get_vacancy_by_id")
    server.register_function(get_vacancies_by_city, "get_vacancies_by_city")
    server.register_function(get_vacancies_by_min_salary, "get_vacancies_by_min_salary")
    server.register_function(exit_server, "exit")

    server.serve_forever()


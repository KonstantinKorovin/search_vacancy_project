import datetime

from src.hh import HH
from src.vacancy import Vacancy


def legit_vacancies(keyword=None, page=1, per_page=50):
    """
    Получение вакансий
    """
    return HH(page=page, per_page=per_page, keyword=keyword).get_vacancies()


def vacancies(hh_list):
    """
    Преобразователь
    """
    return Vacancy.load_vacancy(hh_list)


def key_sorted_function(item):
    """
    Получение значений для сортировки списка по зарплате
    """
    salary = item.get("salary")

    if not salary:
        return 0

    if salary["from"] and salary["to"]:
        return (salary["from"] + salary["to"]) // 2
    elif salary["from"] and not salary["to"]:
        return salary["from"]
    elif salary["to"] and not salary["from"]:
        return salary["to"]


def sorted_vacancy(sorted_list, ascending=True):
    """
    Сортировка списка по зарплате
    """
    return sorted(sorted_list, key=key_sorted_function, reverse=ascending)


def salary_range(range_list, data_range):
    """
    Диапазон зарплат
    """
    salary_list = []
    salary = tuple(map(int, data_range.replace(" ", "").split("-")))
    if len(salary) == 1:
        salary = salary[0]
    for stack in range_list:
        vacancies_salary = stack["salary"]

        if vacancies_salary and isinstance(salary, int):

            if vacancies_salary["from"] and vacancies_salary["to"]:
                if salary <= vacancies_salary["from"]:
                    salary_list.append(stack)
            elif vacancies_salary["from"] and not vacancies_salary["to"]:
                if salary <= vacancies_salary["from"]:
                    salary_list.append(stack)
            elif not vacancies_salary["from"] and vacancies_salary["to"]:
                if salary <= vacancies_salary["to"]:
                    salary_list.append(stack)

        elif vacancies_salary and isinstance(salary, tuple) and len(salary) == 2:

            if vacancies_salary["from"] and vacancies_salary["to"]:
                if salary[0] <= vacancies_salary["from"] and vacancies_salary["to"] <= salary[1]:
                    salary_list.append(stack)
            elif vacancies_salary["from"] and not vacancies_salary["to"]:
                if salary[0] <= vacancies_salary["from"] <= salary[1]:
                    salary_list.append(stack)
            elif not vacancies_salary["from"] and vacancies_salary["to"]:
                if salary[0] <= vacancies_salary["to"] <= salary[1]:
                    salary_list.append(stack)
        elif vacancies_salary and isinstance(salary, tuple) and len(salary) > 2:
            return "Некорректное значение зарплаты!"
    return salary_list


def load_vacancies(search_list):
    """
    Пользовательский формат вакансий
    """
    id_vacancy = 1
    vacancy_string = ""
    for stack in search_list:
        vacancy_string += (
            f"{id_vacancy}: "
            f"{stack["Вакансия"]}, "
            f"{stack["Местоположение"]}, "
            f"{stack["Опыт"]}, {stack["Зарплата"]}, "
            f"{stack["Валюта"]}, {stack["Ссылка на вакансию"]}, "
            f"{stack["Общая информация"]}\n__--____--__\n"
        )
        id_vacancy += 1
    return vacancy_string


def greeting_function():
    date_time = datetime.datetime.now().time()
    if datetime.time(5, 0, 0) <= date_time < datetime.time(11, 0, 0):
        return "Доброе утро!"
    elif datetime.time(11, 0, 0) <= date_time < datetime.time(17, 0, 0):
        return "Добрый день!"
    elif datetime.time(17, 0, 0) <= date_time < datetime.time(23, 0, 0):
        return "Добрый вечер!"
    else:
        return "Доброй ночи!"

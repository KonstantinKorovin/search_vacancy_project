import json

import requests
from abc import abstractmethod, ABC


class AbstractHH(ABC):
    """Класс для взаимодействия с API"""

    @abstractmethod
    def result_api(self):
        pass


class ApiHh(AbstractHH):
    """Инициализация"""

    def __init__(self, page=None, per_page=None, text=None, currency=None, salary=None):
        self.__text = text
        self.__page = page
        self.__per_page = per_page
        self.__currency = currency
        self.__salary = salary
        self.__url = "https://api.hh.ru/vacancies"
        self.__params = {
            "text": text, "page": page, "per_page": per_page, "currency": currency, "salary": salary
        }

    @property
    def __connect_api(self):
        """Подключение к API"""
        response = requests.get(self.__url, params=self.__params)
        return response

    @property
    def result_api(self):
        """Получение результата запроса"""
        result = self.__connect_api
        status_code = result.status_code
        if status_code != 200:
            return f"Ошибка {status_code}!"
        return result.text


class Vacancy(ApiHh):
    """Класс представления вакансий"""

    @property
    def __load_vacancy(self):
        """Парсинг json вакансий в список словарей"""
        return json.loads(self.result_api).get('items')

    @property
    def using_vacation(self):
        """Получение нужных значений из списка с вакансиями"""
        new_vacancy_list = []
        for x in self.__load_vacancy:
            name = x['name']
            area = x['area']['name']
            if x['experience']:
                experience = x['experience']['name']
            else:
                experience = 'Без указания опыта'
            if x['salary']:
                salary = x['salary']
                if salary['from'] and salary['to']:
                    salary = f"от {salary['from']} до {salary['to']}"
                elif not salary['from'] and salary['to']:
                    salary = f"до {salary['to']}"
                else:
                    salary = f"от {salary['from']}"
            else:
                salary = 'Зарплата не указана'
            if x['alternate_url']:
                alternate_url = x['alternate_url']
            else:
                alternate_url = 'Ссылка отсутствует или больше не существует'
            if x['snippet']:
                snippet = x['snippet']['requirement']
            else:
                snippet = 'Информация не указана'
            new_vacancy_list.append(
                {
                'Название вакансии': name,
                'Местоположение': area,
                'Опыт работы': experience,
                'Зарплата': salary,
                'Ссылка на вакансию': alternate_url,
                'Информация': snippet
                }
            )
        return new_vacancy_list




v = Vacancy(text='Менеджер')
print(v.using_vacation)
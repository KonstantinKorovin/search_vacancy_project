import json
from abc import ABC, abstractmethod

import requests


class BaseHH(ABC):
    """
    Класс-представитель
    """

    @abstractmethod
    def get_vacancies(self):
        pass


class HH(BaseHH):
    """
    Класс для работы с API HeadHunter
    """

    __slots__ = ("__page", "__per_page", "__url", "__params", "__vacancies")

    def __init__(self, page=None, per_page=None, keyword=None):
        self.__page = page
        self.__per_page = per_page
        self.__url = "https://api.hh.ru/vacancies"
        self.__params = {"text": keyword, "page": self.__page, "per_page": self.__per_page}
        self.__vacancies = []

    def __connect_api(self):
        """
        Подключение к API
        """
        return requests.get(self.__url, self.__params)

    def get_vacancies(self):
        """
        Получение результата запроса
        """
        try:
            result = self.__connect_api()
            if result.status_code != 200:
                return f"Ошибка {result.status_code}!"
            return json.loads(result.text).get("items")
        except requests.exceptions.MissingSchema:
            print("Пожайлуста убедитесь что вы передаете правильный адрес!")
        except requests.exceptions.InvalidSchema:
            print("Ваш запрос не соответсвует схеме!")

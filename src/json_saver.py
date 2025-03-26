import json
import os.path
import re
from abc import ABC, abstractmethod
from typing import Any

from src.vacancy import Vacancy


class BaseJsonSaver(ABC):
    """
    Класс-представитель
    """

    @abstractmethod
    def json_file_reader(self, path=None):
        pass

    @abstractmethod
    def json_file_parser(self, vacancy_example, path=None):
        pass

    @abstractmethod
    def json_file_deleter(self, name=None, path=None):
        pass


path_json = os.path.abspath(__file__)
src_dir = os.path.dirname(path_json)
data_path = os.path.join(os.path.dirname(src_dir), "data")
PATH_TO_JSON = os.path.join(data_path, "vacancies.json")


class JsonSaver(BaseJsonSaver):
    """
    Сохранение вакансий в json файл
    """

    __slots__ = "__base_path"

    def __init__(self):

        self.__base_path = PATH_TO_JSON

    def __json_validate(self, path: Any = None) -> str:
        """
        Валидация пути к файлу
        """
        if path is None:
            return self.__base_path
        elif not isinstance(path, str):
            raise TypeError("Путь к файлу должен иметь тип str!")
        elif not path.endswith(".json"):
            raise ValueError(
                "Для взайимодействия с json-файлом полученный вами путь должен иметь соответствующий префикс!"
            )
        return path

    def json_file_reader(self, path: Any = None) -> list:
        """
        Чтение файла
        """
        legit_path = self.__json_validate(path)
        try:
            with open(legit_path, "r", encoding="utf-8") as file:
                return json.load(file) or []
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def json_file_parser(self, vacancy_example: Any, path: Any = None) -> str:
        """
        Парсинг данных
        """
        legit_path = self.__json_validate(path)
        vacancies = self.json_file_reader(legit_path)
        if not isinstance(vacancies, list):
            return "На вход получены не корректные данные, проверьте правильность указанного пути!"
        else:
            with open(legit_path, "r+", encoding="utf-8") as file:
                if isinstance(vacancy_example, Vacancy):
                    vacancy_example = self.__to_dict(vacancy_example)
                    if vacancy_example not in vacancies:
                        vacancies.append(vacancy_example)
                        json.dump(vacancies, file, ensure_ascii=False, indent=4)
                        return "Запись в файл..."
                    else:
                        return "Вакансия уже есть в списке!"

                elif isinstance(vacancy_example, list):
                    counter = 0
                    if vacancy_example:
                        for stack in vacancy_example:
                            if stack not in vacancies:
                                vacancies.append(stack)
                                counter += 1
                            else:
                                continue
                        json.dump(vacancies, file, ensure_ascii=False, indent=4)
                        if counter > 0:
                            return "Запись в файл..."
                        else:
                            return "Вы передаете вакансии которые уже есть в списке!"
                    else:
                        return "Вы передаете пустой список!"

                elif isinstance(vacancy_example, dict):
                    if vacancy_example not in vacancies:
                        vacancies.append(vacancy_example)
                        json.dump(vacancies, file, ensure_ascii=False, indent=4)
                        if len(vacancies) > len(self.json_file_reader(legit_path)):
                            return "Запись в файл..."
                        else:
                            return "В файл ничего не записалось, полученные вами вакансии уже есть в файле!"
                    else:
                        return "Вакансия уже есть в списке!"
                else:
                    return "Критическая ошибка при попытке добавления вакансии, попробуйте снова!"

    @staticmethod
    def __to_dict(example: Any) -> dict:
        """
        Преобразователь
        """
        return dict(ex.split(": ") for ex in str(example).split(", "))

    def json_file_deleter(self, name: Any = None, path: Any = None) -> str:
        """
        Делитер
        """
        legit_path = self.__json_validate(path)
        vacancies = self.json_file_reader(legit_path)
        if os.stat(legit_path).st_size == 0:
            return "Тут и так пусто!"

        if name is None:
            with open(legit_path, "r+", encoding="utf-8") as file:
                file.truncate(0)
            return "Содержимое файла удалено навсегда!"
        elif name is not None:
            status = False
            vacancies = [
                stack
                for stack in vacancies
                if not re.findall(name.replace(" ", ""), stack.get("Вакансия"), flags=re.I)
            ]
            if len(vacancies) < len(self.json_file_reader(legit_path)):
                status = True
            if vacancies:
                with open(legit_path, "w", encoding="utf-8") as file:
                    json.dump(vacancies, file, ensure_ascii=False, indent=4)
            else:
                with open(legit_path, "r+", encoding="utf-8") as file:
                    file.truncate(0)
            if status:
                return "Удаление вакансий..."
            else:
                return "Ничего не найдено!"
        else:
            return "Критическая ошибка работы программы, попробуйте снова!"

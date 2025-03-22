from src.cls_exceptions import AreaException, NameException, SalaryZeroException


class Vacancy:
    """
    Радота с вакансиями
    """

    __slots__ = (
        "__name",
        "__area",
        "__experience",
        "__salary_from",
        "__salary_to",
        "__currency",
        "__alternate_url",
        "__snippet",
    )

    def __init__(
        self, name, area, experience, salary_from=None, salary_to=None, currency=None, alternate_url=None, snippet=None
    ):
        self.__name = name
        self.__area = area
        self.__experience = experience
        self.__salary_from = salary_from if salary_from else 0
        self.__salary_to = salary_to if salary_to else 0
        self.__currency = currency if currency else "RUR"
        self.__alternate_url = alternate_url if alternate_url else "Ссылка отсутствует"
        self.__snippet = snippet if snippet else "Требования не указаны"

        self.__validate_vacancies()
        self.__validate_salary()

    def __validate_vacancies(self):
        """
        Валидация обязательных для вакансии атрибутов
        """
        if not self.__name:
            raise NameException
        if not self.__area:
            raise AreaException

    def __validate_salary(self):
        """
        Валидация диапазона зарплат
        """
        if not isinstance(self.__salary_from, int) or not isinstance(self.__salary_to, int):
            raise ValueError("Не валидные данные")
        if self.__salary_from < 0 or self.__salary_to < 0:
            raise SalaryZeroException

    def __str__(self):
        """
        Форматирование
        """
        result = (
            f"Вакансия: {self.__name}, "
            f"Местоположение: {self.__area}, "
            f"Опыт: {self.__experience}, "
            f"Зарплата: {self.__get_salary()}, "
            f"Валюта: {self.__currency if self.__get_salary() != "Зарплата не указана" else "Не указано"}, "
            f"Ссылка на вакансию: {self.__alternate_url}, "
            f"Общая информация: {self.__snippet}"
        )
        return result

    @classmethod
    def __isinstance_function(cls, other):
        if isinstance(other, (list, dict, tuple, set)):
            raise ValueError("Значение справа является не валидным!")

    def __gt__(self, other):
        """
        Сравнение вакансий по минимальной зарплате
        """
        other_object = self.__isinstance_function(other)
        return self.__salary_from > other_object

    def __eq__(self, other):
        """
        Сравнение вакансий по минимальной зарплате
        """
        other_object = self.__isinstance_function(other)
        return self.__salary_from == other_object

    def __get_salary(self):
        """
        Установка значений зарплатного диапазона
        """
        if not self.__salary_from and not self.__salary_to:
            return "Зарплата не указана"
        if not self.__salary_from:
            return f"до {self.__salary_to}"
        if not self.__salary_to:
            return f"от {self.__salary_from}"
        if self.__salary_from == self.__salary_to:
            return self.__salary_from
        else:
            return f"от {self.__salary_from} до {self.__salary_to}"

    @staticmethod
    def load_vacancy(data):
        """
        Получение нужного по критериям списка вакансий
        """
        vacancies = []
        for stack in data:
            name = stack.get("name")
            area = stack.get("area", {}).get("name")
            experience = stack.get("experience", {}).get("name")
            salary_from = stack.get("salary", {}).get("from") if stack.get("salary") else 0
            salary_to = stack.get("salary", {}).get("to") if stack.get("salary") else 0
            currency = stack.get("salary", {}).get("currency") if stack.get("salary") else "RUR"
            alternate_url = stack.get("alternate_url") if stack.get("alternate_url") else "Ссылка отсутствует"
            snippet = (
                stack.get("snippet", {}).get("responsibility") if stack.get("snippet") else "Требования не указаны"
            )
            vacancy = Vacancy(
                name=name,
                area=area,
                experience=experience,
                salary_from=salary_from,
                salary_to=salary_to,
                currency=currency,
                alternate_url=alternate_url,
                snippet=snippet,
            )
            vacancies.append(vacancy.__to_dict())
        return vacancies

    def __to_dict(self):
        """
        Приведение вакансий к более удобному формату
        """
        return {
            "Вакансия": self.__name,
            "Местоположение": self.__area,
            "Опыт": self.__experience,
            "Зарплата": self.__get_salary(),
            "Валюта": self.__currency if self.__get_salary() != "Зарплата не указана" else "Не указано",
            "Ссылка на вакансию": self.__alternate_url,
            "Общая информация": self.__snippet,
        }

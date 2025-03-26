import pytest

from src.cls_exceptions import AreaException, NameException, SalaryZeroException
from src.vacancy import Vacancy


def test_low_vacancy():
    """
    Тест метода __str__
    """
    vacancy = Vacancy("Менеджер", "Москва", "от 1 до 3 лет", 100000, 150000)
    assert str(vacancy) == (
        "Вакансия: Менеджер, "
        "Местоположение: Москва, "
        "Опыт: от 1 до 3 лет, "
        "Зарплата: от 100000 до 150000, "
        "Валюта: RUR, "
        "Ссылка на вакансию: Ссылка отсутствует, "
        "Общая информация: Требования не указаны"
    )


def test_max_vacancy():
    """
    Тест метода __str__
    """
    vacancy = Vacancy(
        "Разработчик", "Екатеринбург", "Без опыта", 150000, 200000, "UZC", "https://12345", "Требуется разработчик"
    )
    assert str(vacancy) == (
        "Вакансия: Разработчик, "
        "Местоположение: Екатеринбург, "
        "Опыт: Без опыта, "
        "Зарплата: от 150000 до 200000, "
        "Валюта: UZC, "
        "Ссылка на вакансию: https://12345, "
        "Общая информация: Требуется разработчик"
    )


def test_load_vacancies():
    """
    Тест метода load_vacancy
    """
    assert Vacancy.load_vacancy(1) == "Данные не валидны!"
    assert Vacancy.load_vacancy([]) == []


def test_value_error():
    with pytest.raises(ValueError):
        assert (
            Vacancy(name="name", area="area", experience="experience", salary_from="100000", salary_to="150000")
            == "Не валидные данные"
        )


def test_raise_name():
    with pytest.raises(NameException):
        assert (
            Vacancy(name=None, area="Москва", experience="от 1 до 3 лет") == "Название вакансии не может быть пустым!"
        )


def test_raise_area():
    with pytest.raises(AreaException):
        assert (
            Vacancy(name="Менеджер", area=None, experience="от 1 до 3 лет") == "Название города не может быть пустым!"
        )


def test_raise_salary_from():
    with pytest.raises(SalaryZeroException):
        assert Vacancy("Менеджер", "Москва", "от 1 до 3 лет", -100, 100) == "Зарплата не может быть меньше нуля!"


def test_raise_salary_to():
    with pytest.raises(SalaryZeroException):
        assert Vacancy("Менеджер", "Москва", "от 1 до 3 лет", 100, -100) == "Зарплата не может быть меньше нуля!"


@pytest.mark.parametrize(
    "result, expected",
    [
        (
            Vacancy.load_vacancy(
                [
                    {
                        "name": "1",
                        "area": {"name": "2"},
                        "experience": {"name": "3"},
                        "salary": {"from": None, "to": None, "currency": None},
                        "alternate_url": None,
                        "snippet": {"responsibility": None},
                    }
                ]
            ),
            [
                {
                    "Вакансия": "1",
                    "Местоположение": "2",
                    "Опыт": "3",
                    "Зарплата": "Зарплата не указана",
                    "Валюта": "Не указано",
                    "Ссылка на вакансию": "Ссылка отсутствует",
                    "Общая информация": "Требования не указаны",
                }
            ],
        ),
        (
            Vacancy.load_vacancy(
                [
                    {
                        "name": "Разработчик",
                        "area": {"name": "Москва"},
                        "experience": {"name": "От 1 до 3 лет"},
                        "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
                        "alternate_url": "https://lfwfew",
                        "snippet": {"responsibility": "Требуется разработчик"},
                    }
                ]
            ),
            [
                {
                    "Вакансия": "Разработчик",
                    "Местоположение": "Москва",
                    "Опыт": "От 1 до 3 лет",
                    "Зарплата": "от 100000 до 150000",
                    "Валюта": "RUR",
                    "Ссылка на вакансию": "https://lfwfew",
                    "Общая информация": "Требуется разработчик",
                }
            ],
        ),
    ],
)
def test_parametrize(result, expected):
    assert result == expected

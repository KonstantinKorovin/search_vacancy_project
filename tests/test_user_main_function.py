import unittest
from unittest.mock import Mock, patch

from src.user_main_function import (
    key_sorted_function,
    load_vacancies,
    salary_range,
    sorted_vacancy,
    vacancies,
)
from src.vacancy import Vacancy


class TestUserMainFunction(unittest.TestCase):

    def setUp(self):
        """Подготовка перед каждым тестом."""
        self.sample_vacancy_data = [
            {
                "id": "1",
                "name": "Python Developer",
                "area": {"name": "Moscow"},
                "experience": {"name": "1-3 years"},
                "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
                "alternate_url": "https://example.com/vacancy1",
                "snippet": {"responsibility": "Develop software"},
            },
            {
                "id": "2",
                "name": "Java Developer",
                "area": {"name": "SPb"},
                "experience": {"name": "3-6 years"},
                "salary": {"from": 120000, "to": None, "currency": "RUR"},
                "alternate_url": "https://example.com/vacancy2",
                "snippet": {"responsibility": "Develop backend"},
            },
        ]

    @patch("src.vacancy.Vacancy.load_vacancy")
    def test_vacancies(self, mock_load_vacancy):
        """Тест преобразования данных в объекты Vacancy."""
        mock_load_vacancy.return_value = [Mock(spec=Vacancy), Mock(spec=Vacancy)]
        result = vacancies(self.sample_vacancy_data)
        self.assertEqual(len(result), 2)
        mock_load_vacancy.assert_called_once_with(self.sample_vacancy_data)

    def test_key_sorted_function(self):
        """Тест функции сортировки по зарплате."""
        item1 = {"salary": {"from": 100000, "to": 150000}}
        item2 = {"salary": {"from": 120000, "to": None}}
        item3 = {"salary": None}
        self.assertEqual(key_sorted_function(item1), 125000)
        self.assertEqual(key_sorted_function(item2), 120000)
        self.assertEqual(key_sorted_function(item3), 0)

    def test_sorted_vacancy(self):
        """Тест сортировки вакансий."""
        vacancies_data = [
            {"salary": {"from": 100000, "to": 150000}},
            {"salary": {"from": 120000, "to": None}},
            {"salary": None},
        ]
        result_asc = sorted_vacancy(vacancies_data, ascending=True)
        result_desc = sorted_vacancy(vacancies_data, ascending=False)
        self.assertEqual(key_sorted_function(result_asc[0]), 125000)
        self.assertEqual(key_sorted_function(result_desc[0]), 0)

    def test_salary_range_single_value(self):
        """Тест фильтрации по зарплате с одним значением."""
        vacancies_data = [
            {"salary": {"from": 100000, "to": 150000}},
            {"salary": {"from": 80000, "to": None}},
            {"salary": None},
        ]
        result = salary_range(vacancies_data, "90000")
        self.assertEqual(len(result), 1)

    def test_salary_range_range_value(self):
        """Тест фильтрации по диапазону зарплат."""
        vacancies_data = [
            {"salary": {"from": 100000, "to": 150000}},
            {"salary": {"from": 80000, "to": None}},
            {"salary": None},
        ]
        result = salary_range(vacancies_data, "90000-120000")
        self.assertEqual(len(result), 0)

    def test_salary_range_invalid_range(self):
        """Тест обработки некорректного диапазона зарплат."""
        vacancies_data = [{"salary": {"from": 100000, "to": 150000}}]
        result = salary_range(vacancies_data, "90000-120000-150000")
        self.assertEqual(result, "Некорректное значение зарплаты!")

    def test_load_vacancies(self):
        """Тест форматирования вакансий в строку."""
        vacancies_data = [
            {
                "Вакансия": "Python Developer",
                "Местоположение": "Moscow",
                "Опыт": "1-3 years",
                "Зарплата": "100000-150000",
                "Валюта": "RUR",
                "Ссылка на вакансию": "https://example.com",
                "Общая информация": "Develop software",
            },
            {
                "Вакансия": "Java Developer",
                "Местоположение": "Moscow",
                "Опыт": "3-6 years",
                "Зарплата": "250000-300000",
                "Валюта": "RUR",
                "Ссылка на вакансию": "https://example1.com",
                "Общая информация": "Develop software",
            },
        ]
        result = load_vacancies(vacancies_data)
        expected = (
            "1: Python Developer, Moscow, 1-3 years, 100000-150000, RUR, "
            "https://example.com, Develop software\n"
            "__--____--__\n"
            "2: Java Developer, Moscow, 3-6 years, 250000-300000, RUR, "
            "https://example1.com, Develop software\n"
            "__--____--__\n"
        )
        self.assertEqual(result, expected)

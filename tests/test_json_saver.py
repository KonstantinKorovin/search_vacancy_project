import json
import os
import unittest

from src.json_saver import JsonSaver
from src.vacancy import Vacancy


class TestJsonSaver(unittest.TestCase):
    def setUp(self):
        """Подготовка перед каждым тестом: создание временного JSON-файла."""
        self.test_file = "test_vacancies.json"
        self.json_saver = JsonSaver()
        # Устанавливаем тестовый путь
        self.json_saver._JsonSaver__base_path = self.test_file
        # Создаем пустой файл
        with open(self.test_file, "w", encoding="utf-8") as f:
            json.dump([], f)

    def tearDown(self):
        """Очистка после каждого теста: удаление временного файла."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_json_validate_valid_path(self):
        """Тест валидации корректного пути."""
        path = "valid_path.json"
        result = self.json_saver._JsonSaver__json_validate(path)
        self.assertEqual(result, path)

    def test_json_validate_invalid_type(self):
        """Тест валидации пути с некорректным типом."""
        with self.assertRaises(TypeError):
            self.json_saver._JsonSaver__json_validate(123)

    def test_json_validate_invalid_extension(self):
        """Тест валидации пути с некорректным расширением."""
        with self.assertRaises(ValueError):
            self.json_saver._JsonSaver__json_validate("file.txt")

    def test_json_file_reader_empty_file(self):
        """Тест чтения пустого файла."""
        result = self.json_saver.json_file_reader(self.test_file)
        self.assertEqual(result, [])

    def test_json_file_reader_non_empty_file(self):
        """Тест чтения файла с данными."""
        test_data = [{"Вакансия": "Python Developer"}]
        with open(self.test_file, "w", encoding="utf-8") as f:
            json.dump(test_data, f)
        result = self.json_saver.json_file_reader(self.test_file)
        self.assertEqual(result, test_data)

    def test_json_file_parser_single_vacancy(self):
        """Тест добавления одной вакансии."""
        vacancy = Vacancy("Python Developer", "Москва", "От 1 до 3 лет", 100000, 150000, "Test link")
        result = self.json_saver.json_file_parser(vacancy, self.test_file)
        self.assertEqual(result, "Запись в файл...")
        data = self.json_saver.json_file_reader(self.test_file)
        self.assertEqual(len(data), 1)

    def test_json_file_parser_duplicate_vacancy(self):
        """Тест добавления дублирующейся вакансии."""
        vacancy = Vacancy("Python Developer", "Екатеринбург", "Без опыта", 200000, 250000, "Test link")
        self.json_saver.json_file_parser(vacancy, self.test_file)
        result = self.json_saver.json_file_parser(vacancy, self.test_file)
        self.assertEqual(result, "Вакансия уже есть в списке!")
        data = self.json_saver.json_file_reader(self.test_file)
        self.assertEqual(len(data), 1)

    def test_json_file_parser_list_vacancies(self):
        """Тест добавления списка вакансий."""
        vacancies = [
            {"Вакансия": "Python Developer", "Зарплата": "100000", "Описание": "Test", "Ссылка": "Link"},
            {"Вакансия": "Java Developer", "Зарплата": "120000", "Описание": "Test", "Ссылка": "Link"},
        ]
        result = self.json_saver.json_file_parser(vacancies, self.test_file)
        self.assertEqual(result, "Запись в файл...")
        data = self.json_saver.json_file_reader(self.test_file)
        self.assertEqual(len(data), 2)

    def test_json_file_deleter_all(self):
        """Тест удаления всего содержимого файла."""
        test_data = [{"Вакансия": "Python Developer"}]
        with open(self.test_file, "w", encoding="utf-8") as f:
            json.dump(test_data, f)
        result = self.json_saver.json_file_deleter(path=self.test_file)
        self.assertEqual(result, "Содержимое файла удалено навсегда!")
        data = self.json_saver.json_file_reader(self.test_file)
        self.assertEqual(data, [])

    def test_json_file_deleter_by_name(self):
        """Тест удаления вакансии по имени."""
        test_data = [{"Вакансия": "Python Developer"}, {"Вакансия": "Java Developer"}]
        with open(self.test_file, "w", encoding="utf-8") as f:
            json.dump(test_data, f)
        result = self.json_saver.json_file_deleter(name="Python", path=self.test_file)
        self.assertEqual(result, "Удаление вакансий...")
        data = self.json_saver.json_file_reader(self.test_file)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["Вакансия"], "Java Developer")

    def test_json_file_deleter_not_found(self):
        """Тест попытки удаления несуществующей вакансии."""
        test_data = [{"Вакансия": "Python Developer"}]
        with open(self.test_file, "w", encoding="utf-8") as f:
            json.dump(test_data, f)
        result = self.json_saver.json_file_deleter(name="NonExistent", path=self.test_file)
        self.assertEqual(result, "Ничего не найдено!")
        data = self.json_saver.json_file_reader(self.test_file)
        self.assertEqual(len(data), 1)

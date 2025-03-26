import re
import random
import time
from json import JSONDecodeError

from src.json_saver import JsonSaver, PATH_TO_JSON
from src.user_main_function import greeting_function, legit_vacancies, vacancies, load_vacancies, salary_range, \
    sorted_vacancy
from src.vacancy import Vacancy
from typing import Any


def watch(user_input: Any) -> list | str:
    """
    Просмотр вакансий
    """
    try:
        if re.fullmatch(r"\d+", user_input):
            return load_vacancies(vacancies(legit_vacancies(page=user_input)))
        elif not re.fullmatch(r"\d+", user_input) \
                and not re.fullmatch("exit", user_input, flags=re.I):
            return "Номер страницы может представлять из себя только число!"
        else:
            return []

    except (AttributeError, TypeError):
        return f"Пожалуйста указывайте корректный номер страницы, например ({random.randint(1, 39)})"


def key_vacancies(key_word: Any) -> list:
    """
    Сортировка вакансий по ключевому слову
    """
    if re.fullmatch("Да", key_word, flags=re.I):
        while True:
            print("Введите информацию через пробел:")
            text_input = input()
            keyword = text_input if text_input != "" else None
            watching = legit_vacancies(keyword=keyword)
            if not watching:
                print("Ничего не нашлось, попробуйте снова!")
            else:
                return watching
    elif re.fullmatch("Нет", key_word, flags=re.I):
        return legit_vacancies()
    else:
        print("Введите Да или Нет!")
        return []


def filter_vacancies(filter_word: Any, filter_list: list) -> list:
    """
    Сортировка вакансий по ключевому слову
    """
    if re.fullmatch("Да", filter_word, flags=re.I):
        while True:
            print("Введите вилку зарплат через (-), или укажите одним числом минимальный порог зарплаты:")
            salary_input = input()
            filtered_list = salary_range(filter_list, salary_input)
            if not filtered_list:
                print("Ничего не нашлось, попробуйте снова!")
            else:
                return filtered_list
    elif re.fullmatch("Нет", filter_word, flags=re.I):
        return filter_list
    else:
        print("Введите Да или Нет!")
        return []


def sorted_vacancies(sorted_word: Any, sorted_list: list) -> list:
    """
    Сортировка вакансий по ключевому слову
    """
    if re.fullmatch("Да", sorted_word, flags=re.I):
        while True:
            print("Отсортировать по возрастанию или по убыванию?")
            sorted_input = input()
            if re.fullmatch("по возрастанию", sorted_input, flags=re.I):
                return sorted_vacancy(sorted_list, ascending=False)
            elif re.fullmatch("по убыванию", sorted_input, flags=re.I):
                return sorted_vacancy(sorted_list, ascending=True)
            else:
                print("Введите по возрастанию или по убыванию!")
    elif re.fullmatch("Нет", sorted_word, flags=re.I):
        return sorted_list
    else:
        print("Введите Да или Нет!")
        return []


def file_worker(file_word: Any, file_list: list) -> list | str:
    """
    Работа с файлом
    """
    if re.fullmatch("1", file_word):
        while True:
            print("Укажите путь к файлу, можете оставить поле пустым и вакансии сохранятся в файл по умолчанию:")
            path_input = input()

            true_path = path_input if path_input != "" else PATH_TO_JSON

            try:
                if isinstance(file_list, Vacancy):
                    saver = JsonSaver().json_file_parser(file_list, true_path)
                elif isinstance(file_list, list):
                    saver = JsonSaver().json_file_parser(Vacancy.load_vacancy(file_list), true_path)
                else:
                    print("Некорректный тип данных file_list")
                    return []

                if saver != "Запись в файл...":
                    print(saver)
                    return "Попробуйте снова!"
                else:
                    print(saver)
                    return f"Вакансии сохранены в файл по умолчанию, путь: {PATH_TO_JSON}"

            except (FileNotFoundError, JSONDecodeError):
                print(
                    "Ошибка чтения файла, Убедитесь в существовании файла, или в том что вы передаете правильный путь!"
                )
                return []
    elif re.fullmatch("2", file_word):
        print("Укажите путь к файлу, можете оставить поле пустым и вакансии сохранятся в файл по умолчанию:")
        file_input = input()

        true_path = file_input if file_input != "" else PATH_TO_JSON

        try:
            file_data = JsonSaver().json_file_reader(true_path)
            if not file_data:
                print("Файл пуст!")
            else:
                print("Хотите ли вы что-нибудь удалить? Введите Да или Нет:")
            del_input = input()

            if re.fullmatch("Нет", del_input, flags=re.I):
                print("Выход из блока удаления вакансий...")
                return "Хорошего дня!"
            elif re.fullmatch("Да", del_input, flags=re.I):
                print("""Хотите передать название вакансии, или удалить все содержимое файла? Введите 1 или 2:""")
                del_input_one = input()
                if re.fullmatch("1", del_input_one):
                    print("Введите название вакансии:")

                    vacancy_input = input()
                    print(JsonSaver().json_file_deleter(vacancy_input, true_path))
                    return "Удаление вакансий..."
                elif re.fullmatch("2", del_input_one):
                    print(JsonSaver().json_file_deleter(path=true_path))
                    return "Очистка файла..."
                else:
                    print("Ошибка удаления!")
                    return "Попробуйте снова!"
            else:
                print("Введите Да или Нет!")
                return "Попробуйте снова!"

        except (FileNotFoundError, JSONDecodeError):
            print("Файл не существует!")
            return []
    elif re.fullmatch("exit", file_word, flags=re.I):
        return "Выхожу из программы..."
    else:
        print("Введите 1 или 2!")
        return []


def finally_user_function(finally_word: Any) -> list | str:
    """
    Результат работы программы
    """
    if re.fullmatch("exit", finally_word, flags=re.I):
        return "Выхожу из программы, хорошего дня!"
    elif finally_word not in ["1", "2"]:
        return "Ваше значение является не допустимым!"
    else:

        print("""Можете оставить поле пустым если хотите просмотреть содержимое файла по умолчанию,
или передать путь к своему файлу""")
    file_input = input()

    true_path = file_input if file_input != "" else PATH_TO_JSON

    try:

        if re.fullmatch("1", finally_word):
            print("Загружаю вакансии...\n")
            vacancies_list = load_vacancies(JsonSaver().json_file_reader(true_path))
            if not vacancies_list:
                print("Файл пуст!")
                return []
            else:
                return vacancies_list
        elif re.fullmatch("exit", finally_word, flags=re.I):
            return "Завершение работы..."
        else:
            return "Введите 1 или exit!"

    except (FileNotFoundError, JSONDecodeError):
        return "Ошибка чтения файла, Убедитесь в существовании файла, или в том что вы передаете правильный путь!"


def main() -> str:
    """
    User function
    """
    print(
        f"""{greeting_function()} Вы в поиске работы и рассматриваете вакансии?
Эта программа вам поможет!!
Eсли вы готовы приступить к подбору вакансий введите "Да" или "Нет" если подбор вакансий не актуален для вас"""
    )

    user_input = input()
    if re.fullmatch("Нет", user_input, flags=re.I):
        return "Возвращайтесь когда вам понадобится моя помощь, хорошего дня!"
    elif re.fullmatch("Да", user_input, flags=re.I):
        print("Идем дальше! Хотите рассматривать вакансии или ищете что то конкретное? Введите 1 или 2:")
    else:
        return "Не понимаю вас, введите Да или Нет и попробуйте снова!"

    status_input = input()
    if re.fullmatch("1", status_input):
        print(
            "Вы запустили программу, передавайте номера страниц для просмотра вакансий или введите 'exit' для выхода"
        )
        status = True
    elif re.fullmatch("2", status_input):
        print("Загружаю данные...")
        status = False
    else:
        return "Не понимаю вас, введите 1 или 2 и попробуйте снова!"
    if status:
        while True:
            print("Какая страница вас интересует?")
            str_input = input()
            if re.fullmatch("exit", str_input, flags=re.I):
                print("Выхожу из программы...")
                time.sleep(3)
                return "Надеюсь вы нашли что нибудь для себя, хорошего дня!"
            else:
                print(watch(str_input))
    elif not status:
        print("""Хотите использовать ключевые слова при поиске? Например название вакансии или требования к сотрудникам
Введите Да или Нет:""")
        keyword_input = input()
        keyword_list = key_vacancies(keyword_input)
        if not keyword_list:
            return "Ничего не нашлось под ваши критерии, пожалуйста попробуйте снова!"
        else:
            if re.fullmatch("Да", keyword_input, flags=re.I):
                print("Хотите посмотреть топ N вакансий по зарплате? Для просмотра введите N, для выхода exit")
                while True:
                    top_input = input()
                    if re.fullmatch("exit", top_input, flags=re.I):
                        print("Идем дальше...")
                        break
                    elif re.fullmatch(r"\d+", top_input) and int(top_input) < len(keyword_list):
                        print(load_vacancies(vacancies(sorted_vacancy(keyword_list)[:int(top_input)])))
                        return "До новых встреч!"
                    else:
                        print(
                            f"Введите другой N, например {random.randint(1, len(keyword_list))}"
                        )
            elif re.fullmatch("Нет", keyword_input, flags=re.I):
                print("Идем дальше...")
            else:
                return "Критическая ошибка! Попробуйте снова!"

        print("Хотите отсортировать вакансии по зарплате? Введите Да или Нет:")

        filter_input = input()
        filtered_vacancies_list = filter_vacancies(filter_input, keyword_list)
        if not filtered_vacancies_list:
            return "Ничего не нашлось под ваши критерии, пожалуйста попробуйте снова!"
        else:
            print("Хотите отсортировать вакансии по зарплате? Введите Да или Нет:")

        sorted_input = input()
        sorted_vacancies_list = sorted_vacancies(sorted_input, filtered_vacancies_list)
        if not sorted_vacancies_list:
            return "Ничего не нашлось под ваши критерии, пожалуйста попробуйте снова!"
        else:
            print("""Отобрал для вас подходящие вакансии,
если хотите сохранить их в файл введите 1,
если хотите посмотреть или удалить вакансии введите 2,
если хотите завершить работу программы введите exit:
(При сохранении в файл пожалуйста убедитесь что вы его создали и передаете полный путь к нему!!""")
        file_input = input()
        file_list = file_worker(file_input, sorted_vacancies_list)
        if re.fullmatch("exit", file_input, flags=re.I):
            return "Завершение работы... \nХорошего дня!"
        elif not file_list:
            return "Ошибка чтения файла, попробуйте запустить программу снова!"
        else:
            print("Введите 1 если хотите посмотреть все вакансии из файла, или exit для выхода из программы")

        finally_input = input()
        finally_list = finally_user_function(finally_input)
        if not finally_list:
            return "Список вакансий пуст, пожалуйста попробуйте снова!"
        else:
            print(finally_list)
            return "До новых встреч!"
    else:
        return "Принудительное завершение работы, пожалуйста перезапустите программу!"


if __name__ == "__main__":
    print(main())

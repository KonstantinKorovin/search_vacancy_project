class NameException(Exception):
    """
    Вызов исключения при отсутствии нейминга вакансии
    """

    def __init__(self, *args):
        self.__message = args if args else "Название вакансии не может быть пустым!"

    def __str__(self):
        return self.__message


class AreaException(Exception):
    """
    Вызов исключения при отсутствии нейминга города
    """

    def __init__(self, *args):
        self.__message = args if args else "Название города не может быть пустым!"

    def __str__(self):
        return self.__message


class SalaryZeroException(Exception):
    """
    Вызов исключения при указании не валидной зарплаты
    """

    def __init__(self, *args):
        self.__message = args if args else "Зарплата не может быть меньше нуля!"

    def __str__(self):
        return self.__message

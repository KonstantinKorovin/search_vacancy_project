from unittest.mock import patch

from src.hh import HH


def test_error_hh():
    """
    Тестовый запрос к API
    """
    with patch("src.hh.HH.get_vacancies") as mock_get:
        mock_get.return_value = "Ошибка 404!"
        assert HH().get_vacancies() == "Ошибка 404!"
        mock_get.assert_called_once()


def test_get_vacancies():
    """
    Проверка работоспособности класса HH
    """
    assert HH(page=100000).get_vacancies() == "Ошибка 400!"

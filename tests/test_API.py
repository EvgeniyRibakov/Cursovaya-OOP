import unittest
from unittest.mock import patch, MagicMock
from src.API import HeadHunterAPI


class TestHeadHunterAPI(unittest.TestCase):

    @patch('requests.get')
    def test_connect_success(self, mock_get):
        # Настройка mock объекта
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        api = HeadHunterAPI()
        response = api.connect()

        # Проверяем, что запрос был отправлен с нужным URL и заголовками
        mock_get.assert_called_once_with("https://api.hh.ru/vacancies", headers={"User-Agent": "api-test-agent"})
        self.assertEqual(response.status_code, 200)

    @patch('requests.get')
    def test_connect_failure(self, mock_get):
        # Настройка mock объекта для имитации ошибки
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        api = HeadHunterAPI()
        with self.assertRaises(Exception) as context:
            api.connect()

        self.assertTrue('Ошибка подключения к API' in str(context.exception))

    @patch('requests.get')
    def test_get_vacancies(self, mock_get):
        # Настройка mock объекта для успешного ответа
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'items': [
            {'name': 'Test Vacancy', 'snippet': {'responsibility': 'Test Description'},
             'alternate_url': 'http://test.url'}]}
        mock_get.return_value = mock_response

        api = HeadHunterAPI()
        vacancies = api.get_vacancies("Test")

        self.assertEqual(len(vacancies), 1)
        self.assertEqual(vacancies[0]['name'], 'Test Vacancy')
        self.assertEqual(vacancies[0]['snippet']['responsibility'], 'Test Description')
        self.assertEqual(vacancies[0]['alternate_url'], 'http://test.url')


if __name__ == '__main__':
    unittest.main()

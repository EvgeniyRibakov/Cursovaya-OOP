import unittest
import os
import json
from src.save_files import JSONSaver
from unittest.mock import MagicMock


class TestJSONSaver(unittest.TestCase):

    def setUp(self):
        self.filename = "test_vacancies.json"
        self.saver = JSONSaver(filename=self.filename)
        # Убедимся, что файл не существует перед тестами
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def tearDown(self):
        # Удаляем файл после тестов
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_read_no_file(self):
        # Проверяем, что чтение несуществующего файла возвращает пустой список
        result = self.saver.read()
        self.assertEqual(result, [])

    def test_read_existing_file(self):
        # Создаем файл с тестовыми данными
        test_data = [
            {"title": "Test Vacancy", "salary": 100000, "description": "Test Description", "url": "http://test.url"}]
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(test_data, file)

        # Проверяем, что данные читаются корректно
        result = self.saver.read()
        self.assertEqual(result, test_data)

    def test_add_vacancy(self):
        # Мок объект вакансии
        vacancy = MagicMock()
        vacancy.to_dict.return_value = {"title": "Test Vacancy", "salary": 100000, "description": "Test Description",
                                        "url": "http://test.url"}

        # Добавляем вакансию и проверяем, что она добавлена
        self.saver.add_vacancy(vacancy)
        result = self.saver.read()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["title"], "Test Vacancy")
        self.assertEqual(result[0]["salary"], 100000)

    def test_delete_vacancy(self):
        # Мок объект вакансии
        vacancy = MagicMock()
        vacancy.to_dict.return_value = {"title": "Test Vacancy", "salary": 100000, "description": "Test Description",
                                        "url": "http://test.url"}
        vacancy.url = "http://test.url"

        # Добавляем вакансию, затем удаляем ее
        self.saver.add_vacancy(vacancy)
        self.saver.delete_vacancy(vacancy)
        result = self.saver.read()
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()

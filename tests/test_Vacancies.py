import unittest
from src.Vacancies import Vacancy

class TestVacancy(unittest.TestCase):
    def test_vacancy_initialization(self):
        vacancy = Vacancy("Test Title", 100000, "Test Description", "http://test.url")
        self.assertEqual(vacancy.title, "Test Title")
        self.assertEqual(vacancy.salary, 100000)
        self.assertEqual(vacancy.description, "Test Description")
        self.assertEqual(vacancy.url, "http://test.url")

    def test_validate_str(self):
        with self.assertRaises(ValueError):
            Vacancy("Test Title", 100000, 123, "http://test.url")  # description не строка

    def test_validate_int(self):
        with self.assertRaises(ValueError):
            Vacancy("Test Title", "NotAnInt", "Test Description", "http://test.url")  # salary не целое число

    def test_comparison_lt(self):
        v1 = Vacancy("Test Title 1", 100000, "Test Description 1", "http://test1.url")
        v2 = Vacancy("Test Title 2", 200000, "Test Description 2", "http://test2.url")
        self.assertTrue(v1 < v2)

    def test_comparison_gt(self):
        v1 = Vacancy("Test Title 1", 300000, "Test Description 1", "http://test1.url")
        v2 = Vacancy("Test Title 2", 200000, "Test Description 2", "http://test2.url")
        self.assertTrue(v1 > v2)

    def test_cast_to_object_list(self):
        vacancies_data = [
            {
                'name': 'Test Title 1',
                'salary': {'from': 100000},
                'snippet': {'responsibility': 'Test Description 1'},
                'alternate_url': 'http://test1.url'
            },
            {
                'name': 'Test Title 2',
                'salary': {'from': 200000},
                'snippet': {'responsibility': 'Test Description 2'},
                'alternate_url': 'http://test2.url'
            }
        ]
        vacancies = Vacancy.cast_to_object_list(vacancies_data)
        self.assertEqual(len(vacancies), 2)
        self.assertEqual(vacancies[0].title, 'Test Title 1')
        self.assertEqual(vacancies[1].title, 'Test Title 2')

    def test_to_dict(self):
        vacancy = Vacancy("Test Title", 100000, "Test Description", "http://test.url")
        expected_dict = {
            'title': "Test Title",
            'salary': 100000,
            'description': "Test Description",
            'url': "http://test.url"
        }
        self.assertEqual(vacancy.to_dict(), expected_dict)

if __name__ == '__main__':
    unittest.main()

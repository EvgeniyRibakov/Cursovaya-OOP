import re
from src.API import HeadHunterAPI
from src.Vacancies import Vacancy
from src.save_files import JSONSaver


def clean_html(raw_html):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', raw_html)


def filter_vacancies(vacancies, keywords):
    filtered = []
    for vacancy in vacancies:
        description = clean_html(vacancy.description.lower()) if vacancy.description else ""
        if all(keyword.lower() in description for keyword in keywords):
            filtered.append(vacancy)
    return filtered


def get_vacancies_by_salary(vacancies, salary_range):
    min_salary, max_salary = map(int, salary_range.replace(' ', '').split('-'))
    return [vacancy for vacancy in vacancies if min_salary <= vacancy.salary <= max_salary]


def sort_vacancies(vacancies):
    return sorted(vacancies, key=lambda x: x.salary, reverse=True)


def get_top_vacancies(vacancies, top_n):
    return vacancies[:top_n]


def print_vacancies(vacancies):
    for vacancy in vacancies:
        print(f"Title: {vacancy.title}, Salary: {vacancy.salary}, URL: {vacancy.url}")


def user_interaction():
    hh_api = HeadHunterAPI()
    search_query = input("Введите поисковый запрос: ")
    hh_vacancies = hh_api.get_vacancies(search_query)
    print(f"Получено {len(hh_vacancies)} вакансий с hh.ru")

    vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)
    print(f"Преобразовано {len(vacancies_list)} вакансий в объекты")

    json_saver = JSONSaver()
    for vacancy in vacancies_list:
        json_saver.add_vacancy(vacancy)

    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    print(f"Фильтруем вакансии по ключевым словам: {filter_words}")
    filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
    print(f"Найдено {len(filtered_vacancies)} вакансий после фильтрации по ключевым словам")

    salary_range = input("Введите диапазон зарплат (например, 100000-150000): ")
    print(f"Фильтруем вакансии по диапазону зарплат: {salary_range}")
    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
    print(f"Найдено {len(ranged_vacancies)} вакансий после фильтрации по диапазону зарплат")

    sorted_vacancies = sort_vacancies(ranged_vacancies)
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

    print("Список вакансий:")
    print_vacancies(top_vacancies)


if __name__ == "__main__":
    user_interaction()

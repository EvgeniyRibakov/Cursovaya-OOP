class Vacancy:
    __slots__ = ['title', 'salary', 'description', 'url']

    def __init__(self, title, salary, description, url):
        self.__validate_str(title, 'title')
        self.__validate_int(salary, 'salary')
        self.__validate_str(description, 'description')
        self.__validate_str(url, 'url')
        self.title = title
        self.salary = salary
        self.description = description
        self.url = url

    def __validate_str(self, value, field):
        if not isinstance(value, str):
            raise ValueError(f"{field} должно быть строкой")

    def __validate_int(self, value, field):
        if not isinstance(value, int):
            raise ValueError(f"{field} должно быть целым числом")

    def __lt__(self, other):
        return self.salary < other.salary

    def __gt__(self, other):
        return self.salary > other.salary

    @staticmethod
    def cast_to_object_list(vacancies_data):
        vacancies = []
        for item in vacancies_data:
            title = item['name']
            salary_info = item.get('salary')
            if not salary_info or not item.get('snippet', {}).get('responsibility'):
                continue  # пропускаем вакансии без зарплаты или описания
            salary = salary_info.get('from', 0)
            description = item['snippet']['responsibility']
            url = item['alternate_url']
            vacancies.append(Vacancy(title, salary, description, url))
        return vacancies

    def to_dict(self):
        return {
            'title': self.title,
            'salary': self.salary,
            'description': self.description,
            'url': self.url
        }

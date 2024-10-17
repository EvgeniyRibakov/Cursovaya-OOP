import json
import os


class JSONSaver:
    def __init__(self, filename="../data/vacancies.json"):
        self.__filename = filename

    def read(self):
        if not os.path.exists(self.__filename):
            return []
        with open(self.__filename, 'r', encoding='utf-8') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []

    def add_vacancy(self, vacancy):
        existing_data = self.read()
        existing_data.append(vacancy.to_dict())
        with open(self.__filename, 'w', encoding='utf-8') as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)

    def delete_vacancy(self, vacancy):
        existing_data = self.read()
        existing_data = [v for v in existing_data if v['url'] != vacancy.url]
        with open(self.__filename, 'w', encoding='utf-8') as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)

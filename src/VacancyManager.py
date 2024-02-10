import json
from abc import ABC, abstractmethod
from pathlib import Path
from src.vacancy import Vacancy


class VacancyManager(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancies(self, query):
        pass

    @abstractmethod
    def save_to_file(self):
        pass

    @abstractmethod
    def load_from_file(self):
        pass


class JSONVacancyManager(VacancyManager):
    __filepath = str(Path().resolve()) + "\\json_data\\"

    def __init__(self, filename):
        self.filename = filename
        self.vacancies = []

    def add_vacancy(self, vacancy_list):
        self.vacancies.extend(vacancy_list)

    def get_vacancies(self, query):
        results = []
        for vacancy in self.vacancies:
            if query in vacancy.description.lower():
                results.append(vacancy)
            else:
                results = self.vacancies
        results.sort(reverse=True)
        return results

    def save_to_file(self):
        data = []
        for vacancy in self.vacancies:
            data.append({
                "title": vacancy.title,
                "location": vacancy.location,
                "employer": vacancy.employer,
                "salary": vacancy.get_salary(),
                "description": vacancy.description,
                "experience": vacancy.experience,
                "link": vacancy.link,
                "source": vacancy.source
            })
            json_data = json.dumps(data, ensure_ascii=False, indent=1)
            with open(self.__filepath + self.filename, "w", encoding="utf-8") as file:
                file.write(json_data)

    def load_from_file(self):
        with open(self.__filepath + self.filename, "r", encoding="utf-8") as file:
            json_data = file.read()

        data = json.loads(json_data)
        vacancies_list = [Vacancy(**vacancy) for vacancy in data]
        return vacancies_list

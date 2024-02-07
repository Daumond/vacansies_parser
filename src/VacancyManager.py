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
    def delete_vacancy(self, vacancy):
        pass


class JSONVacancyManager(VacancyManager):
    __filepath = str(Path().resolve()) + "\\json_data\\"

    def __init__(self, filename):
        self.filename = filename
        self.vacancies = []

    def add_vacancy(self, **vacancies_list):
        self.vacancies.extend(vacancies_list)

    def get_vacancies(self, **query):
        results = []
        for vacancy in self.vacancies:
            if query in vacancy.description.lower():
                results.append(vacancy)
            else:
                results = self.vacancies
        results.sort(reverse=True)
        return results

    def delete_vacancy(self, vacancy):
        self.vacancies.remove(vacancy)

    def save_to_file(self, vacancies_list: list):

        with open(self.__filepath + self.filename, "w", encoding="utf-8") as file:
            data = []
            for vacancy in vacancies_list:
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
                json.dump(data, file, ensure_ascii=False, indent=1)
                #file.write(data)

    def load_from_file(self):
        with open(self.__filepath + self.filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            vacancies_list = [Vacancy(**vacancy) for vacancy in data]
            self.vacancies.append(vacancies_list)

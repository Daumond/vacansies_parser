import requests
import os
from dotenv import load_dotenv
from abc import ABC, abstractmethod

load_dotenv()


class AbstractVacancyAPI(ABC):  # Абстрактный класс для наследования
    @abstractmethod
    def get_vacancies(self, request):
        pass


class HHVacancies(AbstractVacancyAPI):  # Класс для запроса вакансий с HH
    def get_vacancies(self, request):
        url = "https://api.hh.ru/vacancies/"
        params = {"text": request}
        response = requests.get(url, params=params)
        data = response.json()
        vacancies = data.get("items")
        return vacancies


class SJVacancies(AbstractVacancyAPI):  # Класс для запроса вакансий с SJ
    SJ_TOKEN = os.getenv("SJ_SECRET_KEY")

    def get_vacancies(self, request):
        url = "https://api.superjob.ru/2.0/vacancies"
        headers = {"X-Api-App-Id": self.SJ_TOKEN}
        params = {"keyword": request}
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        vacancies = data.get("objects")
        return vacancies

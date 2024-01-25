import requests
import os
from dotenv import load_dotenv

load_dotenv()


class AbstractVacancyAPI():  # Абстрактный класс для наследования
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

    def __init__(self, token=SJ_TOKEN):
        self.token = token

    def get_vacancies(self, request):
        url = "https://api.superjob.ru/2.0/vacancies"
        headers = {"X-Api-App-Id": self.token}
        params = {"keyword": request}
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        vacancies = data.get("objects")
        return vacancies

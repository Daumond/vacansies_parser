import requests
import os
from dotenv import load_dotenv
from abc import ABC, abstractmethod
from src.vacancy import Vacancy

load_dotenv()


class AbstractVacancyAPI(ABC):  # Абстрактный класс для наследования
    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def parse_vacancies(self, raw_data):
        pass


class HHVacancies(AbstractVacancyAPI):
    def __init__(self, request):
        self.request = request

    def get_vacancies(self):
        url = "https://api.hh.ru/vacancies/"
        params = {"text": self.request}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            raw_data = data.get("items")
            return raw_data
        elif response.status_code == 400:
            raise ValueError("Неверные параметры запроса")
        elif response.status_code == 404:
            raise ValueError("Нет данных по указанному запросу")
        else:
            raise ValueError(f"Произошла ошибка при обращении к API: {response.status_code}")

    def parse_vacancies(self, raw_data):
        vacancies_list = []
        for item in raw_data:
            parsed_data = {}

            parsed_data['title'] = item.get("name", "...")
            parsed_data['location'] = item["area"].get("name", "...")
            parsed_data['link'] = item.get("alternate_url", "...")
            if not item["salary"] is None:
                parsed_data['salary'] = {'from': item['salary'].get('from', 0), 'to': item['salary'].get('to', 0),
                                         'currency': item['salary'].get('currency', 'RUB').upper()}
            else:
                parsed_data["salary"] = item["salary"]
            parsed_data['employer'] = item['employer'].get('name', '...')
            parsed_data['description'] = item["snippet"].get('responsibility', '...')
            parsed_data['experience'] = item['experience'].get('name', '...')
            parsed_data['source'] = "hh.ru"

            vacancy = Vacancy(**parsed_data)
            vacancy.validate()
            vacancies_list.append(vacancy)
        return vacancies_list


class SJVacancies(AbstractVacancyAPI):
    SJ_TOKEN = os.getenv("SJ_SECRET_KEY")

    def __init__(self, request):
        self.request = request

    def get_vacancies(self):
        url = "https://api.superjob.ru/2.0/vacancies"
        headers = {"X-Api-App-Id": self.SJ_TOKEN}
        params = {"keyword": self.request}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            vacancies = data.get("objects")
            return vacancies
        elif response.status_code == 400:
            raise ValueError("Неверные параметры запроса")
        elif response.status_code == 404:
            raise ValueError("Нет данных по указанному запросу")
        else:
            raise ValueError(f"Произошла ошибка при обращении к API: {response.status_code}")

    def parse_vacancies(self, raw_data):
        vacancies_list = []
        for item in raw_data:
            parsed_data = {
                'title': item.get('profession', '...'),
                'location': item['town'].get('title', '...'),
                'link': item.get('link', '...'),
                'employer': item.get('firm_name', '...'),
                'salary': {'from': item.get('payment_from', 0), 'to': item.get('payment_to', 0),
                           'currency': item.get('currency', 'RUB').upper()},
                'description': item.get('candidat', '...'),
                'experience': item['experience'].get('title', '...'),
                'source': 'superjob.ru'
            }
            vacancy = Vacancy(**parsed_data)
            vacancy.validate()
            vacancies_list.append(vacancy)
        return vacancies_list

from src.VacansiesFromAPI import HHVacancies, SJVacancies
from src.VacancyManager import JSONVacancyManager


def greetings():
    print("Привет, это программа для поиска и анализа вакансий с разных платформ.\n")
    print("Вы можете выбрать одну или несколько платформ для получения вакансий: hh.ru или superjob.ru.\n")


def get_platforms():
    platforms = input("Выберите платформу для поиска:\n"
                      "1. hh.ru\n"
                      "2. superjob.ru\n"
                      "3. Выбрать обе платформы\n")
    return int(platforms)


def get_vacancies(platform: int, request: str) -> list:
    parsers = []
    if platform == 1:
        parser = HHVacancies(request)
        parsers.append(parser)
    elif platform == 2:
        parser = SJVacancies(request)
        parsers.append(parser)
    elif platform == 3:
        parsers.append(HHVacancies(request))
        parsers.append(SJVacancies(request))
    else:
        print(f"Неверная платформа: {platform}.\n")
        raise ValueError

    vacancies = []

    for parser in parsers:
        data = parser.get_vacancies()
        vacancies.extend(parser.parse_vacancies(data))

    return vacancies


def save_vacancies(vacancies):
    handler = JSONVacancyManager("data.json")
    handler.save_to_file(vacancies)
    print(f"Сохранено {len(vacancies)} вакансий в файл")


greetings()
platforms = get_platforms()
query = input("Введите поисковый запрос: ")
try:
    vacancies = get_vacancies(platforms, query)
    save_vacancies(vacancies)

except ValueError:
    print('Ошибка при обработке запроса. Попробуйте еще раз.\n')

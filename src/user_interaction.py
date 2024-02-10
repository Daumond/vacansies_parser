from src.VacansiesFromAPI import HHVacancies, SJVacancies
from src.VacancyManager import JSONVacancyManager


def get_top_n_vacancies_by_salary(manager):
    try:
        n = int(input("Введите количество вакансий для вывода: "))
        if n <= 0:
            print("Число должно быть положительным.")
            return
    except ValueError:
        print("Введите целое положительное число.")
        return

    sorted_vacancies = sorted(manager.vacancies, key=lambda vacancy: vacancy.salary_from, reverse=True)
    top_n_vacancies = sorted_vacancies[:n]

    print(f"\nТоп-{n} вакансий по зарплате:")
    for i, vacancy in enumerate(top_n_vacancies, start=1):
        print(f"{i}. {vacancy.title} - {vacancy.get_salary()}")


def main():
    print("Добро пожаловать в программу для поиска вакансий!")

    while True:
        print("\nВыберите действие:")
        print("1. Поиск вакансий")
        print("2. Вывод списка вакансий")
        print("3. Выход")

        choice = input("Введите номер действия: ")

        if choice == "1":
            platform = input("Выберите платформу (hh/sj): ")
            query = input("Введите поисковый запрос: ")
            if platform.lower() == "hh":
                api = HHVacancies(query)
            elif platform.lower() == "sj":
                api = SJVacancies(query)
            else:
                print("Неправильно выбрана платформа")
                continue

            vacancies = api.parse_vacancies(api.get_vacancies())
            filename = input("Введите имя файла для сохранения результатов: ")
            manager = JSONVacancyManager(filename)
            manager.add_vacancy(vacancies)
            manager.save_to_file()
            print(f"Сохранено {len(vacancies)} вакансий в файл {filename}")

        elif choice == "2":
            filename = input("Введите имя файла с сохраненными вакансиями: ")
            manager = JSONVacancyManager(filename)
            try:
                loaded_vacancies = manager.load_from_file()
                print("Данные из файла успешно загружены\n")
            except FileNotFoundError:
                print("Ошибка: Не найден такой файл\n")
                continue

            print("Выберите действие:")
            print("1. Вывести все вакансии")
            print("2. Фильтровать вакансии по ключевому слову в описании")
            print("3. Получить топ N вакансий по зарплате")
            print("4. Вернуться в главное меню")

            action = input("Введите номер действия: ")

            if action == "1":
                for vacancy in loaded_vacancies:
                    print(vacancy)
            elif action == "2":
                keyword = input("Введите ключевое слово для фильтрации: ")
                print("Ожидайте, процесс займет какое то время\n")
                filtered_vacancies = manager.get_vacancies(keyword)
                if filtered_vacancies:
                    for vacancy in filtered_vacancies:
                        print(vacancy)
                else:
                    print("Нет вакансий с указанным ключевым словом")
            elif action == "3":
                get_top_n_vacancies_by_salary(manager)
            elif action == "4":
                continue
            else:
                print("Неверный номер действия")

        elif choice == "3":
            print("До свидания!")
            break

        else:
            print("Неверный номер действия")


main()

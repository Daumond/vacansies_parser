class Vacancy:

    def __init__(self, **kwargs):
        self.__title: str = kwargs['title']
        self.__location: str = kwargs['location']
        self.__link: str = kwargs['link']
        self.__employer: str = kwargs['employer']
        self.__salary: dict | str = kwargs['salary']
        self.__description: str = kwargs['description']
        self.__experience: str = kwargs['experience']
        self.__source: str = kwargs['source']

    def __str__(self):
        description = self.__description.replace("\n", " ")

        if len(description) > 150:
            description = description[:147] + "..."

        result = (f"Вакансия: {self.__title}\n"
                  f"Город: {self.__location}\n"
                  f"Работодатель: {self.__employer}\n"
                  f"Зарплата: {self.get_salary()} {self.__salary['currency']}\n"
                  f"Описание: {description}\n"
                  f"Опыт работы: {self.__experience}\n"
                  f"Ссылка на вакансию: {self.__link}\n"
                  f"Источник: {self.__source}")

        return result

    @property
    def title(self):
        return self.__title

    @property
    def location(self):
        return self.__location

    @property
    def employer(self):
        return self.__employer

    @property
    def description(self):
        return self.__description

    @property
    def experience(self):
        return self.__experience

    @property
    def link(self):
        return self.__link

    @property
    def source(self):
        return self.__source

    @property
    def salary_from(self) -> int:
        if isinstance(self.__salary, dict):
            return self.__salary['from']
        else:
            salary_parts = self.__salary.split(' -> ')
            return int(float(salary_parts[0]))

    @property
    def salary_to(self) -> int:
        if isinstance(self.__salary, dict):
            return self.__salary['to']
        else:
            salary_parts = self.__salary.split(' -> ')
            return int(float(salary_parts[1]))

    def get_salary(self) -> str:
        if self.__salary is None:
            self.__salary = {'from': 0, 'to': 0, 'currency': 'RUB'}
        elif self.__salary['from'] is None:
            self.__salary['from'] = 0
        elif self.__salary['to'] is None:
            self.__salary['to'] = 0

        if isinstance(self.__salary, str):
            return self.__salary
        else:
            if self.__salary['from'] and self.__salary['to']:
                salary_total = f'{self.__salary["from"]} -> {self.__salary["to"]}'
                return salary_total

            elif self.__salary['to']:
                salary_total = f'0 -> {self.__salary["to"]}'
                return salary_total

            elif self.__salary['from']:
                salary_total = f'{self.__salary["from"]} -> 0'
                return salary_total

            else:
                salary_total = '0 -> 0'
                return salary_total

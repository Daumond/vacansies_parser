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
                  f"Зарплата: {self.get_salary()}\n"
                  f"Описание: {description}\n"
                  f"Опыт работы: {self.__experience}\n"
                  f"Ссылка на вакансию: {self.__link}\n"
                  f"Источник: {self.__source}\n")

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

    def __eq__(self, other):

        if isinstance(other, Vacancy):
            return (self.salary_from == other.salary_from
                    and self.salary_to == other.salary_to)
        else:
            raise TypeError('Неподдерживаемый тип операнда. Можно сравнить только объекты класса Vacancy.')

    def __lt__(self, other):

        if isinstance(other, Vacancy):
            return (self.salary_from < other.salary_from
                    and self.salary_to < other.salary_to)
        else:
            raise TypeError('Неподдерживаемый тип операнда. Можно сравнить только объекты класса Vacancy.')

    def get_salary(self) -> str:
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

    def validate(self):

        if self.__salary is None:
            self.__salary = {'from': 0, 'to': 0, 'currency': 'RUB'}
        elif self.__salary['from'] is None:
            self.__salary['from'] = 0
        elif self.__salary['to'] is None:
            self.__salary['to'] = 0

        if self.__title is None or not isinstance(self.__title, str):
            self.__title = 'empty...'

        if self.__link is None or not isinstance(self.__link, str):
            self.__link = 'empty...'

        if self.__location is None or not isinstance(self.__location, str):
            self.__location = 'empty...'

        if self.__employer is None or not isinstance(self.__employer, str):
            self.__employer = 'empty...'

        if self.__description is None or not isinstance(self.__description, str):
            self.__description = 'empty...'

        if self.__experience is None or not isinstance(self.__experience, str):
            self.__experience = 'empty...'

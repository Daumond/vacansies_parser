from src import VacansiesFromAPI


hh_vacancies = VacansiesFromAPI.HHVacancies()
print(hh_vacancies.get_vacancies("Python"))
sj_vacancies = VacansiesFromAPI.SJVacancies()
print(sj_vacancies.get_vacancies("Python"))

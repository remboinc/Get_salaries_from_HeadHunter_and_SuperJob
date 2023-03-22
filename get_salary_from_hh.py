from itertools import count
import requests
import global_variables
from get_predict_salary import predict_salary


def get_all_vacancies_hh(language):
    all_vacancies_from_hh = []
    hh_api_url = 'https://api.hh.ru/vacancies/'
    moscow = 1
    month = 30
    params = {
        'specializations': 'программист',
        'text': language,
        'area': moscow,
        'period': month,
        'per_page': 100,
    }
    for page in count(0):
        params["page"] = page
        response = requests.get(hh_api_url, params=params)
        response.raise_for_status()
        vacancies = response.json()
        if page == vacancies['pages'] - 1:
            break
        all_vacancies_from_hh.append(vacancies)
    return all_vacancies_from_hh


def get_salaries(all_vacancies_from_hh):
    all_salaries = []
    for vacancies in all_vacancies_from_hh:
        vacancies_found = vacancies['found']
        vacancies = vacancies['items']
        for vacancy in vacancies:
            if vacancy['salary']:
                salary = vacancy['salary']
                all_salaries.append(salary)
    return all_salaries, vacancies_found


def get_avg_salary(all_salaries):
    average_salary = []
    for salary in all_salaries:
        if salary['currency'] == 'RUR':
            average_salary.append(predict_salary(salary['from'], salary['to']))
    avg_for_lang = int(sum(average_salary) / len(average_salary))
    return avg_for_lang


def get_salary_from_hh():
    all_salaries_hh = {}
    for language in global_variables.PROGRAMMING_LANGUAGES:
        all_vacancies_from_hh = get_all_vacancies_hh(language)
        all_salaries, vacancies_found = get_salaries(all_vacancies_from_hh)
        avg_for_lang = get_avg_salary(all_salaries)
        vacancies_processed = len(all_salaries)
        all_salaries_hh.update(
            {
                language:
                    {'vacancies_found': vacancies_found,
                     'vacancies_processed': vacancies_processed,
                     'average_salary': avg_for_lang},
            }
        )
    return all_salaries_hh

from itertools import count
import requests
import global_variables
from get_predict_salary import predict_salary, get_avg_for_lang


def get_all_vacancies_hh(language):
    all_vacancies_from_hh = {}
    hh_api_url = 'https://api.hh.ru/vacancies/'
    page_with_salary = []
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
        page_with_salary.append(vacancies)
        all_vacancies_from_hh[language] = page_with_salary
    return all_vacancies_from_hh


def get_salaries(all_vacancies_from_hh, language):
    all_salaries = {}
    vacancies_found = {}
    salaries = []
    for vacancies in all_vacancies_from_hh[language]:
        how_much = vacancies['found']
        vacancies_found[language] = how_much
        vacancies = vacancies['items']
        for salary in vacancies:
            if salary['salary']:
                salary = salary['salary']
                salaries.append(salary)
                all_salaries[language] = salaries
    return all_salaries, vacancies_found


def get_avg_salary(all_salaries, language):
    avg_for_lang = {}
    average_salaries = []
    for salary in all_salaries[language]:
        if salary['currency'] == 'RUR':
            average_salaries.extend(predict_salary(salary['from'], salary['to']))
            avg_for_lang.update(get_avg_for_lang(average_salaries, language))
    return avg_for_lang


def get_salary_from_hh():
    all_salaries_hh = {}
    for language in global_variables.PROGRAMMING_LANGUAGES:
        all_vacancies_from_hh = get_all_vacancies_hh(language)
        all_salaries, vacancies_found = get_salaries(all_vacancies_from_hh, language)
        avg_for_lang = get_avg_salary(all_salaries, language)
        average_salary = {}
        vacancies_processed = {}
        average_salary.update(avg_for_lang)
        value_of_vacancy = len(all_salaries[language])
        vacancies_processed[language] = value_of_vacancy
        all_salaries_hh.update(
            {
                language:
                    {'vacancies_found': vacancies_found[language],
                     'vacancies_processed': vacancies_processed[language],
                     'average_salary': average_salary[language]},
            }
        )
    return all_salaries_hh

from itertools import count

import requests
import global_variables


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
        params.update({"page": page})
        response = requests.get(hh_api_url, params=params)
        response.raise_for_status()
        vacancies = response.json()
        if page == vacancies['pages'] - 1:
            break
        page_with_salary.append(vacancies)
        all_vacancies_from_hh.update({language: page_with_salary})
    return all_vacancies_from_hh


def how_much_vacancies(all_vacancies_from_hh, language):
    vacancies_found = {}
    for vaсancies in all_vacancies_from_hh[language]:
        how_much = vaсancies['found']
        vacancies_found.update({language: how_much})
    return vacancies_found


def get_salaries(all_vacancies_from_hh, language):
    all_salaries = {}
    salaries = []
    for items in all_vacancies_from_hh[language]:
        items = items['items']
        for salary in items:
            if salary['salary'] is not None:
                salary = salary['salary']
                salaries.append(salary)
                all_salaries.update({language: salaries})
    return all_salaries


def get_avg_salary(all_salaries, language):
    avarage_for_lang = {}
    average_salaries = []
    for el in all_salaries[language]:
        if el['currency'] == 'RUR' and el['from'] and el['to']:
            avg_salary = (el['from'] + el['to']) / 2
            average_salaries.append(avg_salary)
        elif el['from']:
            avg_salary = el['from'] * 1.2
            average_salaries.append(avg_salary)
        elif el['to']:
            avg_salary = el['to'] * 0.8
            average_salaries.append(avg_salary)
    average_calculation = int(sum(average_salaries) / len(average_salaries))
    avarage_for_lang.update({language: average_calculation})
    return avarage_for_lang


def predict_rub_salary(avarage_for_lang, all_salaries, vacancies_found, language):
    salaries_for_each_language = {}
    average_salary = {}
    vacancies_processed = {}
    average_salary.update(avarage_for_lang)
    value_of_vacancy = len(all_salaries[language])
    vacancies_processed.update({language: value_of_vacancy})
    salaries_for_each_language.update(
        {
            language:
                {'vacancies_found': vacancies_found[language],
                 'vacancies_processed': vacancies_processed[language],
                 'average_salary': average_salary[language]},
        }
    )
    return salaries_for_each_language


def get_salary_from_hh():
    all_salaries_hh = {}
    for language in global_variables.PROGRAMMING_LANGUAGES:
        all_vacancies_from_hh = get_all_vacancies_hh(language)
        vacancies_found = how_much_vacancies(all_vacancies_from_hh, language)
        all_salaries = get_salaries(all_vacancies_from_hh, language)
        avarage_for_lang = get_avg_salary(all_salaries, language)
        all_salaries_hh.update(predict_rub_salary(avarage_for_lang, all_salaries, vacancies_found, language))
    return all_salaries_hh

from itertools import count
import requests

def get_all_content_hh(language):
    all_content = {}
    hh_api_url = 'https://api.hh.ru/vacancies/'
    page_with_salary = []
    params = {
        'specializations': 'программист',
        'text': language,
        'area': '1',
        'period': '30',
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
        all_content.update({language: page_with_salary})
    return all_content


def how_much_vacancies(all_content, language):
    vacancies_found = {}
    for vaсancies in all_content[language]:
        how_much = vaсancies['found']
        vacancies_found.update({language: how_much})
    return vacancies_found


def get_salaries(all_content, language):
    all_salaries = {}
    salaries = []
    for items in all_content[language]:
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


def main():
    PROGRAMMING_LANGUAGES = ('Python', 'JavaScript', 'Java', 'Ruby', 'PHP', 'C++', 'C#')
    all_salaries_hh = {}
    for language in PROGRAMMING_LANGUAGES:
        all_content = get_all_content_hh(language)
        vacancies_found = how_much_vacancies(all_content, language)
        all_salaries = get_salaries(all_content, language)
        avarage_for_lang = get_avg_salary(all_salaries, language)
        all_salaries_hh.update(predict_rub_salary(avarage_for_lang, all_salaries, vacancies_found, language))
    return all_salaries_hh


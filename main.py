from pprint import pprint
from itertools import count
import requests

PROGRAMMING_LANGUAGES = ('Python', 'JavaScript', 'Java', 'Ruby', 'PHP', 'C++', 'C#')


def get_response_json(hh_api_url):
    responses = {}
    for language in PROGRAMMING_LANGUAGES:
        for page in count(0):
            params = {
                'specializations': 'программист',
                'text': language,
                'area': '1',
                'period': '30',
                'page': page,
                'per_page': 100,
            }
            response = requests.get(hh_api_url, params=params)
            response.raise_for_status()
            response_json = response.json()
            if page == response_json['pages'] - 1:
                break
            responses.update({language: response_json})
    return responses


def how_much_vacancies(responses):
    vacancies_found = {}
    for language in PROGRAMMING_LANGUAGES:
        how_much = responses[language]['found']
        vacancies_found.update({language: how_much})
    return vacancies_found


def get_salaries(responses):
    all_salaries = {}
    for language in PROGRAMMING_LANGUAGES:
        salaries = []
        for items in responses[language]['items']:
            if items['salary'] is not None:
                salary = items['salary']
                salaries.append(salary)
                all_salaries.update({language: salaries})
    return all_salaries


def get_avg_salary(all_salaries):
    avg_for_lang = {}
    for language in PROGRAMMING_LANGUAGES:
        average_salaries = []
        for el in all_salaries[language]:
            if el['currency'] == 'RUR':
                if el['from'] and el['to']:
                    avg_salary = (el['from'] + el['to']) / 2
                    average_salaries.append(avg_salary)
                elif el['from']:
                    avg_salary = el['from'] * 1.2
                    average_salaries.append(avg_salary)
                elif el['to']:
                    avg_salary = el['to'] * 0.8
                    average_salaries.append(avg_salary)
        average_calculation = int(sum(average_salaries) / len(average_salaries))
        avg_for_lang.update({language: average_calculation})
    return avg_for_lang


def predict_rub_salary(avg_for_lang, all_salaries, vacancies_found):
    salaries_for_each_language = {}
    average_salary = {}
    vacancies_processed = {}
    for language in PROGRAMMING_LANGUAGES:
        average_salary.update(avg_for_lang)
        value_of_vacancy = len(all_salaries[language])
        vacancies_processed.update({language: value_of_vacancy})
        salaries_for_each_language.update(
            {
                language:
                 {'vacancies_found': vacancies_found[language],
                  'vacancies_processed': vacancies_processed[language],
                  'average_salary': average_salary[language]}
             }
        )
    return salaries_for_each_language


def main():
    hh_api_url = 'https://api.hh.ru/vacancies/'
    responses = get_response_json(hh_api_url)
    vacancies_found = how_much_vacancies(responses)
    all_salaries = get_salaries(responses)
    avg_for_lang = get_avg_salary(all_salaries)
    pprint(predict_rub_salary(avg_for_lang, all_salaries, vacancies_found))


if __name__ == '__main__':
    main()

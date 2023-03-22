import os
from itertools import count
import requests
from dotenv import load_dotenv
import global_variables
from get_predict_salary import predict_salary


def predict_rub_salary_for_superjob(all_vacancies, language):
    average_salaries = {}
    average_salary = []
    for vacancy in all_vacancies[language]:
        for vacancies in vacancy:
            payment_from = vacancies['payment_from']
            payment_to = vacancies['payment_to']
            if vacancies['currency'] == 'rub' and (payment_from or payment_to != 0):
                average_salary.append(predict_salary(payment_from, payment_to))
    average_calculation = int(sum(average_salary) / len(average_salary))
    average_salaries[language] = average_calculation
    return average_salaries


def get_all_vacancies_sj(apikey, language):
    all_vacancies = {}
    search_text_block = 1
    moscow = 4
    industries_dir_sections = 48
    page_with_salary = []
    params = {
        "keyword": f"Программист {language}",
        "srws": search_text_block,
        "town": moscow,
        "catalogues": industries_dir_sections,
        "count": 10,
    }
    headers = {'X-Api-App-Id': apikey}
    sj_api_url = 'https://api.superjob.ru/2.0/vacancies/'
    vacancies_found = {}
    for page in count():
        params['page'] = page
        response = requests.get(sj_api_url, headers=headers, params=params)
        response.raise_for_status()
        vacancies = response.json()
        vacancies_found[language] = vacancies.get('total')
        page_with_salary.append(vacancies.get('objects'))
        all_vacancies[language] = page_with_salary
        if not vacancies['more']:
            break
    return all_vacancies, vacancies_found


def get_salary_from_sj():
    load_dotenv()
    apikey = os.getenv('SJ_SECRET_KEY')

    all_salaries_sj = {}
    for language in global_variables.PROGRAMMING_LANGUAGES:
        all_pages, vacancies_found = get_all_vacancies_sj(apikey, language)
        average_salaries = predict_rub_salary_for_superjob(all_pages, language)
        print(average_salaries)
        vacancies_processed = {}
        response_len = len(all_pages[language])
        vacancies_processed[language] = response_len
        all_salaries_sj.update(
            {
                language:
                    {'vacancies_found': vacancies_found[language],
                     'vacancies_processed': vacancies_processed[language],
                     'average_salary': average_salaries[language]},
            }
        )
    return all_salaries_sj

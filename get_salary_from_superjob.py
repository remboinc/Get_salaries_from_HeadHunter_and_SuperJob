import os
from itertools import count
import requests
from dotenv import load_dotenv
import global_variables


def predict_rub_salary_for_superjob(all_pages, language):
    average_salaries = []
    for vacancy in all_pages[language]:
        for vacancies in vacancy:
            payment_from = vacancies['payment_from']
            payment_to = vacancies['payment_to']
            if vacancies['currency'] == 'rub' and payment_from and payment_to:
                average_salaries.append((payment_from + payment_to) / 2)
            elif payment_from:
                average_salaries.append(payment_from * 1.2)
            elif payment_to:
                average_salaries.append(payment_to * 0.8)
    return average_salaries


def get_avg_for_lang(average_salaries, language):
    avg_for_lang = {}
    average_calculation = int(sum(average_salaries) / len(average_salaries))
    avg_for_lang[language] = average_calculation
    return avg_for_lang


def get_all_pages_sj(apikey, language):
    all_pages = {}
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
        vacancies_found.update({language: vacancies.get('total')})
        page_with_salary.append(vacancies.get('objects'))
        all_pages.update({language: page_with_salary})
        if not vacancies['more']:
            break
    return all_pages, vacancies_found


def collect_all_salaries(all_pages, vacancies_found, language, avg_for_lang):
    salaries_for_each_language = {}
    vacancies_processed = {}
    response_len = len(all_pages[language])
    vacancies_processed.update({language: response_len})
    salaries_for_each_language.update(
        {
            language:
                {'vacancies_found': vacancies_found[language],
                 'vacancies_processed': vacancies_processed[language],
                 'average_salary': avg_for_lang[language]},
        }
    )
    return salaries_for_each_language


def get_salary_from_sj():
    load_dotenv()
    apikey = os.getenv('SJ_SECRET_KEY')

    all_salaries_sj = {}
    for language in global_variables.PROGRAMMING_LANGUAGES:
        all_pages, vacancies_found = get_all_pages_sj(apikey, language)
        average_salaries = predict_rub_salary_for_superjob(all_pages, language)
        avg_for_lang = get_avg_for_lang(average_salaries, language)
        all_salaries_sj.update(collect_all_salaries(all_pages, vacancies_found, language, avg_for_lang))
    return all_salaries_sj

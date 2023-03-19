import os
from itertools import count
import requests
from dotenv import load_dotenv

PROGRAMMING_LANGUAGES = ('Python', 'JavaScript', 'Java', 'Ruby', 'PHP', 'C++', 'C#')


def predict_rub_salary_for_superjob(all_pages):
    avg_for_lang = {}
    for language in PROGRAMMING_LANGUAGES:
        average_salaries = []
        for vac in all_pages[language]:
            for vacancies in vac:
                payment_from = vacancies['payment_from']
                payment_to = vacancies['payment_to']
                if vacancies['currency'] == 'rub':
                    if payment_from and payment_to:
                        average_salaries.append((payment_from + payment_to) / 2)
                    elif payment_from:
                        average_salaries.append(payment_from * 1.2)
                    elif payment_to:
                        average_salaries.append(payment_to * 0.8)
            average_calculation = int(sum(average_salaries) / len(average_salaries))
            avg_for_lang[language] = average_calculation
    return avg_for_lang


def get_salaries_for_each_language_sj(avg_for_lang, all_pages, apikey):
    salaries_for_each_language = {}
    vacancies_found = {}
    vacancies_processed = {}
    for language in PROGRAMMING_LANGUAGES:
        params = {
            "keyword": f"Программист {language}",
            "srws": 1,
            "town": 4,
            "catalogues": 48,
            "count": 10,
        }
        headers = {'X-Api-App-Id': apikey}
        sj_api_url = 'https://api.superjob.ru/2.0/vacancies/'

        response = requests.get(sj_api_url, headers=headers, params=params)
        response.raise_for_status()
        vacancies = response.json()
        response_len = len(all_pages[language])
        vacancies_found.update({language: vacancies['total']})
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


def get_all_pages_sj(apikey):
    all_pages = {}
    search_text_block = 1
    moscow = 4
    list_of_industries_dir_sections = 48
    for language in PROGRAMMING_LANGUAGES:
        page_with_salary = []
        params = {
            "keyword": f"Программист {language}",
            "srws": search_text_block,
            "town": moscow,
            "catalogues": list_of_industries_dir_sections,
            "count": 10,
        }
        headers = {'X-Api-App-Id': apikey}
        sj_api_url = 'https://api.superjob.ru/2.0/vacancies/'

        for page in count():
            params['page'] = page
            response = requests.get(sj_api_url, headers=headers, params=params)
            response.raise_for_status()
            vacancies = response.json()
            page_with_salary.append(vacancies.get('objects'))
            all_pages.update({language: page_with_salary})

            if not vacancies['more']:
                break
    return all_pages


def main():
    load_dotenv()
    apikey = os.getenv('SJ_SECRET_KEY')
    all_pages = get_all_pages_sj(apikey)
    avg_for_lang = predict_rub_salary_for_superjob(all_pages)
    get_salaries_for_each_language_sj(avg_for_lang, all_pages, apikey)


if __name__ == '__main__':
    main()

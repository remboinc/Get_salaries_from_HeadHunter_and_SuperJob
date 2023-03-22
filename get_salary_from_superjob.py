import os
from itertools import count
import requests
import global_variables
from get_predict_salary import predict_salary


def predict_rub_salary_for_superjob(page_with_salary):
    average_salary = []
    for vacancy in page_with_salary:
        for vacancies in vacancy:
            payment_from = vacancies['payment_from']
            payment_to = vacancies['payment_to']
            if vacancies['currency'] == 'rub' and (payment_from or payment_to != 0):
                average_salary.append(predict_salary(payment_from, payment_to))
    average_salaries = int(sum(average_salary) / len(average_salary))
    return average_salaries


def get_all_vacancies_sj(apikey, language):
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

    for page in count():
        params['page'] = page
        response = requests.get(sj_api_url, headers=headers, params=params)
        response.raise_for_status()
        vacancies = response.json()
        vacancies_found = vacancies.get('total')
        page_with_salary.append(vacancies.get('objects'))
        if not vacancies['more']:
            break
    return page_with_salary, vacancies_found


def get_salary_from_sj(apikey):
    all_salaries_sj = {}
    for language in global_variables.PROGRAMMING_LANGUAGES:
        page_with_salary, vacancies_found = get_all_vacancies_sj(apikey, language)
        average_salaries = predict_rub_salary_for_superjob(page_with_salary)
        vacancies_processed = len(page_with_salary)
        all_salaries_sj.update(
            {
                language:
                    {'vacancies_found': vacancies_found,
                     'vacancies_processed': vacancies_processed,
                     'average_salary': average_salaries, }
            }
        )
    return all_salaries_sj


def main():
    apikey = os.getenv('SJ_SECRET_KEY')
    get_salary_from_sj(apikey)


if __name__ == '__main__':
    main()

import requests

PROGRAMMING_LANGUAGES = ('Python', 'JavaScript', 'Java', 'Ruby', 'PHP', 'C++', 'C#', 'C')


def get_salaries(hh_api_url):
    all_salaries = {}

    for language in PROGRAMMING_LANGUAGES:
        params = {
            'specializations': 'программист',
            'text': language,
            'area': '1',
            'period': '30'
        }
        response = requests.get(hh_api_url, params=params)
        response.raise_for_status()
        list_of_vacancies = [response.json()]
        for vacancy in list_of_vacancies:
            salaries = []
            for items in vacancy['items']:
                if items['salary'] is not None:
                    salary = items['salary']
                    salaries.append(salary)
                    all_salaries[language] = salaries
            print(all_salaries)
            return all_salaries


def find_average_salaries(all_salaries):
    print(all_salaries)
    average_salaries = []
    for salary in all_salaries:
        for lang in salary:
            if lang['currency'] == 'RUR':
                if lang['from'] and lang['to']:
                    avg_salary = (int(lang['from']) + int(lang['to'])) / 2
                    average_salaries.append(avg_salary)
                elif lang['from']:
                    avg_salary = int(lang['from']) * 1.2
                    average_salaries.append(avg_salary)
                elif lang['to']:
                    avg_salary = int(lang['to']) * 0.8
                    average_salaries.append(avg_salary)
            else:
                continue
    all_avrg_salaries = int(sum(average_salaries) / len(average_salaries))
    return all_avrg_salaries


def found_vacancies(hh_api_url, all_avrg_salaries, all_salaries):
    vacancies_found = {}
    average_salary = {}
    vacancies_processed = {}
    for language in PROGRAMMING_LANGUAGES:
        params = {
            'specializations': 'программист',
            'text': language,
            'area': '1',
            'period': '30'
        }
        response = requests.get(hh_api_url, params=params)
        response.raise_for_status()
        response_hh = response.json()['found']
        vacancies_found['vacancies_found'] = response_hh
        vacancies_processed['vacancies_processed'] = len(all_salaries)
        average_salary['average_salary'] = all_avrg_salaries
        salaries_for_each_language = {**vacancies_found, **vacancies_processed, **average_salary}
        salaries_for_each_language = {language: salaries_for_each_language}
        print(salaries_for_each_language)


def main():
    hh_api_url = 'https://api.hh.ru/vacancies/'
    all_salaries = get_salaries(hh_api_url)
    all_avrg_salaries = find_average_salaries(all_salaries)
    found_vacancies(hh_api_url, all_avrg_salaries, all_salaries)


if __name__ == '__main__':
    main()
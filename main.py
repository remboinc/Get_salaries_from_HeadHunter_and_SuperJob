import requests

PROGRAMMING_LANGUAGES = ('Python', 'JavaScript', 'Java', 'Ruby', 'PHP', 'C++', 'C#', 'C')


def get_salary(hh_api_url):
    for language in PROGRAMMING_LANGUAGES:
        params = {
            'specializations': 'программист',
            'text': language,
            'area': '1',
            'period': '30'
        }
        response = requests.get(hh_api_url, params=params)
        response.raise_for_status()
        if response is None:
            continue
        elif response is not None:
            salaries = []
            for salary in response.json()['items']:
                if salary is None:
                    continue
                elif salary['salary'] is not None:
                    salaries.append(salary['salary'])
            return salaries


def find_all_salaries(salaries):
    average_salaries = []
    for salary in salaries:
        if salary['currency'] == 'RUR':
            if salary['from'] and salary['to']:
                avg_python_salary = (int(salary['from']) + int(salary['to'])) / 2
                average_salaries.append(avg_python_salary)
            elif salary['from']:
                avg_python_salary = int(salary['from']) * 1.2
                average_salaries.append(avg_python_salary)
            elif salary['to']:
                avg_python_salary = int(salary['to']) * 0.8
                average_salaries.append(avg_python_salary)
        else:
            continue
    all_salaries = int(sum(average_salaries) / len(average_salaries))
    return all_salaries


def found_vacancies(hh_api_url, all_salaries, salaries):
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
        average_salary['average_salary'] = all_salaries
        vacancies_processed['vacancies_processed'] = len(salaries)
        vacancies_found.update(average_salary)
        vacancies_found.update(vacancies_processed)
        d2 = {language: vacancies_found}
        print(d2)


def main():
    hh_api_url = 'https://api.hh.ru/vacancies/'

    salaries = get_salary(hh_api_url)
    all_salaries = find_all_salaries(salaries)
    found_vacancies(hh_api_url, all_salaries, salaries)


if __name__ == '__main__':
    main()

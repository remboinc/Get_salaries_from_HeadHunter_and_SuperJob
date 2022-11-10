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
            return response


def referferf(response):
    avg_salary = []
    for salary in response.json()['items']:
        if salary is None:
            continue
        elif salary['salary'] is not None:
            avg_salary.append(salary['salary'])
    return avg_salary


def get_avrg_salary(avg_salary):
    avg_salaries = []
    for salary in avg_salary:
        print(salary)
        if salary['currency'] == 'RUR':
            if salary['from'] and salary['to']:
                avg_python_salary = (int(salary['from']) + int(salary['to'])) / 2
                avg_salaries.append(avg_python_salary)
            elif salary['from']:
                avg_python_salary = int(salary['from']) * 1.2
                avg_salaries.append(avg_python_salary)
            elif salary['to']:
                avg_python_salary = int(salary['to']) * 0.8
                avg_salaries.append(avg_python_salary)
                fgg = sum(avg_salaries) / len(avg_salaries)
                print(fgg)
        else:
            continue
    return fgg


def found_vacancies(hh_api_url, fgg, avg_salary):
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
        average_salary['average_salary'] = fgg
        vacancies_processed['vacancies_processed'] = len(avg_salary)
        vacancies_found.update(average_salary)
        vacancies_found.update(vacancies_processed)
        d2 = {language: vacancies_found}
        print(d2)


def main():
    hh_api_url = 'https://api.hh.ru/vacancies/'
    response = get_salary(hh_api_url)

    while True:
        avg_salary = get_salary(hh_api_url)
        referferf(response)
        fgg = get_avrg_salary(avg_salary)
        print(found_vacancies(hh_api_url, fgg, avg_salary))


if __name__ == '__main__':
    main()

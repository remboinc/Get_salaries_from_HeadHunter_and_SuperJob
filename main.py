import os
from dotenv import load_dotenv
from terminaltables import AsciiTable
from get_salary_from_hh import get_salary_from_hh
from get_salary_from_superjob import get_salary_from_sj


def get_salary_table(vacancies):
    salary_table = []
    table_headers = [
        'Язык программирования',
        'Вакансий найдено',
        'Вакансий обработано',
        'Средняя зарплата',
    ],
    salary_table.extend(table_headers)
    for lang, statistics in vacancies.items():
        job_table = [[
            lang,
            statistics.get('vacancies_found'),
            statistics.get('vacancies_processed'),
            statistics.get('average_salary'),
        ]]
        salary_table.extend(job_table)
    return salary_table


def main():
    load_dotenv()

    apikey = os.getenv('SJ_SECRET_KEY')
    statistics_sj = get_salary_table(get_salary_from_sj(apikey))
    statistics_hh = get_salary_table(get_salary_from_hh())

    sj_table = AsciiTable(statistics_sj, title='SuperJob Moscow')
    hh_table = AsciiTable(statistics_hh, title='hh.ru Moscow')
    print(sj_table.table)
    print(hh_table.table)


if __name__ == '__main__':
    main()

from terminaltables import AsciiTable
from get_salary_from_superjob import *
from get_salary_from_hh import predict_rub_salary, all_salaries, vacancies_found, avg_for_lang


def print_salary_table(dict):
    salary_table = []
    table_data = [
        'Язык программирования',
        'Вакансий найдено',
        'Вакансий обработано',
        'Средняя зарплата',
    ],
    salary_table.extend(table_data)
    for lang, statistics in dict.items():
        temp_data = [[

            lang,
            statistics.get('vacancies_found'),
            statistics.get('vacancies_processed'),
            statistics.get('average_salary'),
        ]]
        salary_table.extend(temp_data)
    return salary_table


def main():
    statistics_sj = AsciiTable(print_salary_table(get_salaries_for_each_language_sj(avg_for_lang, responses, apikey)), title='SuperJob Moscow')
    statistics_hh = AsciiTable(print_salary_table(predict_rub_salary(avg_for_lang, all_salaries, vacancies_found)), title='hh.ru Moscow')
    print(statistics_sj.table)
    print(statistics_hh.table)


if __name__ == '__main__':
    main()

from terminaltables import AsciiTable
from get_salary_from_superjob import get_salaries_for_each_language_sj, avg_for_lang, responses, apikey
from get_salary_from_hh import predict_rub_salary, avarage_for_lang, all_salaries, vacancies_found


def get_salary_table(dict):
    salary_table = []
    table_headers = [
        'Язык программирования',
        'Вакансий найдено',
        'Вакансий обработано',
        'Средняя зарплата',
    ],
    salary_table.extend(table_headers)
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
    script_for_sj = get_salaries_for_each_language_sj(avg_for_lang, responses, apikey)
    script_for_hh = predict_rub_salary(avarage_for_lang, all_salaries, vacancies_found)
    statistics_sj = get_salary_table(script_for_sj)
    statistics_hh = get_salary_table(script_for_hh)
    sj_table = AsciiTable(statistics_sj, title='SuperJob Moscow')
    hh_table = AsciiTable(statistics_hh, title='hh.ru Moscow')
    print(sj_table.table)
    print(hh_table.table)


if __name__ == '__main__':
    main()

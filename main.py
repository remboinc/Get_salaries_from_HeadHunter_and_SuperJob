from terminaltables import AsciiTable
from Get_salaries_from_HeadHunter_and_SuperJob import get_salary_from_superjob
from get_salary_from_hh import predict_rub_salary, get_avg_salary, how_much_vacancies, get_salaries, get_all_content_hh

PROGRAMMING_LANGUAGES = ('Python', 'JavaScript', 'Java', 'Ruby', 'PHP', 'C++', 'C#')


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
    all_content = get_all_content_hh()
    vacancies_found = how_much_vacancies(all_content)
    all_salaries = get_salaries(all_content)
    avarage_for_lang = get_avg_salary(all_salaries)

    script_for_sj = get_salary_from_superjob.main()
    script_for_hh = predict_rub_salary(avarage_for_lang, all_salaries, vacancies_found)
    statistics_sj = get_salary_table(script_for_sj)
    statistics_hh = get_salary_table(script_for_hh)

    sj_table = AsciiTable(statistics_sj, title='SuperJob Moscow')
    hh_table = AsciiTable(statistics_hh, title='hh.ru Moscow')
    print(sj_table.table)
    print(hh_table.table)


if __name__ == '__main__':
    main()

def predict_salary(salary_from, salary_to):
    average_salaries = []
    if salary_from and salary_to:
        average_salaries.append(int(salary_from + salary_to) / 2)
    elif salary_from:
        average_salaries.append(int(salary_from * 1.2))
    elif salary_to:
        average_salaries.append(int(salary_to * 0.8))
    return average_salaries


def get_avg_for_lang(average_salaries, language):
    avg_for_lang = {}
    if average_salaries:
        average_calculation = int(sum(average_salaries) / len(average_salaries))
        avg_for_lang[language] = average_calculation
    return avg_for_lang

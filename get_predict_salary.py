def predict_salary(salary_from, salary_to):
    if salary_from and salary_to:
        average_salary = int(salary_from + salary_to) / 2
        return average_salary
    elif salary_from:
        average_salary = int(salary_from * 1.2)
        return average_salary
    elif salary_to:
        average_salary = int(salary_to * 0.8)
        return average_salary



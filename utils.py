def sort_salary(vacancy_list):
    return sorted(vacancy_list, key=lambda vacansy: vacansy.salary, reverse=True)

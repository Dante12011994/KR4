def sort_funk(list_):
    return list_['зарплата_от']


def sort_salary(vacancy_list):
    return sorted(vacancy_list, key=sort_funk, reverse=True)

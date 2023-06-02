def sort_funk(list_):
    """
    Функция для выделенеия элементов сортировки
    """
    return list_['зарплата_от']


def sort_salary(vacancy_list):
    """
    Функция для сортировки списка вакансий
    """
    return sorted(vacancy_list, key=sort_funk, reverse=True)

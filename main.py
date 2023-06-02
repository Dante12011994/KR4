from utils import sort_salary
from classes import Get_hh, Get_superjob, Vacancys, Get_servis_api

if __name__ == '__main__':
    key_words = input('Укажите ключевое слово: ')
    quantity_on_platform = int(input('Укажите количество ванасий для платформ: '))
    hh = Get_hh(key_words, quantity_on_platform)
    super_job = Get_superjob(key_words, quantity_on_platform)
    vacancy_list = Get_servis_api.all_vacansis
    Get_servis_api.all_vacansis = []
    for i in vacancy_list:
        Vacancys(i['платформа'],
                 i['должность'],
                 i['зарплата_от'],
                 i['описание'],
                 i['ссылка'])
    Get_servis_api.all_vacansis = sort_salary(Get_servis_api.all_vacansis)
    Vacancys.to_json()
    Vacancys.to_txt()
    Vacancys.to_csv()

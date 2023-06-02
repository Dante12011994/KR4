from utils import sort_salary
from classes import Get_hh, Get_superjob, Vacancys, Get_servis_api

if __name__ == '__main__':
    # Указываем параметры для поска вакансий
    key_words = input('Укажите ключевое слово: ')
    quantity_on_platform = int(input('Укажите количество ванасий для платформ: '))

    # Вызываем API сервис HH
    hh = Get_hh(key_words, quantity_on_platform)

    # Вызываем API сервис SuperJob
    super_job = Get_superjob(key_words, quantity_on_platform)

    # Копируем получившейся список вакансий
    vacancy_list = Get_servis_api.all_vacansis

    # Обнуляем список вакансий в классе Get_servis_api
    Get_servis_api.all_vacansis = []

    # Создаем экземпляры класса Vacancys
    for i in vacancy_list:
        Vacancys(i['платформа'],
                 i['должность'],
                 i['зарплата_от'],
                 i['описание'],
                 i['ссылка'])

    # Сортируем вакансии по уровню зарплаты
    Get_servis_api.all_vacansis = sort_salary(Get_servis_api.all_vacansis)

    # Создаем документы с отсортированными вакансиями в различных форматах
    Vacancys.to_json()
    Vacancys.to_txt()
    Vacancys.to_csv()

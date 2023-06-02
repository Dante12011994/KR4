import json

from classes import Get_hh, Get_superjob, Vacansis

if __name__ == '__main__':
    key_words = input('Укажите ключевое слово: ')
    quantity_on_platform = int(input('Укажите количество ванасий для платформ: '))
    vacansy_list = []
    hh = Get_hh(key_words, quantity_on_platform)
    super_job = Get_superjob(key_words, quantity_on_platform)

    with open('vacansy.json', encoding="utf-8") as file:
        file = json.load(file)
        for i in file:
            vacansy_list.append(Vacansis(i['платформа'],
                                         i['должность'],
                                         i['зарплата_от'],
                                         i['описание'],
                                         i['ссылка']))

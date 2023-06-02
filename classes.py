import csv
import json
import os
from abc import ABC, abstractmethod
import requests


class Get_servis_api(ABC):
    """
    Абстрактный класс для работы с вакансиями
    """
    all_vacansis = []

    @abstractmethod
    def __init__(self):
        """
        Абстрактный метод для инициализации API запросов
        """
        pass

    @classmethod
    def to_json(cls):
        """
        Сохраняет список вакансий в формате JSON
        """
        with open('vacansy.json', 'w', encoding="utf-8") as file:
            json.dump(cls.all_vacansis, file, indent=4)

    @classmethod
    def to_txt(cls):
        """
        Сохраняет список вакансий в формате TXT
        """
        with open('vacansy.txt', 'w', encoding="utf-8") as file:
            for i in cls.all_vacansis:
                file.write(f"{i['платформа']}\n"
                           f"{i['должность']}\n"
                           f"{i['зарплата_от']}\n"
                           f"{i['описание']}\n"
                           f"{i['ссылка']}\n\n")

    @classmethod
    def to_csv(cls):
        """
        Сохраняет список вакансий в формате CSV
        """
        with open('vacansy.scv', 'w', encoding="utf-8") as file:
            names = ['платформа', 'должность', 'зарплата_от', 'описание', 'ссылка']
            file_writer = csv.DictWriter(file, delimiter=",",
                                         lineterminator="\r", fieldnames=names)
            file_writer.writeheader()
            for i in cls.all_vacansis:
                file_writer.writerow(i)


class Get_hh(Get_servis_api):
    """
    Класс для работы с API сервисом НН
    """

    def __init__(self, word, quantity):
        """
        Инициализируем сервис с указанными параметрами
        """
        self.quantity = quantity
        self.word = word

        # Указываем параметры для запроса
        params = {
            'text': 'NAME:' + self.word,
            'area': 1,
            'page': 0,
            'per_page': self.quantity
        }
        req = requests.get('https://api.hh.ru/vacancies', params)
        data = req.content.decode()
        req.close()
        vacancy_list = json.loads(data)

        for i in vacancy_list['items']:
            try:
                salary = i['salary']['from']
            except TypeError:
                salary = 'з/п не указана'
            Get_servis_api.all_vacansis.append({'платформа': 'HeadHunter',
                                                'должность': i['name'],
                                                'зарплата_от': salary,
                                                'описание': f"{i['snippet']['requirement']}\n"
                                                            f"{i['snippet']['responsibility']}",
                                                'ссылка': i['alternate_url']})


class Get_superjob(Get_servis_api):
    """
    Класс для работы с API сервисом SuprJob
    """

    def __init__(self, word, quantity):
        """
        Инициализируем сервис с указанными параметрами
        """
        self.quantity = quantity
        self.word = word

        SUPERJOB_API_KEY = os.environ.get('SUPERJOB_API_KEY')

        headers = {'X-Api-App-Id': SUPERJOB_API_KEY}
        params = {'town': 4, 'count': self.quantity, 'keyword': self.word}
        response = requests.get('https://api.superjob.ru/2.0/vacancies/',
                                params=params,
                                headers=headers)
        vacancys = response.json()
        for i in vacancys['objects']:
            if i['payment_from'] != 0:
                salary = i['payment_from']
            else:
                salary = 'з/п не указана'
            Get_servis_api.all_vacansis.append({'платформа': 'SuperJob',
                                                'должность': i['profession'],
                                                'зарплата_от': salary,
                                                'описание': i['candidat'],
                                                'ссылка': i['link']})


class Vacancys(Get_servis_api):
    """

    """

    def __init__(self, platform, name, salary, description, url):
        self.platform = platform
        self.name = name
        if type(salary) == str or salary is None:
            self.salary = 0
        else:
            self.salary = salary
        self.description = description
        self.url = url
        Get_servis_api.all_vacansis.append({'платформа': self.platform,
                                            'должность': self.name,
                                            'зарплата_от': self.salary,
                                            'описание': self.description,
                                            'ссылка': self.url})

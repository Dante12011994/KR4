import json
import os
from abc import ABC, abstractmethod
import requests


class Get_servis_api(ABC):
    all_vacansis = []

    @abstractmethod
    def __init__(self):
        pass

    @classmethod
    def to_json(cls):
        with open('vacansy.json', 'w', encoding="utf-8") as file:
            json.dump(cls.all_vacansis, file, indent=4)

    @classmethod
    def open_json(cls):
        with open('vacansy.json', encoding="utf-8") as file:
            file = json.load(file)
        return file


class Get_hh(Get_servis_api):

    def __init__(self, word, quantity):
        self.quantity = quantity
        self.word = word

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

    def __init__(self, word, quantity):
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


class Vacancys:
    def __init__(self, platform, name, salary, description, url):
        self.platform = platform
        self.name = name
        if type(salary) == str or salary is None:
            self.salary = 0
        else:
            self.salary = salary
        self.description = description
        self.url = url

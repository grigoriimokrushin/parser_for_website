import json
import os.path


class Vacancy:
    """Класс для работы с вакансиями."""
    all = []

    def __init__(self, name: str, url: str, salary, experience: str):
        """
        Инициализируем экземпляр класса следующими атрибутами: название вакансии (name),
        ccылка на вакансии (url), зарплата (salary) и опыт работы (experience).
        Если работодатель не указал никаких данных по заработной плате, то мы считаем ее за 0
        и автоматически эта вакансия не попадет в наш топ вакансий.
        """
        self.__name = name
        self.__url = url
        self.__experience = experience
        if type(salary) == int:
            self.__salary = salary
        else:
            self.__salary = 0

    def __str__(self):
        """Магический метод для нашего пользователя."""
        return f"{self.__name}"

    def __repr__(self):
        """Магический метод для отладки разработчиком."""
        return f"{self.__class__.__name__}('{self.__name}', '{self.__url}', {self.__salary}, '{self.__experience}')"

    @classmethod
    def instantiate_from_json(cls, file_name='vacancies.json') -> list:
        """Инициализируемся данными из словаря json."""
        try:
            VACANCIES_JSON = os.path.join(file_name)
            with open(VACANCIES_JSON, 'r', encoding="utf-8", errors='ignore') as json_file:
                data = json.load(json_file)
                for vacancy in data['vacancies']:
                    cls.all.append(cls(vacancy['name'], vacancy['url'], vacancy['salary'], vacancy['experience']))
            return cls.all
        except FileNotFoundError:
            raise FileNotFoundError('Отсутствует файл с вакансиями.')

    @classmethod
    def sort_vacancies(cls):
        """Сортировка вакансий по заработной плате."""
        cls.all.sort(key=lambda vacancy: vacancy.__salary, reverse=True)
        return cls.all

    @classmethod
    def get_top_vacancies(cls, top_n: int, vacancies: list) -> list:
        """Получаем топ-N вакансий из нашего списка."""
        return vacancies[:top_n]

    @classmethod
    def print_vacancies(cls, for_print: list):
        """Печатает информацию о вакансиях в консоль."""
        count = 1
        for vacancy in for_print:
            print(f'Вакансия №{count}:\nНазвание:{vacancy.__name}\nЗарплата:{vacancy.__salary} рублей\nОпыт работы: {vacancy.__experience}\n')
            count += 1

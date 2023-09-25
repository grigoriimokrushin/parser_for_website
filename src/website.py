from abc import ABC, abstractmethod
import requests
import os


class Website_API(ABC):
    """Абстрактный класс для работы с API сайтов с вакансиями."""

    @abstractmethod
    def __init__(self):
        """Инициализация экземпляра класса с параметрами для запроса по API."""
        pass

    @abstractmethod
    def get_vacancies(self) -> dict:
        """Получает информацию о вакансиях по API и выдает словарь с информацией."""
        pass

    @abstractmethod
    def format(self, data: dict) -> dict:
        """
        Форматирует полученный словарь в формат для последующего
        сохранения в файл и удобного сравнения вакансий.
        """
        pass


class HeadHunterAPI(Website_API):
    """Класс для работы с HeadHunter через API."""

    def __init__(self, keyword: str):
        """
        Инициализация экземпляра класса с параметрами для запроса по API.
        keyword - наш запрос,
        page = 0 - номер страницы нашего запроса,
        area = 1 - город Москва,
        per_page = 100 - максимальное кол-во запрашиваемых вакансий по API.
        """
        self.__keyword = keyword
        self.__area = 1
        self.__page = 0
        self.__per_page = 100

    def __str__(self):
        """Магический метод для нашего пользователя."""
        return f"Ключевое слово запроса:{self.__keyword}"

    def __repr__(self):
        """Магический метод для отладки разработчиком."""
        return f"{self.__class__.__name__}(keyword:'{self.__keyword}', area: {self.__area}, page: {self.__page}, per_page: {self.__per_page})"

    def get_vacancies(self) -> dict:
        """
        Получает информацию о вакансиях по API и выдает словарь с информацией.
        """
        url_params = {
            'text': f'NAME:{self.__keyword}',
            'area': self.__area,
            'page': self.__page,
            'per_page': self.__per_page}
        responce = requests.get('https://api.hh.ru/vacancies', url_params)
        return responce.json()

    def format(self, data: dict) -> dict:
        """
        Форматирует полученный словарь в формат для последующего
        сохранения в файл и удобного сравнения вакансий.
        """
        vacancies = {'vacancies': []}
        for obj in data['items']:
            if obj['salary'] is None:
                salary = "ЗП не указана"
            elif obj['salary']['from'] is None:
                salary = obj['salary']['to']
            elif obj['salary']['to'] is None:
                salary = obj['salary']['from']
            else:
                salary = int(int(obj['salary']['to']) + int(obj['salary']['from']) / 2)
            new_job = {'name': obj['name'], 'url': obj['apply_alternate_url'], 'salary': salary,
                       'experience': obj['experience']['name']}
            vacancies['vacancies'].append(new_job)
        return vacancies


class SuperJobAPI(Website_API):
    """Класс для работы с SuperJob через API."""

    def __init__(self, keyword: str):
        """
        Инициализация экземпляра класса с параметрами для запроса по API.
        keyword - наш запрос,
        catalogue_id = 48 - id каталога 'Разработка, программирование',
        town_id = 4 - город Москва,
        vacancies_count = 100 - максимальное кол-во запрашиваемых вакансий по API.
        """
        self.__keyword = keyword
        self.__relative_url = 'vacancies/'
        self.__catalogue_id = 48
        self.__town_id = 4
        self.__vacancies_count = 100

    def __str__(self):
        """Магический метод для нашего пользователя."""
        return f"Ключевое слово запроса:{self.__keyword}"

    def __repr__(self):
        """Магический метод для отладки разработчиком."""
        return f"{self.__class__.__name__}(keyword:'{self.__keyword}', catalogue_id: {self.__catalogue_id}, town_id: {self.__town_id}, vacancies_count: {self.__vacancies_count})"

    def get_vacancies(self) -> dict:
        """Получает информацию о вакансиях по API и выдает словарь с информацией."""
        SUPERJOB_API_KEY = os.environ.get('SUPERJOB_API_KEY')
        url_params = {'town': self.__town_id, 'catalogues': self.__catalogue_id, 'count': self.__vacancies_count,
                      'keyword': self.__keyword}
        headers = {
            'X-Api-App-Id': SUPERJOB_API_KEY}
        response = requests.get('https://api.superjob.ru/2.0/%s' % self.__relative_url,
                                params=url_params, headers=headers)
        return response.json()

    def format(self, data: dict) -> dict:
        """
        Форматирует полученный словарь в формат для последующего
        сохранения в файл и удобного сравнения вакансий.
        """
        vacancies = {'vacancies': []}
        for obj in data['objects']:
            if obj['payment_to'] == 0:
                salary = obj['payment_from']
            else:
                salary = obj['payment_to']
            new_job = {'name': obj['profession'], 'url': obj['client']['link'], 'salary': salary, 'experience': obj['experience']['title']}
            vacancies['vacancies'].append(new_job)
        return vacancies





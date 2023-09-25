import json
import os
from abc import ABC, abstractmethod


class Saver(ABC):
    """
    Абстрактный класс, который обязывает реализовать методы для добавления вакансий в файл,
    получения данных из файла по указанным критериям и удаления информации о вакансиях.
    """

    @classmethod
    @abstractmethod
    def add_vacancy(cls, vacancies):
        """Добавляет информацию о вакансиях в файл."""
        pass

    @classmethod
    @abstractmethod
    def get_vacancies(cls) -> dict:
        """Получает информацию о всех вакансиях в файле."""
        pass

    @classmethod
    @abstractmethod
    def delete_file(cls):
        """Удаляет информацию о вакансиях из файла."""
        pass


class JSONSaver(Saver):
    """
    Класс для добавления вакансий в файл,
    получения данных из файла по указанным критериям
    и удаления информации о вакансиях.
    """

    @classmethod
    def add_vacancy(cls, vacancies, file_name='vacancies.json'):
        """Добавляет информацию о вакансиях в файл формата json."""
        with open('vacancies.json', 'a', encoding='utf-8') as json_file:
            json.dump(vacancies, json_file, indent=4, ensure_ascii=False)

    @classmethod
    def get_vacancies(cls, file_name='vacancies.json') -> dict:
        """Получает информацию о всех вакансиях в файле формата json."""
        try:
            VACANCIES_JSON = os.path.join(file_name)
            with open(VACANCIES_JSON, 'r', encoding="utf-8", errors='ignore') as json_file:
                data = json.load(json_file)
                return data
        except FileNotFoundError:
            raise FileNotFoundError('Отсутствует файл с вакансиями.')

    @classmethod
    def delete_file(cls, file_name='vacancies.json'):
        """Удаляет информацию о вакансиях из файла формата json."""
        try:
            VACANCIES_JSON = os.path.join(file_name)
            os.remove(VACANCIES_JSON)
        except FileNotFoundError:
            raise FileNotFoundError('Отсутствует файл с вакансиями.')



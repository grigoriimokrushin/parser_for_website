from src.website import HeadHunterAPI, SuperJobAPI
from src.saver import JSONSaver
from src.vacancies import Vacancy


def user_interaction():
    """
    Функция взаимодействия с пользователем:
    Сначала приветствуем,
    затем предлогаем ввести ключевое слово для поиска,
    происходит подключение по API,
    создается json-фаил,
    инициализируем экземпляры класса Vacancy,
    производим или не производим сортировку по зарплате
    и выдаем запрошенное кол-во вакансий.
    """
    print("Привет!\nЭта программа поможет тебе найти работу в сфере IT в городе Москва.")
    while True:
        Vacancy.all = []
        keyword = input("Введите ключевое слово для поиска:")
        hh = HeadHunterAPI(keyword)
        hh_vacancies = hh.format(hh.get_vacancies())
        sj = SuperJobAPI(keyword)
        sj_vacancies = sj.format((sj.get_vacancies()))
        hh_vacancies['vacancies'].extend(sj_vacancies['vacancies'])
        JSONSaver.add_vacancy(hh_vacancies)
        vacancies = Vacancy.instantiate_from_json()
        numbers_of_vacancies = len(vacancies)
        if numbers_of_vacancies == 0:
            print("Нет вакансий, по вашему запросу.")
            JSONSaver.delete_file()
            continue

        yes_or_no = input(f"Нам удалось найти для вас {numbers_of_vacancies} вакансии.\nХотите отсортируем вакансии по ЗП(+/-)?")
        if yes_or_no in ['-', 'no', 'нет']:
            count = int(input(f"Сколько вакансий из {numbers_of_vacancies} вы хотите посмотреть?"))
            top_vacancies = Vacancy.get_top_vacancies(top_n=count, vacancies=vacancies)
            Vacancy.print_vacancies(top_vacancies)
            JSONSaver.delete_file()
            return

        elif yes_or_no in ['+', 'yes', 'да']:
            count = int(input(f"Топ скольки вакансий из {numbers_of_vacancies} вы хотите посмотреть?"))
            sorted_vacancies = Vacancy.sort_vacancies()
            top_vacancies = Vacancy.get_top_vacancies(top_n=count, vacancies=sorted_vacancies)
            Vacancy.print_vacancies(top_vacancies)
            JSONSaver.delete_file()
            return


if __name__ == "__main__":
    user_interaction()



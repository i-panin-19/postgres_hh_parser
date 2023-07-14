from DBManager import *
from api_hh_func import *


def create_db_tables():
    employers_id = [1225626, 561525, 7788, 9261916, 2335684, 2548771, 3999279, 3693000,
                    973386, 5203927, 240410, 5178096, 640251, 2991458, 5774220, 908642]
    employers_data = []
    vacancies_data = []
    for id in employers_id:
        employers_data.append(getFromIdEmployer(id))
    for id in employers_id:
        vacancies_data = vacancies_data + getVacancies(id)

    data = DBManager(employers_data)
    data.fill_employers_db()
    data = DBManager(vacancies_data)
    data.fill_vacancies_db()


def requests_db():
    input('Нажмите Enter для продолжения..\n')
    # получает список всех компаний и количество вакансий у каждой компании
    #null_data заглушка для класса DBManager
    null_data = []
    data = DBManager(null_data)
    result = data.get_companies_and_vacancies_count()
    print('\nСписок всех компаний и количество вакансий у каждой компании.')
    key_0 = 'Компания'
    key_1 = 'Кол-во вакансий'
    print(f'\n| {key_0 + " " * (50 - len(key_0))} | {key_1 + " " * (15 - len(key_1))} |')
    print(f'|{"_" * 52}|{"_" * 17}|')
    for item in result:
        print(f'| {item[0] + " " * (50 - len(item[0]))} | {str(item[1]) + " " * (15 - len(str(item[1])))} |')
    print(f' {"‾" * 70}')

    # получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
    input('Нажмите Enter для продолжения..\n')
    null_data = []
    data = DBManager(null_data)
    result = data.get_all_vacancies()
    print('\nСписок всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.')
    key_1 = 'Вакансия'
    key_2 = 'Зарплата от'
    key_3 = 'Зарплата до'
    key_4 = 'Валюта'
    key_5 = 'Ссылка вакансии'
    print(f'\n'
          f'| {key_0 + " " * (30 - len(key_0))} | {key_1 + " " * (100 - len(key_1))} | {key_2 + " " * (15 - len(key_2))} '
          f'| {key_3 + " " * (15 - len(key_3))} | {key_4 + " " * (15 - len(key_4))} | {key_5 + " " * (50 - len(key_5))} |')
    print(f'| {"_" * 30} | {"_" * 100} | {"_" * 15} | {"_" * 15} | {"_" * 15} | {"_" * 50} |')
    for item in result:
        print(f'| {item[0] + " " * (30 - len(item[0]))} | {str(item[1]) + " " * (100 - len(str(item[1])))} '
              f'| {str(item[2]) + " " * (15 - len(str(item[2])))} | {str(item[3]) + " " * (15 - len(str(item[3])))} '
              f'| {item[4] + " " * (15 - len(item[4]))} | {str(item[5]) + " " * (50 - len(str(item[5])))} |')
    print(f' {"‾" * 242}')

    # получает среднюю зарплату по вакансиям
    input('Нажмите Enter для продолжения..\n')
    null_data = []
    data = DBManager(null_data)
    result = data.get_avg_salary()
    print(f'\nСредняя зарплата по вакансиям: {round(result[0][0],2)} RUR')

    # получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
    input('\nНажмите Enter для продолжения..\n')
    null_data = []
    data = DBManager(null_data)
    result = data.get_vacancies_with_higher_salary()
    print('\nСписок всех вакансий, у которых зарплата выше средней по всем вакансиям.')
    print(f'| {key_1 + " " * (100 - len(key_1))} |')
    print(f'|{"_" * 102}|')
    for item in result:
        print(f'| {item[0] + " " * (100 - len(item[0]))} |')
    print(f' {"‾" * 102}')

    input('Нажмите Enter для продолжения..\n')
    null_data = []
    key_word = 'разработчик'
    data = DBManager(null_data)
    result = data.get_vacancies_with_keyword(key_word)
    print('\nСписок всех вакансий, в названии которых содержатся переданные в метод слова, например “разработчик”.')
    print(f'| {key_1 + " " * (100 - len(key_1))} |')
    print(f'|{"_" * 102}|')
    for item in result:
        print(f'| {item[0] + " " * (100 - len(item[0]))} |')
    print(f' {"‾" * 102}')


if __name__ == '__main__':
    #create_db_tables()
    requests_db()

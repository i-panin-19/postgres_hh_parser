import psycopg2
import configparser


class DBManager:
    def __init__(self, data):
        self.data = data

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании
        :return:
        """
        config = configparser.ConfigParser()
        config.read("settings.ini")
        conn = psycopg2.connect(host=config['DBConfig']['host'], database=config['DBConfig']['database'],
                                user=config['DBConfig']['username'], password=config['DBConfig']['password'])
        result = []
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        'SELECT employer_name, open_vacancies FROM employers'
                    )
                    data = cur.fetchall()
                    for item in data:
                        result.append([item[0], item[1]])
        finally:
            conn.close()
        return result

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
        :return:
        """
        config = configparser.ConfigParser()
        config.read("settings.ini")
        conn = psycopg2.connect(host=config['DBConfig']['host'], database=config['DBConfig']['database'],
                                user=config['DBConfig']['username'], password=config['DBConfig']['password'])
        result = []
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        'SELECT employer_name, vacancy_name, salary_from, salary_to, salary_currency, vacancy_url '
                        'FROM vacancies INNER JOIN employers USING (employer_id)'
                    )
                    data = cur.fetchall()
                    for item in data:
                        result.append([item[0], item[1], item[2], item[3], item[4], item[5]])
        finally:
            conn.close()
        return result

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям
        :return:
        """
        config = configparser.ConfigParser()
        config.read("settings.ini")
        conn = psycopg2.connect(host=config['DBConfig']['host'], database=config['DBConfig']['database'],
                                user=config['DBConfig']['username'], password=config['DBConfig']['password'])
        result = []
        try:
            with conn:
                with conn.cursor() as cur:

                    #средняя зп подсчитывает только полные данные 'зп от' и 'зп до', что логично
                    cur.execute(
                        "SELECT AVG(salary_from + salary_to) / 2 AS salary_avg FROM vacancies "
                        "WHERE salary_from NOT IN (0) AND salary_to NOT IN (0) AND salary_currency IN ('RUR')"
                    )
                    data = cur.fetchall()
                    for item in data:
                        result.append([item[0]])
        finally:
            conn.close()
        return result

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        :return:
        """
        config = configparser.ConfigParser()
        config.read("settings.ini")
        conn = psycopg2.connect(host=config['DBConfig']['host'], database=config['DBConfig']['database'],
                                user=config['DBConfig']['username'], password=config['DBConfig']['password'])

        # вместо подзапроса запускаю функцию средней зп
        avg_salary = self.get_avg_salary()
        result = []
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        f'SELECT vacancy_name FROM vacancies WHERE salary_from > {avg_salary[0][0]}'
                    )
                    data = cur.fetchall()
                    for item in data:
                        result.append([item[0]])
        finally:
            conn.close()
        return result

    def get_vacancies_with_keyword(self, key_word):
        """
        Получает список всех вакансий, в названии которых содержатся переданное слово
        :param key_word:
        :return:
        """
        config = configparser.ConfigParser()
        config.read("settings.ini")
        conn = psycopg2.connect(host=config['DBConfig']['host'], database=config['DBConfig']['database'],
                                user=config['DBConfig']['username'], password=config['DBConfig']['password'])
        result = []
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(
                        f"SELECT vacancy_name FROM vacancies "
                        f"WHERE vacancy_name LIKE '%{key_word.title()}%' OR vacancy_name LIKE '%{key_word.lower()}%'"
                    )
                    data = cur.fetchall()
                    for item in data:
                        result.append([item[0]])
        finally:
            conn.close()
        return result
        pass

    def fill_employers_db(self):
        """
        метод заполнения таблицы employers
        :return:
        """
        config = configparser.ConfigParser()
        config.read("settings.ini")
        conn = psycopg2.connect(host=config['DBConfig']['host'], database=config['DBConfig']['database'],
                                user=config['DBConfig']['username'], password=config['DBConfig']['password'])
        try:
            with conn:
                with conn.cursor() as cur:
                    for item in self.data:
                        cur.execute(
                            'INSERT INTO employers (employer_id, employer_name, open_vacancies, employer_url) VALUES (%s, %s, %s, %s)',
                            (item[0], item[1], item[3], item[2])
                        )
        finally:
            conn.close()

    def fill_vacancies_db(self):
        """
        метод заполнения таблицы vacancies
        :return:
        """
        config = configparser.ConfigParser()
        config.read("settings.ini")
        conn = psycopg2.connect(host=config['DBConfig']['host'], database=config['DBConfig']['database'],
                                user=config['DBConfig']['username'], password=config['DBConfig']['password'])
        try:
            with conn:
                with conn.cursor() as cur:
                    for item in self.data:
                        cur.execute(
                            'INSERT INTO vacancies (employer_id, vacancy_name, salary_from, salary_to, salary_currency, vacancy_notes, vacancy_url) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                            (item[0], item[2], item[5], item[6], item[7], item[4], item[3])
                        )
        finally:
            conn.close()

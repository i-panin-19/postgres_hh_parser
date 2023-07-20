import utils


if __name__ == '__main__':
    # заполняем бд
    utils.create_db_tables()
    # выполнение запросов и вывод результата на экран
    utils.requests_db()

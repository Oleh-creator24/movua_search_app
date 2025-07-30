from tabulate import tabulate  # Импортируем функцию для форматирования таблиц в виде ASCII-таблиц

# Функция для форматирования списка фильмов в виде табличного вывода
def format_movies(data):
    headers = ["Title", "Year", "Rating", "Genre"]  # Заголовки колонок
    return tabulate(data, headers=headers, tablefmt="grid")  # Преобразует список кортежей в ASCII-таблицу с рамками

# Функция для форматирования логов запросов (например, для вывода истории поисков)
def format_logs(logs):
    return "\n".join([
        f"{log['timestamp']} | {log['search_type']} | {log.get('params')} | results: {log['results_count']}"
        for log in logs  # Перебираем все логи и формируем строки с нужной информацией
    ])



import pymysql
from config import MYSQL_CONFIG  # Импорт настроек подключения к базе данных из внешнего файла

# Функция для установления соединения с базой данных
def get_connection():
    return pymysql.connect(**MYSQL_CONFIG)  # Возвращает объект подключения, используя параметры из конфигурации

# Поиск фильмов по ключевому слову в названии
def search_by_keyword(keyword, offset=0, limit=10):
    query = """
        SELECT film.title, film.release_year, film.rating, category.name AS genre
        FROM film
        JOIN film_category ON film.film_id = film_category.film_id
        JOIN category ON film_category.category_id = category.category_id
        WHERE film.title LIKE %s
        ORDER BY film.title
        LIMIT %s OFFSET %s
    """
    conn = get_connection()
    with conn:  # Гарантирует автоматическое закрытие соединения
        with conn.cursor() as cursor:  # Создаёт курсор для выполнения SQL-запроса
            # Выполняем запрос с параметрами:
            # %keyword% — для поиска части слова,
            # limit и offset — для пагинации
            cursor.execute(query, (f"%{keyword}%", limit, offset))
            return cursor.fetchall()  # Возвращаем список найденных фильмов

# Получение списка всех жанров (категорий фильмов)
def get_genres():
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            # Выполняем запрос на получение уникальных жанров
            cursor.execute("SELECT DISTINCT name FROM category ORDER BY name")
            # Возвращаем список жанров (в виде списка строк)
            return [row[0] for row in cursor.fetchall()]

# Получение диапазона лет выхода всех фильмов в базе
def get_year_range():
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            # Получаем минимальный и максимальный год выпуска фильмов
            cursor.execute("SELECT MIN(release_year), MAX(release_year) FROM film")
            return cursor.fetchone()  # Возвращаем кортеж (min_year, max_year)

# Поиск фильмов по жанру и диапазону годов выпуска
def search_by_genre_and_year(genre, year_from, year_to, offset=0, limit=10):
    query = """
        SELECT film.title, film.release_year, film.rating, category.name AS genre
        FROM film
        JOIN film_category ON film.film_id = film_category.film_id
        JOIN category ON film_category.category_id = category.category_id
        WHERE category.name = %s AND film.release_year BETWEEN %s AND %s
        ORDER BY film.title
        LIMIT %s OFFSET %s
    """
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            # Выполняем запрос с фильтрацией по жанру и диапазону годов
            cursor.execute(query, (genre, year_from, year_to, limit, offset))
            return cursor.fetchall()  # Возвращаем список найденных фильмов



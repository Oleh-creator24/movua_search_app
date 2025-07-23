
import pymysql
from config import MYSQL_CONFIG

def get_connection():
    return pymysql.connect(**MYSQL_CONFIG)

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
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (f"%{keyword}%", limit, offset))
            return cursor.fetchall()

def get_genres():
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT name FROM category ORDER BY name")
            return [row[0] for row in cursor.fetchall()]

def get_year_range():
    conn = get_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT MIN(release_year), MAX(release_year) FROM film")
            return cursor.fetchone()

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
            cursor.execute(query, (genre, year_from, year_to, limit, offset))
            return cursor.fetchall()




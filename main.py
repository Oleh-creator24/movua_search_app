
from mysql_connector import (
    search_by_keyword,
    get_genres,
    get_year_range,
    search_by_genre_and_year
)
from log_writer import log_search
from log_stats import get_last_queries, get_top_keywords
from formatter import format_movies, format_logs

def main():
    while True:
        print("\n--- Film Search ---")
        print("1. Поиск по ключевому слову")
        print("2. Поиск по жанру и году")
        print("3. Показать последние 5 запросов")
        print("4. Показать популярные ключевые слова")
        print("0. Выход")
        choice = input("Выбор: ")

        if choice == "1":
            while True:
                keyword = input("Введите ключевое слово: ")
                offset = 0
                results = search_by_keyword(keyword, offset)

                if not results:
                    print("Такой фразы в названии фильмов нет. Введите корректное значение или измените свой выбор.")
                    повтор = input("Хотите попробовать снова? (y/n): ")
                    if повтор.lower() != "y":
                        break
                    continue  # повтор запроса

                while True:
                    results = search_by_keyword(keyword, offset)

                    if not results:
                        # Не должно произойти, но защита на случай пустой страницы
                        print("Это список последних фильмов из Вашей подборки.")
                        break

                    print(format_movies(results))
                    log_search("keyword", {"keyword": keyword, "offset": offset}, len(results))

                    if len(results) < 10:
                        # Это последняя страница (меньше 10 фильмов)
                        print("Это список последних фильмов из Вашей подборки.")
                        break

                    more = input("Вывести следующие названия фильмов? (y/n): ")
                    if more.lower() != "y":
                        print("Выход в главное меню.")
                        break

                    offset += 10
                break  # завершить цикл после одного успешного поиска



        elif choice == "2":
            genres = get_genres()
            genres_lower = [g.lower() for g in genres]  # для регистронезависимого сравнения
            print("Жанры:", ", ".join(genres))
            year_min, year_max = get_year_range()
            print(f"Год выпуска: от {year_min} до {year_max}")

            # 🔁 Валидация ввода жанра
            while True:
                genre_input = input("Выберите жанр: ")

                # Проверка: только буквы (русские/английские), не пусто
                if not genre_input.isalpha():
                    print("Введите корректное название жанра заглавными или строчными буквами в соответствующей раскладке.")
                    continue

                # Приведение к нижнему регистру и проверка наличия в списке жанров
                if genre_input.lower() not in genres_lower:
                    print("Такой жанр не найден. Пожалуйста, выберите из предложенного списка.")
                    continue

                # Приводим к оригинальному виду (как в базе)
                genre_index = genres_lower.index(genre_input.lower())
                genre = genres[genre_index]
                break  # 🎯 Выход после успешного выбора жанра

            # 📆 Ввод диапазона годов с валидацией (вынесено НА СВОЙ УРОВЕНЬ)
            while True:
                try:
                    year_from = int(input("От года: "))
                    year_to = int(input("До года: "))

                    if (
                        year_from < year_min or
                        year_to > year_max or
                        year_from > year_to
                    ):
                        print("Введите корректное значение года согласно предложенного диапазона, включая начальные и конечные значения годов выхода фильмов.")
                        continue

                    break  # корректный ввод
                except ValueError:
                    print("Введите числовые значения для годов.")

            # 🔄 Вывод фильмов
            offset = 0
            while True:
                results = search_by_genre_and_year(genre, year_from, year_to, offset)
                print(format_movies(results))
                log_search("genre_year", {
                    "genre": genre,
                    "year_from": year_from,
                    "year_to": year_to
                }, len(results))
                if len(results) < 10:
                    print("Это список последних фильмов из Вашей подборки.")
                    break
                more = input("Показать ещё? (y/n): ")
                if more.lower() != "y":
                    print("Выход в главное меню.")
                    break
                offset += 10



        elif choice == "3":
            logs = get_last_queries()
            print(format_logs(logs))

        elif choice == "4":
            logs = get_top_keywords()
            for log in logs:
                print(f"{log['_id']} — {log['count']} запросов")

        elif choice == "0":
            print("Выход...")
            break
        else:
            print("Неверный выбор")

if __name__ == "__main__":
    main()





# Импорт функций для работы с базой данных MySQL
from mysql_connector import (
    search_by_keyword,         # Поиск фильмов по ключевому слову
    get_genres,                # Получение списка доступных жанров
    get_year_range,            # Получение диапазона годов выпуска фильмов
    search_by_genre_and_year  # Поиск по жанру и диапазону годов
)

# Импорт логирования запросов в MongoDB
from log_writer import log_search

# Импорт аналитики логов
from log_stats import get_last_queries, get_top_keywords, get_top_genre_year_queries

# Импорт форматирования результатов
from formatter import format_movies, format_logs

def main():
    while True:
        print("\n--- Film Search ---")
        print("1. Поиск по ключевому слову")
        print("2. Поиск по жанру и диапазону годов")
        print("3. Посмотреть популярные или последние запросы")
        print("4. Выход")
        choice = input("Выбор: ")

        if choice == "1":
            while True:
                keyword = input("Введите ключевое слово: ")
                offset = 0
                results = search_by_keyword(keyword, offset)

                if not results:
                    print("Такой фразы в названии фильмов нет.")
                    povtor = input("Хотите попробовать снова? (y/n): ")
                    if povtor.lower() != "y":
                        break
                    continue

                while True:
                    results = search_by_keyword(keyword, offset)

                    if not results:
                        print("Это список последних фильмов из Вашей подборки.")
                        break

                    print(format_movies(results))
                    log_search("keyword", {"keyword": keyword, "offset": offset}, len(results))

                    if len(results) < 10:
                        print("Это список последних фильмов из Вашей подборки.")
                        break

                    more = input("Вывести следующие названия фильмов? (y/n): ")
                    if more.lower() != "y":
                        break

                    offset += 10

                next_action = input("\nХотите выполнить другой поиск по ключевому слову? (y — да / n — в меню): ")
                if next_action.lower() != "y":
                    break


        # --- Поиск по жанру и диапазону годов ---
        elif choice == "2":
            genres = get_genres()  # получаем список жанров
            genres_lower = [g.lower() for g in genres]
            year_min, year_max = get_year_range()  # получаем диапазон годов

            while True:  # внешний цикл — повторяется, пока не выбран выход в главное меню
                # === Выбор жанра ===
                while True:
                    print("Жанры:", ", ".join(genres))
                    print(f"Год выпуска: от {year_min} до {year_max}")
                    genre_input = input("Выберите жанр: ")

                    if not genre_input.replace("-", "").replace(" ", "").isalpha():
                        print("Введите корректное название жанра.")
                        continue

                    if genre_input.lower() not in genres_lower:
                        print("Такой жанр не найден.")
                        continue

                    genre_index = genres_lower.index(genre_input.lower())
                    genre = genres[genre_index]  # сохраняем выбранный жанр
                    break  # выходим из цикла выбора жанра

                while True:  # цикл выбора диапазона годов для текущего жанра
                    # === Ввод диапазона годов ===
                    try:
                        year_from = int(input("От года: "))
                        year_to = int(input("До года: "))

                        if (
                                year_from < year_min or
                                year_to > year_max or
                                year_from > year_to
                        ):
                            print("Введите корректные значения годов.")
                            continue

                    except ValueError:
                        print("Введите числовые значения.")
                        continue

                    # === Показ фильмов ===
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
                            break

                        offset += 10

                    # === Подменю действий ===
                    next_action = input(
                        "\n1 — Новый жанр\n"
                        "2 — Новый диапазон годов в этом жанре\n"
                        "n — В главное меню\n"
                        "Выбор: "
                    )

                    if next_action == "1":
                        break  # выйти к выбору нового жанра (внешний цикл продолжается)
                    elif next_action == "2":
                        continue  # снова запросить годовой диапазон
                    elif next_action.lower() == "n":
                        # выйти в основное меню
                        # для этого нужно выйти из обоих вложенных циклов
                        genre = None  # очистить текущий жанр
                        break  # выйти из цикла диапазона годов

                if next_action.lower() == "n":
                    break  # выйти из внешнего цикла (возврат в главное меню)




        elif choice == "3":
            while True:
                print("\n1. Подборка по популярным ключевым словам")
                print("2. Последние 5 запросов")
                print("3. Популярные запросы по жанру и году выпуска")
                sub_choice = input("Выбор: ")

                if sub_choice == "1":
                    logs = get_top_keywords()
                    for log in logs:
                        print(f"{log['_id']} — {log['count']} запросов")

                elif sub_choice == "2":
                    logs = get_last_queries()
                    print(format_logs(logs))

                elif sub_choice == "3":
                    logs = get_top_genre_year_queries()
                    for log in logs:
                        genre = log['_id']['genre']
                        year_from = log['_id']['year_from']
                        year_to = log['_id']['year_to']
                        count = log['count']
                        print(f"{genre} ({year_from}-{year_to}) — {count} запросов")

                else:
                    print("Неверный выбор подменю. Пожалуйста, выберите 1, 2 или 3.")
                    continue

                next_action = input("\nХотите выполнить другое действие в этом разделе? (y — остаться / n — в меню): ")
                if next_action.lower() != "y":
                    break

        elif choice == "4":
            print("Выход...")
            break

        else:
            print("Неверный выбор. Пожалуйста, введите 1–4.")

if __name__ == "__main__":
    main()



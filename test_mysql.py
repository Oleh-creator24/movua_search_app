from mysql_connector import search_by_keyword, get_genres, get_year_range

def test_search():
    print("🔎 Поиск по ключевому слову 'academy'")
    results = search_by_keyword("academy")
    for row in results:
        print(row)

def test_genres():
    print("🎬 Список жанров:")
    for genre in get_genres():
        print("-", genre)

def test_year_range():
    print("📅 Диапазон годов выпуска:")
    print(get_year_range())

if __name__ == "__main__":
    test_search()
    test_genres()
    test_year_range()

from log_writer import log_search
from log_stats import get_last_queries

# Тест логирования
if __name__ == "__main__":
    print("Тест логирования в MongoDB...")

    # Пробуем записать тестовый запрос
    log_search(
        search_type="keyword",
        params={"keyword": "test_matrix"},
        results_count=42
    )
    print("✅ Лог записан")

    # Пробуем получить последние 5 логов
    logs = get_last_queries()
    print("\nПоследние запросы:")
    for log in logs:
        print(log)

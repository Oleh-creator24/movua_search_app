import os
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Получаем параметры подключения к MongoDB из переменных окружения
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME")

# Подключаемся к MongoDB
client = MongoClient(MONGO_URI)
collection = client[MONGO_DB_NAME][MONGO_COLLECTION_NAME]

def log_search(search_type, params, results_count):
    """
    Логирует информацию о поисковом запросе в MongoDB.

    :param search_type: тип запроса ("keyword" или "genre_year")
    :param params: параметры запроса (например, {"keyword": "action"} или {"genre": "Comedy", "year_from": 2000, "year_to": 2005})
    :param results_count: количество возвращённых результатов
    """
    log = {
        "timestamp": datetime.utcnow().isoformat(),  # текущее время в формате UTC ISO
        "search_type": search_type,                  # тип запроса
        "params": params,                            # параметры запроса
        "results_count": results_count               # количество найденных результатов
    }
    collection.insert_one(log)  # сохраняем лог в MongoDB




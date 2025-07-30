import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Подключение к MongoDB с использованием переменных окружения
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME")

client = MongoClient(MONGO_URI)
collection = client[MONGO_DB_NAME][MONGO_COLLECTION_NAME]

def get_last_queries(limit=5):
    """
    Получение последних поисковых запросов, отсортированных по времени.
    """
    return list(collection.find().sort("timestamp", -1).limit(limit))

def get_top_keywords(limit=5):
    """
    Получение самых популярных ключевых слов (type = 'keyword').
    """
    pipeline = [
        {"$match": {"search_type": "keyword"}},
        {"$group": {"_id": "$params.keyword", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": limit}
    ]
    return list(collection.aggregate(pipeline))

def get_top_genre_year_queries(limit=5):
    """
    Получение самых частых запросов по жанру и диапазону годов.
    """
    pipeline = [
        {"$match": {"search_type": "genre_year"}},
        {"$group": {
            "_id": {
                "genre": "$params.genre",
                "year_from": "$params.year_from",
                "year_to": "$params.year_to"
            },
            "count": {"$sum": 1}
        }},
        {"$sort": {"count": -1}},
        {"$limit": limit}
    ]
    return list(collection.aggregate(pipeline))


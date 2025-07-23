
from pymongo import MongoClient
from config import MONGO_URI, MONGO_DB_NAME, MONGO_COLLECTION_NAME

client = MongoClient(MONGO_URI)
collection = client[MONGO_DB_NAME][MONGO_COLLECTION_NAME]

def get_last_queries(limit=5):
    return list(collection.find().sort("timestamp", -1).limit(limit))

def get_top_keywords(limit=5):
    pipeline = [
        {"$match": {"search_type": "keyword"}},
        {"$group": {"_id": "$params.keyword", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": limit}
    ]
    return list(collection.aggregate(pipeline))


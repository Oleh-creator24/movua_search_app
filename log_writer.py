
from pymongo import MongoClient
from datetime import datetime
from config import MONGO_URI, MONGO_DB_NAME, MONGO_COLLECTION_NAME

client = MongoClient(MONGO_URI)
collection = client[MONGO_DB_NAME][MONGO_COLLECTION_NAME]

def log_search(search_type, params, results_count):
    log = {
        "timestamp": datetime.utcnow().isoformat(),
        "search_type": search_type,
        "params": params,
        "results_count": results_count
    }
    collection.insert_one(log)



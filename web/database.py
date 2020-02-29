from pymongo import MongoClient
from pprint import pprint
import secret

client = MongoClient(secret.mongodb_url_local)
db = client[secret.db_name]
categories = db[secret.collection_name]


def fetch_new_entry():
    results = list(categories.aggregate([{'$sample': {'size': 1}}]))
    if len(results) != 1:
        return None
    else:
        return results[0]

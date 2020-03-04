from pymongo import MongoClient
from pprint import pprint
import secret

client = MongoClient(secret.mongodb_url_local)
db = client[secret.db_name]
categories = db[secret.collection_name]


def fetch_new_entry():
    results = list(categories.aggregate([{'$match': {"annotation": {"$exists": False}}},
                                         {'$sample': {'size': 1}}]))
    if len(results) != 1:
        return None
    else:
        return results[0]


def write_interests(category_id, interests):
    # category = categories.find_one({'category_id': category_id})
    categories.update_one({'category_id': category_id},
                          {'$set': {
                              'annotation': ', '.join(interests)
                          }}, upsert=False)

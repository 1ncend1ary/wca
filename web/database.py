from pymongo import MongoClient
from pprint import pprint
import secret

client = MongoClient(secret.mongodb_url)
db = client.new
categories = db.categories


def fetch_new_entry():
    results = list(categories.aggregate([{'$sample': {'size': 1}}]))
    if len(results) != 1:
        return None
    else:
        # result = results[0]
        return results[0]

# print(db.list_collection_names())
# pprint(categories.find_one())

from pymongo import MongoClient
from pprint import pprint
import secret

# from main import login

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


user_db = client[secret.db_name_users]
users = user_db[secret.collection_name_users]


# @login.user_loader
# def load_user(user_id):
#     return users.find_one({'id': user_id})
# return User.query.get(int(user_id))


def find_user(username):
    pass

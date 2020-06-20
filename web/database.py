# -*- coding: utf-8 -*-
"""
MongoDB database handling module

Programmer: Aleksei Seliverstov <alexseliverstov@yahoo.com>
"""
from pymongo import MongoClient
import web.secret as secret
from web import logger

client = MongoClient(secret.mongodb_url_local)


class Categories:
    """
    MongoDB categories expecting to be annotated class
    """
    __db = client[secret.db_name]
    __categories = __db[secret.collection_name]

    def get_random(self):
        """
        Get a random annotation from the mongodb database

        Fetches a single random entry without an existing annotation
        """
        category = list(self.__categories.aggregate([{'$match': {"annotation": {"$exists": False}}},
                                                     {'$sample': {'size': 1}}]))
        logger.info('Successfully retrieved an annotation from the database.')
        return None if len(category) != 1 else category[0]

    def add_annotations(self, category_id, annotations):
        """
        Add a list of annotations to the category specified by category_id
        """
        self.__categories.update_one({'category_id': category_id},
                                     {'$set': {
                                         'annotation': ', '.join(annotations)
                                     }}, upsert=False)
        logger.info('Successfully written annotations to the database.')

    def __new__(cls):
        """
        Declare this class as singleton

        This method is initiated before __init__ and check whether an instance of this class already exists
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super(Categories, cls).__new__(cls)
        return cls.instance

# class Users:
#     """
#     MongoDB users password/login credentials database
#     """
#     __user_db = client[secret.db_name_users]
#     __users = __user_db[secret.collection_name_users]
#
#     def __new__(cls):
#         """
#         Declare this class as singleton
#
#         This method is initiated before __init__ and check whether an instance of this class already exists
#         """
#         if not hasattr(cls, 'instance'):
#             cls.instance = super(Users, cls).__new__(cls)
#         return cls.instance

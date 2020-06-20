# -*- coding: utf-8 -*-
"""
MongoDB database handling module

Programmer: Aleksei Seliverstov <alexseliverstov@yahoo.com>
"""
from web import logger
from flask_login import UserMixin
from web import secret, client


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


class User(UserMixin):
    """
    Flask user representation model class.
    """
    __user_db = client[secret.db_name_users]
    __users = __user_db[secret.collection_name_users]

    def __init__(self, username, password):
        self.id = username
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User {}>'.format(self.username)

    @classmethod
    def get(cls, user_id):
        user_db_entry = cls.__users.find_one({'login': str(user_id)})

        if user_db_entry is None:
            logger.info('Not found user by their login.')
            return None
        else:
            user = User(user_db_entry['login'], user_db_entry['password'])
            logger.info('Found user with id: {}.'.format(user_id))
            return user

    def check_password(self, password):
        return self.password == password

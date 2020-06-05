# -*- coding: utf-8 -*-
"""
Flask models representation module

Programmer: Aleksei Seliverstov <alexseliverstov@yahoo.com>
"""
from flask_login import UserMixin
import secret


class User(UserMixin):
    """
    Flask user representation model class.
    """

    def __init__(self, username, password):
        self.id = username
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User {}>'.format(self.username)

    @classmethod
    def get(cls, user_id):
        return secret.user_database.get(user_id)

    def check_password(self, password):
        return self.password == password

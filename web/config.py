import os


class Config(object):
    """
    Flask application configuration object class
    """
    SECRET_KEY = os.urandom(32)

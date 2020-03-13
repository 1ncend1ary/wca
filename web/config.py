# -*- coding: utf-8 -*-
"""
Flask application configuration module

Programmer: Aleksei Seliverstov <alexseliverstov@yahoo.com>
"""
import os


class Config(object):
    """
    Flask application configuration object class
    """
    SECRET_KEY = os.urandom(32)

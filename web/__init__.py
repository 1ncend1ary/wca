#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Initialization file for module 'web'.

__author__ = "Aleksei Seliverstov"
__license__ = "MIT"
__email__ = "alexseliverstov@yahoo.com"
"""
from flask import Flask
from flask_login import LoginManager
from web import secret
from web.config import Config
from pymongo import MongoClient
import logging

# Create a custom logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the flask application instance
app = Flask(__name__)
app.config.from_object(Config)

# Create a login manager for flask-login
login_manager = LoginManager()
login_manager.init_app(app)

# Create a client for mongodb connections via 'pymongo'
client = MongoClient(secret.mongodb_url_local)

from web import database
from web import interests

db = database.Categories()
requester = interests.FacebookRequest()

logger.info('App has been initialized.')

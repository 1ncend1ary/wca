from flask import Flask
from flask_login import LoginManager
from web.config import Config
import logging
from web import secret
from pymongo import MongoClient

# Create a custom logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

login_manager = LoginManager()

app = Flask(__name__)
app.config.from_object(Config)
login_manager.init_app(app)

client = MongoClient(secret.mongodb_url_local)

from web import database
from web import interests

db = database.Categories()
requester = interests.FacebookRequest()

logger.info('App has been initialized.')

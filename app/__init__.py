from flask import Flask
from mongoengine import connect as mongo_connect
from app.config import Config
from app.routes import api as api_blueprint
import logging


def init_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db_settings = app.config.get('MONGODB_SETTINGS', {})
    if db_settings:
        try:
            mongo_connect(**db_settings)
        except Exception as e:
            logging.error(f"Failed to connect to MongoDB: {e}")
    else:
        logging.warning("No MongoDB settings provided.")

    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app

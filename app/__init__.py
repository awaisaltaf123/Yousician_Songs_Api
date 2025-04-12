from flask import Flask
from mongoengine import connect
from app.config import Config
from app.routes import api

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    connect(**app.config['MONGODB_SETTINGS'])
    app.register_blueprint(api, url_prefix='/api')
    return app
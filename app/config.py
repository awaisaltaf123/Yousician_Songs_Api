import os

class AppConfig:
    DB_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/songs_db')

    MONGO_CONF = {
        'host': DB_URI,
        'uuidRepresentation': 'standard',
    }

    DEFAULT_PAGE_SIZE = 10

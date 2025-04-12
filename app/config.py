import os

class Config:
    MONGODB_SETTINGS = {
        'host': os.getenv('MONGO_URI', 'mongodb://localhost:27017/songs_db'),
        'uuidRepresentation': 'standard'
    }
    PAGE_SIZE = 10
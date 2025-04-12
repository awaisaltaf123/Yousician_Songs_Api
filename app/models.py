from mongoengine import Document, StringField, FloatField, IntField, ListField
from bson.json_util import JSONOptions, UuidRepresentation

JSON_OPTIONS = JSONOptions(uuid_representation=UuidRepresentation.STANDARD)

class Song(Document):
    artist = StringField(required=True)
    title = StringField(required=True)
    difficulty = FloatField(required=True)
    level = IntField(required=True)
    released = StringField(required=True)
    ratings = ListField(IntField(min_value=1, max_value=5))

    meta = {
        'collection': 'songs',
        'indexes': [
            'artist',
            'title',
            ('artist', 'title'),
            'level'
        ],
        'json_options': JSON_OPTIONS
    }
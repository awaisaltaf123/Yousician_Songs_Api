from mongoengine import Document, StringField, FloatField, IntField, ListField
from bson.json_util import JSONOptions, UuidRepresentation

JSON_CFG = JSONOptions(uuid_representation=UuidRepresentation.STANDARD)

class SongModel(Document):
    artist_name = StringField(required=True)
    song_title = StringField(required=True)
    difficulty_score = FloatField(required=True)
    game_level = IntField(required=True)
    release_date = StringField(required=True)
    user_ratings = ListField(IntField(min_value=1, max_value=5))

    meta = {
        'collection': 'songs',
        'indexes': [
            'artist_name',
            'song_title',
            ('artist_name', 'song_title'),
            'game_level'
        ],
        'json_options': JSON_CFG
    }

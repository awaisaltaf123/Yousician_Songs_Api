import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models import Song

from mongoengine import connect
import json

connect(host='mongodb://localhost:27017/songs_db')

with open('data/songs.json') as f:
    songs = json.load(f)
    Song.objects.delete()
    for song in songs:
        Song(**song).save()

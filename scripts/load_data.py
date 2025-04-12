import os
import sys
import json
from mongoengine import connect

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.models import SongModel

connect(host='mongodb://localhost:27017/songs_db')

def load_seed_data():
    file_path = os.path.join(BASE_DIR, 'data', 'songs.json')
    
    if not os.path.exists(file_path):
        print(f"Seed file not found at: {file_path}")
        return

    try:
        with open(file_path, 'r') as f:
            data = json.load(f)

        SongModel.objects.delete()

        for entry in data:
            try:
                SongModel(**entry).save()
            except Exception as e:
                print(f"Skipped entry due to error: {e}")

        print(f"Loaded {len(data)} songs into the database.")

    except Exception as err:
        print(f"Failed to load seed data: {err}")


if __name__ == '__main__':
    load_seed_data()

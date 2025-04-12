import unittest
import json
from app import create_app
from mongoengine import connect, disconnect
from mongomock import MongoClient
from app.models import Song

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        disconnect()
        connect(
            'mongoenginetest',
            host='mongodb://localhost',
            mongo_client_class=MongoClient,
            uuidRepresentation='standard'
        )

        with open('tests/test_data.json') as f:
            songs = json.load(f)
            for song in songs:
                Song(**song).save()

    def tearDown(self):
        Song.drop_collection()
        disconnect()

    def test_list_songs(self):
        response = self.client.get('/api/songs?page=1&per_page=2')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['songs']), 2)
        self.assertEqual(data['total'], 3)

    def test_average_difficulty(self):
        response = self.client.get('/api/songs/difficulty')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertAlmostEqual(data['average_difficulty'], 12.9, places=2)

    def test_average_difficulty_by_level(self):
        response = self.client.get('/api/songs/difficulty?level=13')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertAlmostEqual(data['average_difficulty'], 14.8, places=2)

    def test_search_songs(self):
        response = self.client.get('/api/songs/search?message=you')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['songs']), 2)

    def test_add_rating(self):
        song = Song.objects.first()
        response = self.client.post('/api/songs/rating',
                                  json={'song_id': str(song.id), 'rating': 4})
        self.assertEqual(response.status_code, 200)
        updated_song = Song.objects(id=song.id).first()
        self.assertIn(4, updated_song.ratings)

    def test_add_invalid_rating(self):
        song = Song.objects.first()
        response = self.client.post('/api/songs/rating',
                                  json={'song_id': str(song.id), 'rating': 6})
        self.assertEqual(response.status_code, 400)

    def test_get_ratings(self):
        song = Song.objects.first()
        song.ratings = [1, 3, 5]
        song.save()
        response = self.client.get(f'/api/songs/{song.id}/ratings')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['average_rating'], 3.0)
        self.assertEqual(data['lowest_rating'], 1)
        self.assertEqual(data['highest_rating'], 5)

if __name__ == '__main__':
    unittest.main()
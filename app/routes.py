from flask import Blueprint, jsonify, request
from mongoengine import Q
from app.models import Song
from app.config import Config
from bson import ObjectId
from statistics import mean

api = Blueprint('api', __name__)

@api.route('/songs', methods=['GET'])
def list_songs():
    """Returns a paginated list of songs."""
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', Config.PAGE_SIZE))
    skip = (page - 1) * per_page

    songs = Song.objects.skip(skip).limit(per_page)
    total = Song.objects.count()

    return jsonify({
        'songs': [song.to_json() for song in songs],
        'total': total,
        'page': page,
        'per_page': per_page
    })

@api.route('/songs/difficulty', methods=['GET'])
def average_difficulty():
    """Returns the average difficulty, optionally filtered by level."""
    level = request.args.get('level')
    query = Song.objects
    if level:
        try:
            query = query.filter(level=int(level))
        except ValueError:
            return jsonify({'error': 'Invalid level parameter'}), 400

    difficulties = [song.difficulty for song in query]
    if not difficulties:
        return jsonify({'average_difficulty': 0})

    return jsonify({'average_difficulty': round(mean(difficulties), 2)})

@api.route('/songs/search', methods=['GET'])
def search_songs():
    """Searches songs by artist or title (case-insensitive)."""
    message = request.args.get('message')
    if not message:
        return jsonify({'error': 'Missing message parameter'}), 400

    query = Q(artist__icontains=message) | Q(title__icontains=message)
    songs = Song.objects(query)

    return jsonify({'songs': [song.to_json() for song in songs]})

@api.route('/songs/rating', methods=['POST'])
def add_rating():
    """Adds a rating to a song."""
    data = request.get_json()
    song_id = data.get('song_id')
    rating = data.get('rating')

    if not song_id or rating is None:
        return jsonify({'error': 'Missing song_id or rating'}), 400

    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({'error': 'Rating must be an integer between 1 and 5'}), 400

    try:
        song = Song.objects(id=song_id).first()
        if not song:
            return jsonify({'error': 'Song not found'}), 404

        song.ratings.append(rating)
        song.save()
        return jsonify({'message': 'Rating added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@api.route('/songs/<song_id>/ratings', methods=['GET'])
def get_ratings(song_id):
    """Returns average, lowest, and highest rating for a song."""
    song = Song.objects(id=song_id).first()
    if not song:
        return jsonify({'error': 'Song not found'}), 404

    ratings = song.ratings
    if not ratings:
        return jsonify({
            'average_rating': 0,
            'lowest_rating': 0,
            'highest_rating': 0
        })

    return jsonify({
        'average_rating': round(mean(ratings), 2),
        'lowest_rating': min(ratings),
        'highest_rating': max(ratings)
    })
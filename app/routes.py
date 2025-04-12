from flask import Blueprint, jsonify, request
from mongoengine import Q
from bson import ObjectId
from statistics import mean
from app.models import Song
from app.config import AppConfig

songs_api = Blueprint('songs_api', __name__)

@songs_api.route('/songs', methods=['GET'])
def get_all_songs():
    """Paginated fetch of song documents."""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', AppConfig.DEFAULT_PAGE_SIZE))
    except ValueError:
        return jsonify({'error': 'Invalid pagination params'}), 400

    offset = (page - 1) * per_page
    results = Song.objects.skip(offset).limit(per_page)
    total_count = Song.objects.count()

    return jsonify({
        'songs': [song.to_json() for song in results],
        'total': total_count,
        'page': page,
        'per_page': per_page
    })


@songs_api.route('/songs/difficulty', methods=['GET'])
def get_avg_difficulty():
    """Compute average difficulty, filtered optionally by level."""
    level_param = request.args.get('level')
    query = Song.objects

    if level_param:
        try:
            level = int(level_param)
            query = query.filter(game_level=level)
        except ValueError:
            return jsonify({'error': 'Level must be an integer'}), 400

    difficulties = [s.difficulty_score for s in query]
    avg = round(mean(difficulties), 2) if difficulties else 0

    return jsonify({'average_difficulty': avg})


@songs_api.route('/songs/search', methods=['GET'])
def search_song_by_keyword():
    """Case-insensitive search across artist or title fields."""
    keyword = request.args.get('message')
    if not keyword:
        return jsonify({'error': 'Query parameter "message" is required'}), 400

    search_query = Q(artist_name__icontains=keyword) | Q(song_title__icontains=keyword)
    results = Song.objects(search_query)

    return jsonify({'songs': [song.to_json() for song in results]})


@songs_api.route('/songs/rating', methods=['POST'])
def submit_rating():
    """Append a new rating to a song entry."""
    payload = request.get_json(force=True)
    song_id = payload.get('song_id')
    rating = payload.get('rating')

    if not song_id or rating is None:
        return jsonify({'error': 'song_id and rating are required'}), 400

    try:
        rating = int(rating)
        if rating not in range(1, 6):
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid rating format'}), 400

    song = Song.objects(id=song_id).first()
    if not song:
        return jsonify({'error': 'No song found with that ID'}), 404

    try:
        song.user_ratings.append(rating)
        song.save()
    except Exception as err:
        return jsonify({'error': f'Could not save rating: {err}'}), 500

    return jsonify({'message': 'Rating submitted successfully'})


@songs_api.route('/songs/<song_id>/ratings', methods=['GET'])
def get_song_ratings(song_id):
    """Get summary of song's ratings (avg, min, max)."""
    song = Song.objects(id=song_id).first()
    if not song:
        return jsonify({'error': 'Song not found'}), 404

    ratings = song.user_ratings
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

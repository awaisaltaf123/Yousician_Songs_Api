# Songs API

A Flask-based REST API for managing songs and their ratings, backed by MongoDB. This project implements the requirements for the Yousician Backend Developer Assignment, providing endpoints to list songs, calculate average difficulty, search songs, add ratings, and retrieve rating statistics.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
  - [Using Docker](#using-docker)
  - [Manual Setup (Without Docker)](#manual-setup-without-docker)
- [Loading Initial Data](#loading-initial-data)
- [API Endpoints](#api-endpoints)
- [Running Tests](#running-tests)
- [Scalability Considerations](#scalability-considerations)
- [Troubleshooting](#troubleshooting)

## Prerequisites

- **Docker** and **Docker Compose** (recommended for easiest setup)
- **Python 3.11** (preferred; Python 3.8+ is supported)
- **MongoDB** (if not using Docker; version 4.4 recommended)
- **Git** (optional, for cloning the repository)
- Internet access (to pull Docker images and Python packages)

## Project Structure

```plaintext
songs_api/
├── app/
│   ├── __init__.py         # Flask app initialization
│   ├── config.py           # Configuration settings
│   ├── models.py           # MongoDB schema definitions
│   ├── routes.py           # API route definitions
├── data/
│   └── songs.json          # Initial song data
├── scripts/
│   └── load_data.py        # Script to load songs.json into MongoDB
├── tests/
│   ├── __init__.py
│   ├── test_routes.py      # Unit tests for API endpoints
│   ├── test_data.json      # Test data for unit tests
├── Dockerfile              # Docker configuration for Flask app
├── docker-compose.yml      # Docker Compose configuration
├── requirements.txt        # Python dependencies
├── run.py                  # Entry point for Flask app
└── README.md               # This file
```

## Setup Instructions

### Using Docker

The recommended way to run the project is with Docker, which handles MongoDB and the Flask app in isolated containers.

1. **Clone the Repository** (if applicable):
   ```bash
   git clone https://github.com/awaisaltaf123/Yousician_Songs_Api.git
   cd Yousician_Songs_Api
   ```

2. **Start Docker Containers**:
   ```bash
   docker-compose up --build -d
   ```
   - This pulls `mongo:4.4`, builds the Flask app image, and starts:
     - MongoDB on `localhost:27017`
     - Flask API on `localhost:5000`
   - The `-d` flag runs containers in the background.

3. **Verify Services**:
   ```bash
   docker ps
   ```
   You should see `songs_api_mongo_1` and `songs_api_app_1` running.

4. **Load Initial Data**:
   See [Loading Initial Data](#loading-initial-data) below to populate MongoDB with `songs.json`.

### Manual Setup (Without Docker)

If you prefer to run MongoDB and the Flask app locally:

1. **Install Python 3.11**:
   - Download and install from [python.org](https://www.python.org/downloads/release/python-31110/).
   - Verify:
     ```bash
     python --version
     ```

2. **Set Up Virtual Environment**:
   ```bash
   cd D:\Assessment\Yousician\songs_api
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run MongoDB Locally**:
   - Install MongoDB 4.4 (or compatible) from [mongodb.com](https://www.mongodb.com/try/download/community).
   - Start MongoDB:
     ```bash
     mongod
     ```
   - Ensure it’s running on `localhost:27017`.

5. **Run the Flask App**:
   ```bash
   python run.py
   ```
   The API will be available at `http://localhost:5000/api`.

6. **Load Initial Data**:
   See [Loading Initial Data](#loading-initial-data) below.

## Loading Initial Data

The `songs.json` file in `data/` contains the initial song data. To load it into MongoDB:

1. **Ensure MongoDB is Running**:
   - Via Docker: `docker-compose up -d`
   - Or locally: `mongod`

2. **Run the Load Script**:
   ```bash
   cd D:\Assessment\Yousician\songs_api
   venv\Scripts\activate
   python .\scripts\load_data.py
   ```
   This:
   - Connects to `mongodb://localhost:27017/songs_db`
   - Clears existing songs
   - Loads songs from `data/songs.json`

3. **Verify Data**:
   ```bash
   docker exec -it yousician_songs_api-mongo-1 mongo
   > use songs_db
   > db.songs.find().pretty()
   ```
   Or, if local:
   ```bash
   mongo
   > use songs_db
   > db.songs.find().pretty()
   ```
   You should see 11 songs.

Alternatively, load data inside the Docker container:
```bash
docker exec -it songs_api_app_1 python /app/scripts/load_data.py
```

## API Endpoints

All endpoints are prefixed with `/api` and return JSON responses.

| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/songs` | GET | Lists songs with pagination | `page` (int, default: 1), `per_page` (int, default: 10) |
| `/songs/difficulty` | GET | Returns average difficulty, optionally filtered by level | `level` (int, optional) |
| `/songs/search` | GET | Searches songs by artist or title (case-insensitive) | `message` (string, required) |
| `/songs/rating` | POST | Adds a rating (1-5) to a song | JSON body: `{"song_id": "<id>", "rating": <int>}` |
| `/songs/<song_id>/ratings` | GET | Returns average, lowest, and highest ratings for a song | `song_id` (string, in URL) |

**Example Requests**:
- List songs:
  ```bash
  curl http://localhost:5000/api/songs?page=1&per_page=5
  ```
- Get average difficulty for level 13:
  ```bash
  curl http://localhost:5000/api/songs/difficulty?level=13
  ```
- Search for "Yousicians":
  ```bash
  curl http://localhost:5000/api/songs/search?message=Yousicians
  ```
- Add a rating:
  ```bash
  curl -X POST http://localhost:5000/api/songs/rating -H "Content-Type: application/json" -d '{"song_id": "<song_id>", "rating": 4}'
  ```
- Get ratings for a song:
  ```bash
  curl http://localhost:5000/api/songs/<song_id>/ratings
  ```

## Running Tests

The project includes unit tests for all API endpoints using `unittest` and `mongomock`.

1. **Ensure Dependencies**:
   ```bash
   cd D:\Assessment\Yousician\songs_api
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Run Tests**:
   ```bash
   python -m unittest discover tests
   ```
   This runs all tests in `tests/test_routes.py`, covering:
   - Song listing and pagination
   - Average difficulty (with/without level filter)
   - Search functionality
   - Adding ratings (valid and invalid)
   - Retrieving rating statistics

3. **Expected Output**:
   A summary like:
   ```
   ......
   ----------------------------------------------------------------------
   Ran 6 tests in 0.123s
   OK
   ```

## Scalability Considerations

- **MongoDB Indexes**: Indexes on `artist`, `title`, and `level` ensure efficient queries for searching, filtering, and sorting, supporting millions of songs and ratings.
- **Pagination**: The `/songs` endpoint uses skip/limit pagination to handle large datasets. For very high scale, cursor-based pagination could be implemented.
- **Embedded Ratings**: Ratings are stored in the `Song` document to reduce joins, optimized for read-heavy workloads. For high write volumes, a separate ratings collection could be considered.
- **MongoDB Scaling**: MongoDB supports sharding and replication for horizontal scaling, suitable for millions of documents and users.
- **Performance**: Input validation and error handling prevent database bloat. Future enhancements could include caching (e.g., Redis) for frequent queries.

## Troubleshooting

- **ModuleNotFoundError: No module named 'app'**:
  - Ensure `app/` directory exists with `__init__.py` and `models.py`.
  - Run scripts from project root:
    ```bash
    cd D:\Assessment\Yousician\songs_api
    python .\scripts\load_data.py
    ```
  - Set `PYTHONPATH`:
    ```bash
    set PYTHONPATH=D:\Assessment\Yousician\songs_api
    ```

- **MongoDB Connection Issues**:
  - Verify MongoDB is running:
    ```bash
    docker ps
    ```
  - Check connection:
    ```bash
    docker exec -it songs_api_mongo_1 mongo --eval "db.getMongo()"
    ```

- **Empty Database**:
  - Run `scripts/load_data.py` to populate `songs.json`:
    ```bash
    python .\scripts\load_data.py
    ```
  - Verify:
    ```bash
    docker exec -it songs_api_mongo_1 mongo --eval "use songs_db; db.songs.find()"
    ```

- **Docker Issues**:
  - Ensure Docker Desktop is running.
  - Rebuild containers:
    ```bash
    docker-compose down
    docker-compose up --build -d
    ```

For further assistance, check logs:
```bash
docker logs songs_api_app_1
docker logs songs_api_mongo_1
```

If the `ModuleNotFoundError` persists after trying the above, share the directory listings, and I’ll help pinpoint the exact issue (e.g., missing `app/` or incorrect paths). Let me know how it goes!
# Music Players Integration

A Python library that provides a unified interface to search and retrieve song information from multiple music streaming platforms:
- Spotify
- YouTube Music
- Deezer

## Features

- Search songs by name and artist across supported platforms
- Extract song information from platform-specific URLs
- Convert music links between different platforms
- Web interface for easy link conversion
- REST API endpoint for programmatic access

## Setup

1. Install the required packages:
```bash
pip install -e .
```

2. Set up your API credentials:
   - Copy `.env.example` to `.env`
   - Fill in your API credentials:
     - For Spotify: Get credentials from [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Set a secret key for Flask:
     ```
     FLASK_SECRET_KEY=your_secret_key_here
     ```

## Usage

### Web Interface

1. Start the web server:
```bash
python app.py
```

2. Open your browser and go to `http://localhost:5000`

3. Paste a music link from any supported platform (Spotify, Deezer, or YouTube Music)

4. Click "Convert" to get links to the same song on other platforms

### REST API

You can also use the REST API endpoint to convert links programmatically:

```python
import requests

response = requests.post('http://localhost:5000/api/convert', 
    json={'url': 'https://open.spotify.com/track/your_track_id'})
result = response.json()
```

### Python Library

```python
from music_search import MusicPlatform

# Initialize the client
music = MusicPlatform()

# 1. Search for a song across all platforms
results = music.search_track("Bohemian Rhapsody", "Queen")
print(results)

# 2. Search on a specific platform
spotify_results = music.search_track("Bohemian Rhapsody", "Queen", platform="spotify")
print(spotify_results)

# 3. Get song info from a platform-specific URL
url = "https://open.spotify.com/track/your_track_id"
song_info = music.get_song_info(url)
print(song_info)
```

## Response Format

All methods return a dictionary with standardized fields:

```python
{
    'title': 'Song Title',
    'artist': 'Artist Name',
    'album': 'Album Name',
    'url': 'Platform-specific URL'
}
```

If an error occurs, the response will be:
```python
{
    'error': 'Error message'
}
```

## Error Handling

The library handles various error cases gracefully:
- Missing API credentials
- Network errors
- Invalid URLs
- No search results

Each error will return a dictionary with an 'error' key explaining the issue.

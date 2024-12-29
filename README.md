# Music Players Integration

A Python library that provides a unified interface to search and retrieve song information from multiple music streaming platforms:
- Spotify
- YouTube Music
- Apple Music
- Deezer

## Features

- Search songs by name and artist across all supported platforms
- Extract song information from platform-specific URLs
- Unified response format across all platforms
- Type hints for better development experience

## Setup

1. Install the required packages:
```bash
pip install -e .
```

2. Set up your API credentials:
   - Copy `.env.example` to `.env`
   - Fill in your API credentials:
     - For Spotify: Get credentials from [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
     - For Apple Music: Get credentials from [Apple Developer](https://developer.apple.com/documentation/applemusicapi)
     - Deezer and YouTube Music don't require credentials for basic usage

## Usage

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

import os
import requests
from urllib.parse import urlparse, quote
import re
from typing import Dict, Optional, Any
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from ytmusicapi import YTMusic
import applemusicpy
from yandex_music import Client as YandexMusicClient
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class MusicPlatform:
    def __init__(self):
        # Initialize API clients
        self._init_spotify()
        self._init_ytmusic()
        self._init_apple_music()
        self._init_yandex_music()
        
        # Platform URL patterns
        self.platforms = {
            'deezer.page.link': self.handle_deezer,
            'deezer.com': self.handle_deezer,         # https://www.deezer.com/track/12345
            'open.spotify.com': self.handle_spotify,   # https://open.spotify.com/track/12345
            'music.apple.com': self.handle_apple_music,# https://music.apple.com/us/album/song/12345
            'music.youtube.com': self.handle_youtube_music, # https://music.youtube.com/watch?v=12345
            'music.yandex.com': self.handle_yandex_music,  # https://music.yandex.com/album/12345/track/67890
            'music.yandex.ru': self.handle_yandex_music    # https://music.yandex.ru/album/12345/track/67890
        }

    def _init_spotify(self):
        """Initialize Spotify client"""
        try:
            client_id = os.getenv('SPOTIFY_CLIENT_ID')
            client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
            if client_id and client_secret:
                self.spotify = spotipy.Spotify(
                    client_credentials_manager=SpotifyClientCredentials(
                        client_id=client_id,
                        client_secret=client_secret
                    )
                )
            else:
                self.spotify = None
        except Exception:
            self.spotify = None

    def _init_ytmusic(self):
        """Initialize YouTube Music client"""
        try:
            print("Initializing YouTube Music client...")
            self.ytmusic = YTMusic()
            print("YouTube Music client initialized successfully")
        except Exception as e:
            print(f"Error initializing YouTube Music client: {str(e)}")
            self.ytmusic = None

    def _init_apple_music(self):
        """Initialize Apple Music client"""
        try:
            key_id = os.getenv('APPLE_KEY_ID')
            team_id = os.getenv('APPLE_TEAM_ID')
            secret_key = os.getenv('APPLE_SECRET_KEY')
            if all([key_id, team_id, secret_key]):
                self.apple_music = applemusicpy.AppleMusic(secret_key, key_id, team_id)
            else:
                self.apple_music = None
        except Exception:
            self.apple_music = None

    def _init_yandex_music(self):
        """Initialize Yandex Music client"""
        try:
            token = os.getenv('YANDEX_MUSIC_TOKEN')
            if token:
                self.yandex = YandexMusicClient(token).init()
            else:
                self.yandex = None
        except Exception:
            self.yandex = None

    def get_song_info(self, url: str) -> Dict[str, Any]:
        """Extract song information from any supported music platform URL"""
        try:
            domain = urlparse(url).netloc.replace('www.', '')
            base_domain = next((k for k in self.platforms.keys() if k in domain), None)
            
            if base_domain:
                return self.platforms[base_domain](url)
            else:
                return {"error": "Unsupported platform"}
        except Exception as e:
            return {"error": f"Failed to process URL: {str(e)}"}

    def handle_deezer(self, url: str) -> Dict[str, Any]:
        """Handle Deezer links"""
        try:
            response = requests.get(url, allow_redirects=True)
            final_url = response.url
            
            track_id = final_url.split('track/')[1].split('?')[0]
            api_url = f"https://api.deezer.com/track/{track_id}"
            
            response = requests.get(api_url)
            data = response.json()
            
            return {
                'platform': 'deezer',
                'song': data['title'],
                'artist': data['artist']['name'],
                'album': data['album']['title'],
                'url': data['link']
            }
        except Exception as e:
            return {"error": f"Deezer processing failed: {str(e)}"}

    def handle_spotify(self, url: str) -> Dict[str, Any]:
        """Handle Spotify links"""
        if not self.spotify:
            return {"error": "Spotify API credentials not configured"}
        
        try:
            track_id = url.split('track/')[1].split('?')[0]
            track = self.spotify.track(track_id)
            
            return {
                'platform': 'spotify',
                'song': track['name'],
                'artist': track['artists'][0]['name'],
                'album': track['album']['name'],
                'url': track['external_urls']['spotify']
            }
        except Exception as e:
            return {"error": f"Spotify processing failed: {str(e)}"}

    def handle_apple_music(self, url: str) -> Dict[str, Any]:
        """Handle Apple Music links"""
        if not self.apple_music:
            return {"error": "Apple Music API credentials not configured"}
        
        try:
            # Extract song ID from URL (format: https://music.apple.com/us/album/song-name/id)
            song_id = url.split('/')[-1]
            result = self.apple_music.song(song_id)
            
            return {
                'platform': 'apple_music',
                'song': result['data'][0]['attributes']['name'],
                'artist': result['data'][0]['attributes']['artistName'],
                'album': result['data'][0]['attributes']['albumName'],
                'url': result['data'][0]['attributes']['url']
            }
        except Exception as e:
            return {"error": f"Apple Music processing failed: {str(e)}"}

    def handle_youtube_music(self, url: str) -> Dict[str, Any]:
        """Handle YouTube Music links"""
        if not self.ytmusic:
            return {"error": "YouTube Music API not initialized"}
        
        try:
            # Extract video ID from URL
            video_id = url.split('watch?v=')[1].split('&')[0]
            result = self.ytmusic.get_song(video_id)
            
            return {
                'platform': 'youtube_music',
                'song': result['title'],
                'artist': result['artists'][0]['name'],
                'album': result.get('album', {}).get('name', 'N/A'),
                'url': f"https://music.youtube.com/watch?v={video_id}"
            }
        except Exception as e:
            return {"error": f"YouTube Music processing failed: {str(e)}"}

    def handle_yandex_music(self, url: str) -> Dict[str, Any]:
        """Handle Yandex Music links"""
        if not self.yandex:
            return {"error": "Yandex Music API credentials not configured"}
        
        try:
            # Extract track and album IDs from URL
            # Format: https://music.yandex.ru/album/{album_id}/track/{track_id}
            album_id = url.split('album/')[1].split('/')[0]
            track_id = url.split('track/')[1].split('?')[0]
            
            track = self.yandex.tracks([f"{track_id}:{album_id}"])[0]
            
            return {
                'platform': 'yandex_music',
                'song': track.title,
                'artist': track.artists[0].name,
                'album': track.albums[0].title,
                'url': f"https://music.yandex.ru/album/{album_id}/track/{track_id}"
            }
        except Exception as e:
            return {"error": f"Yandex Music processing failed: {str(e)}"}

    def search_track(self, song_name: str, artist_name: str, platform: str = "all") -> Dict[str, Any]:
        """Search for a track across all platforms or a specific platform"""
        results = {}
        
        if platform == "all" or platform == "deezer":
            results['deezer'] = self._search_deezer(song_name, artist_name)
            
        if platform == "all" or platform == "spotify":
            results['spotify'] = self._search_spotify(song_name, artist_name)
            
        if platform == "all" or platform == "apple_music":
            results['apple_music'] = self._search_apple_music(song_name, artist_name)
            
        if platform == "all" or platform == "youtube_music":
            results['youtube_music'] = self._search_youtube_music(song_name, artist_name)
            
        if platform == "all" or platform == "yandex_music":
            results['yandex_music'] = self._search_yandex_music(song_name, artist_name)
            
        return results

    def _search_deezer(self, song_name: str, artist_name: str) -> Dict[str, Any]:
        """Search on Deezer"""
        try:
            # Create a more specific search query for tracks
            query = quote(f'track:"{song_name}" artist:"{artist_name}"')
            search_url = "https://api.deezer.com/search/track"  # Use track-specific endpoint
            response = requests.get(search_url, params={
                'q': query,
                'strict': 'on'  # Enable strict mode for more accurate results
            })
            data = response.json()
            
            if not data.get('data'):
                return {"error": "No results found"}
                
            track = data['data'][0]
            return {
                'title': track['title'],
                'artist': track['artist']['name'],
                'album': track['album']['title'],
                'url': track['link']
            }
        except Exception as e:
            return {"error": f"Search failed: {str(e)}"}

    def _search_spotify(self, song_name: str, artist_name: str) -> Dict[str, Any]:
        """Search on Spotify"""
        if not self.spotify:
            return {"error": "Spotify API credentials not configured"}
        
        try:
            query = f"track:{song_name} artist:{artist_name}"
            results = self.spotify.search(q=query, type='track', limit=1)
            
            if not results['tracks']['items']:
                return {"error": "No results found"}
            
            track = results['tracks']['items'][0]
            return {
                'title': track['name'],
                'artist': track['artists'][0]['name'],
                'album': track['album']['name'],
                'url': track['external_urls']['spotify']
            }
        except Exception as e:
            return {"error": f"Search failed: {str(e)}"}

    def _search_apple_music(self, song_name: str, artist_name: str) -> Dict[str, Any]:
        """Search on Apple Music"""
        if not self.apple_music:
            return {"error": "Apple Music API credentials not configured"}
        
        try:
            query = f"{song_name} {artist_name}"
            results = self.apple_music.search(query, types=['songs'], limit=1)
            
            if not results['songs']['data']:
                return {"error": "No results found"}
            
            track = results['songs']['data'][0]['attributes']
            return {
                'title': track['name'],
                'artist': track['artistName'],
                'album': track['albumName'],
                'url': track['url']
            }
        except Exception as e:
            return {"error": f"Search failed: {str(e)}"}

    def _search_youtube_music(self, song_name: str, artist_name: str) -> Dict[str, Any]:
        """Search on YouTube Music"""
        if not self.ytmusic:
            print("YouTube Music API not initialized, returning error")
            return {"error": "YouTube Music API not initialized"}
        
        try:
            print(f"Searching YouTube Music for: {song_name} by {artist_name}")
            query = f"{song_name} {artist_name}"
            results = self.ytmusic.search(query, filter="songs", limit=1)
            
            if not results:
                print("No results found on YouTube Music")
                return {"error": "No results found"}
            
            track = results[0]
            print(f"Found track on YouTube Music: {track['title']}")
            return {
                'title': track['title'],
                'artist': track['artists'][0]['name'],
                'album': track.get('album', {}).get('name', 'N/A'),
                'url': f"https://music.youtube.com/watch?v={track['videoId']}"
            }
        except Exception as e:
            print(f"Error searching YouTube Music: {str(e)}")
            return {"error": f"Search failed: {str(e)}"}

    def _search_yandex_music(self, song_name: str, artist_name: str) -> Dict[str, Any]:
        """Search on Yandex Music"""
        if not self.yandex:
            return {"error": "Yandex Music API credentials not configured"}
        
        try:
            query = f"{song_name} {artist_name}"
            results = self.yandex.search(query, type_='track')
            
            if not results.tracks or not results.tracks.results:
                return {"error": "No results found"}
            
            track = results.tracks.results[0]
            return {
                'title': track.title,
                'artist': track.artists[0].name,
                'album': track.albums[0].title,
                'url': f"https://music.yandex.ru/album/{track.albums[0].id}/track/{track.id}"
            }
        except Exception as e:
            return {"error": f"Search failed: {str(e)}"}

# Example usage
if __name__ == "__main__":
    music = MusicPlatform()
    
    # Example 1: Get song info from different platform URLs
    urls = [
        "https://www.deezer.com/track/3135556",
        "https://open.spotify.com/track/6rPO02ozF3bM7NnOV4h6s2",
        "https://music.apple.com/us/album/bohemian-rhapsody/1440806041?i=1440806768",
        "https://music.youtube.com/watch?v=fJ9rUzIMcZQ",
        "https://music.yandex.ru/album/297670/track/2867727"
    ]
    
    for url in urls:
        result = music.get_song_info(url)
        print(f"\nSong info from {url}:", result)
    
    # Example 2: Search for a track across all platforms
    search_result = music.search_track("Bohemian Rhapsody", "Queen")
    print("\nSearch results:", search_result)
import requests

def get_song_info(deezer_url):
    try:
        # Follow redirects to get the full URL
        response = requests.get(deezer_url, allow_redirects=True)
        response.raise_for_status()
        
        # Get the final URL after redirects
        final_url = response.url
        
        # Extract track ID from the final URL
        track_id = final_url.split('track/')[1].split('?')[0]
        
        # Deezer API endpoint
        api_url = f"https://api.deezer.com/track/{track_id}"
        
        # Make API request
        response = requests.get(api_url)
        response.raise_for_status()
        
        # Parse response
        data = response.json()
        
        # Extract song info
        song_name = data['title']
        artist_name = data['artist']['name']
        
        return {
            'song': song_name,
            'artist': artist_name
        }
    except Exception as e:
        return f"Error: {str(e)}"

def find_track(song_name, artist_name):
    try:
        # Create search query
        query = f"{song_name} artist:'{artist_name}'"
        
        # Deezer search API endpoint
        search_url = "https://api.deezer.com/search"
        params = {
            'q': query
        }
        
        # Make API request
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        
        # Parse response
        data = response.json()
        
        if not data.get('data'):
            return "No tracks found"
            
        # Get the first result
        track = data['data'][0]
        
        return {
            'track_id': track['id'],
            'title': track['title'],
            'artist': track['artist']['name'],
            'album': track['album']['title'],
            'duration': track['duration'],  # duration in seconds
            'preview': track['preview'],    # 30-second preview URL
            'link': track['link']          # Deezer track URL
        }
        
    except Exception as e:
        return f"Error: {str(e)}"

# Example usage
if __name__ == "__main__":
    # First, get song info from URL
    deezer_url = "https://deezer.page.link/nikuG1hQefajJXkZA"
    song_info = get_song_info(deezer_url)
    print("Original song info:", song_info)
    
    # Then use that info to find the track
    if isinstance(song_info, dict):
        result = find_track(song_info['song'], song_info['artist'])
        print("\nFound track details:", result)
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
    
    except requests.exceptions.RequestException as e:
        return f"Error fetching data: {str(e)}"
    except KeyError as e:
        return f"Error parsing response: {str(e)}"
    except IndexError:
        return "Invalid Deezer URL format"

# Example usage
if __name__ == "__main__":
    deezer_url = "https://deezer.page.link/nikuG1hQefajJXkZA"
    result = get_song_info(deezer_url)
    print(result)
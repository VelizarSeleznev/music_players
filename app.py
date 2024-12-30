from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from music_search import MusicPlatform
import os
from dotenv import load_dotenv
from flask_cors import CORS
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Flask app once
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev')

# Configure CORS with specific options
CORS(app, resources={
    r"/api/*": {
        "origins": ["chrome-extension://*", "http://localhost:*"],
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

class MusicLinkForm(FlaskForm):
    url = StringField('Music URL', validators=[DataRequired(), URL()])
    submit = SubmitField('Convert')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = MusicLinkForm()
    result = None
    error = None
    
    if form.validate_on_submit():
        music = MusicPlatform()
        url = form.url.data
        
        # Get song info from the provided URL
        song_info = music.get_song_info(url)
        
        if 'error' in song_info:
            error = song_info['error']
        else:
            # Search for the song on other platforms
            search_results = music.search_track(
                song_info['song'],
                song_info['artist'],
                platform="all"
            )
            
            # Filter to include only Deezer, Spotify, and YouTube Music
            result = {
                'original': {
                    'platform': song_info['platform'],
                    'song': song_info['song'],
                    'artist': song_info['artist'],
                    'url': song_info['url']
                },
                'alternatives': {}
            }
            
            # Add alternative platform links if they exist and aren't the original platform
            for platform in ['deezer', 'spotify', 'youtube_music']:
                if platform != song_info['platform'] and platform in search_results:
                    platform_result = search_results[platform]
                    if 'error' not in platform_result:
                        result['alternatives'][platform] = platform_result
    
    return render_template('index.html', form=form, result=result, error=error)

@app.route('/api/convert', methods=['POST'])
def convert_api():
    try:
        logger.debug(f"Received request: {request.json}")
        
        url = request.json.get('url')
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        logger.debug(f"Processing URL: {url}")
        music = MusicPlatform()
        
        # Get song info from the provided URL
        song_info = music.get_song_info(url)
        logger.debug(f"Song info: {song_info}")
        
        if 'error' in song_info:
            logger.error(f"Error in song info: {song_info['error']}")
            return jsonify({'error': song_info['error']}), 400
        
        # Search for the song on other platforms
        search_results = music.search_track(
            song_info['song'],
            song_info['artist'],
            platform="all"
        )
        logger.debug(f"Search results: {search_results}")
        
        # Filter to include only Deezer, Spotify, and YouTube Music
        result = {
            'original': {
                'platform': song_info['platform'],
                'song': song_info['song'],
                'artist': song_info['artist'],
                'url': song_info['url']
            },
            'alternatives': {}
        }
        
        # Add alternative platform links if they exist and aren't the original platform
        for platform in ['deezer', 'spotify', 'youtube_music']:
            if platform != song_info['platform'] and platform in search_results:
                platform_result = search_results[platform]
                if 'error' not in platform_result:
                    result['alternatives'][platform] = platform_result
        
        logger.debug(f"Sending response: {result}")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True) 
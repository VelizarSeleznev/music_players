from PIL import Image
import os

def resize_icon(input_path, output_path, size):
    """Resize an image to a specific size and save it."""
    with Image.open(input_path) as img:
        # Convert to RGBA if not already
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        # Resize image
        resized = img.resize((size, size), Image.Resampling.LANCZOS)
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        # Save resized image
        resized.save(output_path, 'PNG')

def main():
    # Source icons
    icons = {
        'spotify': 'static/spotify.png',
        'deezer': 'static/deezer.png',
        'youtube_music': 'static/youtube_music.png'
    }
    
    # Required sizes for Chrome extension
    sizes = [16, 48, 128]
    
    # Create icons directory if it doesn't exist
    os.makedirs('extension/icons', exist_ok=True)
    source_path = 'static/icon.png'
    # Process each icon
    for size in sizes:
        output_path = f'extension/icons/icon{size}.png'
        resize_icon(source_path, output_path, size)
        print(f"Created {size}x{size} icon")

if __name__ == '__main__':
    main()
    print("Icon resizing complete!") 
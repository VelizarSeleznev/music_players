// Listen for page load
document.addEventListener('DOMContentLoaded', () => {
  // Get the current URL
  const currentUrl = window.location.href;
  
  // Check if we're on a music platform page with a track
  if (isTrackPage(currentUrl)) {
    // Send message to popup that we're on a valid music page
    chrome.runtime.sendMessage({
      type: 'VALID_MUSIC_PAGE',
      url: currentUrl
    });
  }
});

// Function to check if the current page is a track page
function isTrackPage(url) {
  // Spotify track pattern
  if (url.match(/spotify\.com\/track\/[a-zA-Z0-9]+/)) {
    return true;
  }
  
  // Deezer track pattern
  if (url.match(/deezer\.com\/[a-z]+\/track\/[0-9]+/)) {
    return true;
  }
  
  // YouTube Music track pattern
  if (url.match(/music\.youtube\.com\/watch\?v=[a-zA-Z0-9_-]+/)) {
    return true;
  }
  
  return false;
} 
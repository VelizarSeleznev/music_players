document.addEventListener('DOMContentLoaded', () => {
  console.log('Extension popup opened');
  // Get current active tab
  chrome.tabs.query({active: true, currentWindow: true}, async (tabs) => {
    const currentUrl = tabs[0].url;
    console.log('Current URL:', currentUrl);
    
    try {
      console.log('Sending request to API...');
      // Call your API endpoint
      const response = await fetch('http://127.0.0.1:5000/api/convert', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: currentUrl })
      });
      
      console.log('API Response status:', response.status);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('API Response data:', data);
      
      if (data.error) {
        console.error('API returned error:', data.error);
        showError(`Error: ${data.error}`);
        return;
      }
      
      // Update UI with results
      updateUI(data);
    } catch (error) {
      console.error('Error details:', error);
      if (error.message.includes('Failed to fetch')) {
        showError('Cannot connect to the server. Make sure the application is running on localhost:5000');
      } else {
        showError(`Error: ${error.message}`);
      }
    }
  });
});

function updateUI(data) {
  // Hide loading, show content
  document.getElementById('loading').style.display = 'none';
  document.getElementById('content').style.display = 'block';
  
  // Update song info
  document.getElementById('songTitle').textContent = data.original.song;
  document.getElementById('artistName').textContent = data.original.artist;
  
  // Clear existing links
  const linksContainer = document.getElementById('links');
  linksContainer.innerHTML = '';
  
  // Add alternative platform links
  Object.entries(data.alternatives).forEach(([platform, info]) => {
    const link = document.createElement('a');
    link.href = info.url;
    link.className = `platform-link ${platform}`;
    link.textContent = `Open in ${formatPlatformName(platform)}`;
    link.target = '_blank';
    linksContainer.appendChild(link);
  });
}

function showError(message) {
  console.error('Showing error:', message);
  document.getElementById('loading').style.display = 'none';
  const errorElement = document.getElementById('error');
  errorElement.textContent = message;
  errorElement.style.display = 'block';
}

function formatPlatformName(platform) {
  const names = {
    'spotify': 'Spotify',
    'deezer': 'Deezer',
    'youtube_music': 'YouTube Music'
  };
  return names[platform] || platform;
} 
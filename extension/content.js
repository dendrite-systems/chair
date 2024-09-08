

async function uploadVideo(base64String) {
  const url = 'http://localhost:5050/upload_video';
  console.log('Uploading video to:', url);
  console.log('String:', base64String);

  
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        'video_base64': base64String
      }),
    });


    if (!response.ok) {
      console.error('HTTP error! status:', response.status);
      throw new Error(`HTTP error! status: ${response.status}`);
    }


    const result = await response.json();
    console.log('Upload successful:', result);
    return result;
  } catch (error) {
    console.error('Error uploading video:', error);
    throw error;
  }
}

// Wait for the endedRecording message from recording_screen.js
chrome.runtime.onMessage.addListener((request) => {
  console.log('onMessage', request);
  if (request.name !== 'endedRecording') {
    return;
  }


  console.log('Uploading video');
  uploadVideo(request.body.base64)
  .then(result => {
    console.log('Uploaded file:', result.filename);
  })
  .catch(error => {
    console.error('Upload failed:', error);
  });


  // Create a new video element and show it in an overlay div (a lot of styles just for fun)
  const video = document.createElement('video');
  video.src = request.body.base64;
  video.controls = true;
  video.autoplay = true;
  video.style.width = '100%';
  video.style.height = '100%';
  video.style.maxWidth = '600px';
  video.style.maxHeight = '600px';

  const overlay = document.createElement('div');
  overlay.style.position = 'fixed';
  overlay.style.top = 0;
  overlay.style.left = 0;
  overlay.style.width = '100%';
  overlay.style.height = '100%';
  overlay.style.backdropFilter = 'blur(5px)';
  overlay.style.zIndex = 999999

  overlay.appendChild(video);

  document.body.appendChild(overlay);
});
const fetchBlob = async (url) => {
  const response = await fetch(url);
  const blob = await response.blob();
  const base64 = await convertBlobToBase64(blob);

  return base64;
};

const convertBlobToBase64 = (blob) => {
  return new Promise(resolve => {
    const reader = new FileReader();
    reader.readAsDataURL(blob);
    reader.onloadend = () => {
      const base64data = reader.result;

      resolve(base64data);
    };
  });
};

chrome.runtime.onMessage.addListener((message) => {
  if (message.name !== 'startRecordingOnBackground') {
    return;
  }

  // Prompt user to choose screen or window
  chrome.desktopCapture.chooseDesktopMedia(
    ['screen', 'window'],
    function (streamId) {
      if (streamId == null) {
        return;
      }

      // Once user has chosen screen or window, create a stream from it and start recording
      navigator.mediaDevices.getUserMedia({
        audio: false,
        video: {
          mandatory: {
            chromeMediaSource: 'desktop',
            chromeMediaSourceId: streamId,
          }
        }
      }).then(stream => {
        const mediaRecorder = new MediaRecorder(stream);

        const chunks = [];

        mediaRecorder.ondataavailable = function(e) {
          chunks.push(e.data);
        };

        mediaRecorder.onstop = async function(e) {
          const blobFile = new Blob(chunks, { type: "video/webm" });
          const base64 = await fetchBlob(URL.createObjectURL(blobFile));

          // When recording is finished, send message to current tab content script with the base64 video
          chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
            const tabWhenRecordingStopped = tabs[0];

            chrome.tabs.sendMessage(tabWhenRecordingStopped.id, {
              name: 'endedRecording',
              body: {
                base64,
              }
            })

            window.close();
          });

          // Stop all tracks of stream
          stream.getTracks().forEach(track => track.stop());
        }

        mediaRecorder.start();
      }).finally(async () => {
        // After all setup, focus on previous tab (where the recording was requested)
        await chrome.tabs.update(message.body.currentTab.id, { active: true, selected: true })
      });
    })
});

async function uploadVideo(base64String) {
  const url = 'http://localhost:5050/upload_video';
  console.log('Uploading video to:', url);
  
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        video_base64: base64String
      }),
    });


    if (!response.ok) {
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


// Usage
const base64Video = 'your-base64-encoded-video-string';
uploadVideo(base64Video)
  .then(result => {
    console.log('Uploaded file:', result.filename);
  })
  .catch(error => {
    console.error('Upload failed:', error);
  });


let recorder;
let chunks = [];

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "start") {
    startRecording();
  } else if (request.action === "stop") {
    stopRecording();
  }
});

function startRecording() {
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    let tab = tabs[0];
    chrome.tabCapture.capture({
      video: true,
      audio: true,
      videoConstraints: {
        mandatory: {
          chromeMediaSource: 'tab',
          maxWidth: 1920,
          maxHeight: 1080
        }
      }
    }, function(stream) {
      if (stream) {
        recorder = new MediaRecorder(stream, {mimeType: 'video/webm'});
        
        recorder.ondataavailable = event => {
          if (event.data.size > 0) {
            chunks.push(event.data);
          }
        };

        recorder.onstop = () => {
          const blob = new Blob(chunks, { type: 'video/webm' });
          const url = URL.createObjectURL(blob);
          chrome.tabs.create({ url: url });
          chunks = [];
        };

        recorder.start(1000); // Start recording, and dump data every 1 second
        console.log('Recording started');
      } else {
        console.error('Error starting tab capture');
        alert('Failed to capture tab. Please try again.');
      }
    });
  });
}

function stopRecording() {
  if (recorder && recorder.state !== 'inactive') {
    recorder.stop();
    console.log('Recording stopped');
  }
}
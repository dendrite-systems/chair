let startButton = document.getElementById('startRecording');
let stopButton = document.getElementById('stopRecording');

startButton.onclick = () => {
  chrome.runtime.sendMessage({action: "start"});
  startButton.disabled = true;
  stopButton.disabled = false;
};

stopButton.onclick = () => {
  chrome.runtime.sendMessage({action: "stop"});
  startButton.disabled = false;
  stopButton.disabled = true;
};
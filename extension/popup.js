const startRecording = () => {
  chrome.runtime.sendMessage({ name: 'startRecording' });
};

document.addEventListener('DOMContentLoaded', () => {
  console.log('DOMContentLoaded');
  document.getElementById('startRecordingButton').addEventListener('click', startRecording);
});
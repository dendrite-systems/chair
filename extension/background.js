const startRecording = async () => {
  await chrome.tabs.query({'active': true, 'lastFocusedWindow': true, 'currentWindow': true}, async function (tabs) {
    // Get current tab to focus on it after start recording on recording screen tab
    const currentTab = tabs[0];

    // Create recording screen tab
    console.log('Creating recording screen tab');
    const tab = await chrome.tabs.create({
      url: chrome.runtime.getURL('recording_screen.html'),
      pinned: true,
      active: true,
    });

    // Wait for recording screen tab to be loaded and send message to it with the currentTab
    console.log('Waiting for recording screen tab to be loaded');
    chrome.tabs.onUpdated.addListener(async function listener(tabId, info) {
      if (tabId === tab.id && info.status === 'complete') {
        chrome.tabs.onUpdated.removeListener(listener);

        console.log('Sending message to recording screen tab');
        await chrome.tabs.sendMessage(tabId, {
          name: 'startRecordingOnBackground',
          body: {
            currentTab: currentTab,
          },
        });
        console.log('Message sent to recording screen tab');
      }
    });
  });
};

// Listen for startRecording message from popup.js
console.log('Listening for startRecording message');
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.name === 'startRecording') {
    startRecording();
  }
});
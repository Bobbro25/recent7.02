// Popup JavaScript for Block Trump Extension
/* global chrome */

document.addEventListener('DOMContentLoaded', async function() {
  const toggleSwitch = document.getElementById('toggleSwitch');
  const statusIndicator = document.getElementById('statusIndicator');
  const blockedCountElement = document.getElementById('blockedCount');
  
  // Load current settings
  let isEnabled = true;
  try {
    const result = await chrome.storage.sync.get(['isEnabled']);
    isEnabled = result.isEnabled !== false; // Default to true
  } catch (error) {
    console.log('Storage not available, using default settings');
  }
  
  // Update UI based on current state
  updateUI(isEnabled);
  
  // Get blocked count from current tab
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    // Execute a script to get the blocked count
    const results = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      function: getBlockedCount
    });
    
    if (results && results[0] && results[0].result !== undefined) {
      blockedCountElement.textContent = results[0].result;
    }
  } catch (error) {
    console.log('Could not get blocked count:', error);
  }
  
  // Toggle switch click handler
  toggleSwitch.addEventListener('click', async function() {
    isEnabled = !isEnabled;
    
    // Save new state
    try {
      await chrome.storage.sync.set({ isEnabled: isEnabled });
    } catch (error) {
      console.log('Could not save settings:', error);
    }
    
    // Update UI
    updateUI(isEnabled);
    
    // Reload current tab to apply changes
    try {
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      await chrome.tabs.reload(tab.id);
      
      // Close popup after a short delay
      setTimeout(() => {
        window.close();
      }, 500);
    } catch (error) {
      console.log('Could not reload tab:', error);
    }
  });
  
  function updateUI(enabled) {
    if (enabled) {
      toggleSwitch.classList.add('active');
      statusIndicator.classList.remove('disabled');
    } else {
      toggleSwitch.classList.remove('active');
      statusIndicator.classList.add('disabled');
    }
  }
});

// Function to be injected into the current tab to get blocked count
function getBlockedCount() {
  const blockedElements = document.querySelectorAll('.trump-blocked-content');
  return blockedElements.length;
}
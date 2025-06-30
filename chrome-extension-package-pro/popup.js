// Popup JavaScript for Block Trump Extension Pro
/* global chrome */

document.addEventListener('DOMContentLoaded', async function() {
  const toggleSwitch = document.getElementById('toggleSwitch');
  const statusIndicator = document.getElementById('statusIndicator');
  const blockedCountElement = document.getElementById('blockedCount');
  const totalBlockedElement = document.getElementById('totalBlocked');
  
  // Tab switching functionality
  const tabs = document.querySelectorAll('.tab');
  const tabContents = document.querySelectorAll('.tab-content');
  
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const targetTab = tab.getAttribute('data-tab');
      
      // Remove active class from all tabs and contents
      tabs.forEach(t => t.classList.remove('active'));
      tabContents.forEach(tc => tc.classList.remove('active'));
      
      // Add active class to clicked tab and corresponding content
      tab.classList.add('active');
      document.getElementById(targetTab).classList.add('active');
    });
  });
  
  // Load current settings
  let isEnabled = true;
  let settings = {
    theme: 'classic',
    customMessage: 'Trump content blocked',
    animations: true,
    sounds: false,
    showCount: true,
    totalBlocked: 0,
    sitesVisited: 0,
    textBlocked: 0,
    imageBlocked: 0,
    videoBlocked: 0
  };
  
  try {
    const result = await chrome.storage.sync.get(['isEnabled', 'proSettings']);
    isEnabled = result.isEnabled !== false;
    if (result.proSettings) {
      settings = { ...settings, ...result.proSettings };
    }
  } catch (error) {
    console.log('Storage not available, using default settings');
  }
  
  // Initialize UI
  updateUI(isEnabled);
  loadThemeSettings();
  loadStatistics();
  
  // Get blocked count from current tab
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
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
  
  // Main toggle switch
  toggleSwitch.addEventListener('click', async function() {
    isEnabled = !isEnabled;
    
    try {
      await chrome.storage.sync.set({ isEnabled: isEnabled });
    } catch (error) {
      console.log('Could not save settings:', error);
    }
    
    updateUI(isEnabled);
    
    try {
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      await chrome.tabs.reload(tab.id);
      
      setTimeout(() => {
        window.close();
      }, 500);
    } catch (error) {
      console.log('Could not reload tab:', error);
    }
  });
  
  // Theme selection
  const themeOptions = document.querySelectorAll('.theme-option');
  themeOptions.forEach(option => {
    option.addEventListener('click', () => {
      themeOptions.forEach(opt => opt.classList.remove('selected'));
      option.classList.add('selected');
      settings.theme = option.getAttribute('data-theme');
    });
  });
  
  // Custom message input
  const customMessageInput = document.getElementById('customMessage');
  customMessageInput.addEventListener('input', () => {
    settings.customMessage = customMessageInput.value;
  });
  
  // Save theme settings
  document.getElementById('saveTheme').addEventListener('click', async () => {
    try {
      await chrome.storage.sync.set({ proSettings: settings });
      showSaveNotification('Theme settings saved!');
    } catch (error) {
      console.log('Could not save theme settings:', error);
    }
  });
  
  // Settings toggles
  const settingsToggles = {
    animationToggle: 'animations',
    soundToggle: 'sounds',
    countToggle: 'showCount'
  };
  
  Object.entries(settingsToggles).forEach(([toggleId, settingKey]) => {
    const toggle = document.getElementById(toggleId);
    if (settings[settingKey]) {
      toggle.classList.add('active');
    }
    
    toggle.addEventListener('click', () => {
      toggle.classList.toggle('active');
      settings[settingKey] = toggle.classList.contains('active');
    });
  });
  
  // Save all settings
  document.getElementById('saveSettings').addEventListener('click', async () => {
    try {
      await chrome.storage.sync.set({ proSettings: settings });
      showSaveNotification('All settings saved!');
    } catch (error) {
      console.log('Could not save settings:', error);
    }
  });
  
  // Reset settings
  document.getElementById('resetSettings').addEventListener('click', async () => {
    if (confirm('Reset all settings to defaults?')) {
      settings = {
        theme: 'classic',
        customMessage: 'Trump content blocked',
        animations: true,
        sounds: false,
        showCount: true,
        totalBlocked: 0,
        sitesVisited: 0,
        textBlocked: 0,
        imageBlocked: 0,
        videoBlocked: 0
      };
      
      try {
        await chrome.storage.sync.set({ proSettings: settings });
        loadThemeSettings();
        showSaveNotification('Settings reset to defaults!');
      } catch (error) {
        console.log('Could not reset settings:', error);
      }
    }
  });
  
  // Export statistics
  document.getElementById('exportStats').addEventListener('click', () => {
    const statsData = {
      totalBlocked: settings.totalBlocked,
      sitesVisited: settings.sitesVisited,
      textBlocked: settings.textBlocked,
      imageBlocked: settings.imageBlocked,
      videoBlocked: settings.videoBlocked,
      exportDate: new Date().toISOString()
    };
    
    const dataStr = JSON.stringify(statsData, null, 2);
    const dataBlob = new Blob([dataStr], {type: 'application/json'});
    const url = URL.createObjectURL(dataBlob);
    
    // Create download link
    const link = document.createElement('a');
    link.href = url;
    link.download = 'block-trump-stats.json';
    link.click();
    
    showSaveNotification('Statistics exported!');
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
  
  function loadThemeSettings() {
    // Set selected theme
    themeOptions.forEach(option => {
      option.classList.remove('selected');
      if (option.getAttribute('data-theme') === settings.theme) {
        option.classList.add('selected');
      }
    });
    
    // Set custom message
    customMessageInput.value = settings.customMessage;
    
    // Update total blocked display
    if (totalBlockedElement) {
      totalBlockedElement.textContent = settings.totalBlocked || 0;
    }
  }
  
  function loadStatistics() {
    // Update statistics display
    const stats = [
      { id: 'textCount', progressId: 'textProgress', value: settings.textBlocked || 0 },
      { id: 'imageCount', progressId: 'imageProgress', value: settings.imageBlocked || 0 },
      { id: 'videoCount', progressId: 'videoProgress', value: settings.videoBlocked || 0 }
    ];
    
    const total = stats.reduce((sum, stat) => sum + stat.value, 0);
    
    stats.forEach(stat => {
      const element = document.getElementById(stat.id);
      const progressElement = document.getElementById(stat.progressId);
      
      if (element) element.textContent = stat.value;
      if (progressElement && total > 0) {
        const percentage = (stat.value / total) * 100;
        progressElement.style.width = percentage + '%';
      }
    });
    
    // Update other stats
    const sitesElement = document.getElementById('sitesVisited');
    const avgElement = document.getElementById('avgPerSite');
    
    if (sitesElement) sitesElement.textContent = settings.sitesVisited || 0;
    if (avgElement) {
      const avg = settings.sitesVisited > 0 ? Math.round(total / settings.sitesVisited) : 0;
      avgElement.textContent = avg;
    }
    
    if (totalBlockedElement) {
      totalBlockedElement.textContent = total;
    }
  }
  
  function showSaveNotification(message) {
    // Create temporary notification
    const notification = document.createElement('div');
    notification.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      background: #4CAF50;
      color: white;
      padding: 10px 20px;
      border-radius: 8px;
      font-size: 0.9em;
      z-index: 1000;
      animation: slideIn 0.3s ease;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
      notification.remove();
    }, 2000);
  }
});

// Function to be injected into the current tab to get blocked count
function getBlockedCount() {
  const blockedElements = document.querySelectorAll('.trump-blocked-content');
  return blockedElements.length;
}
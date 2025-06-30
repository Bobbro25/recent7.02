// Block Trump Chrome Extension Pro - Content Script
/* global chrome */

class TrumpBlockerPro {
  constructor() {
    this.isEnabled = true;
    this.keywords = [
      'donald trump',
      'donald j. trump',
      'djt',
      'potus 47',
      '45'
    ];
    this.blockedCount = 0;
    this.observer = null;
    this.settings = {
      theme: 'classic',
      customMessage: 'Trump content blocked',
      animations: true,
      sounds: false,
      showCount: true
    };
    
    this.init();
  }

  async init() {
    // Load settings from storage
    try {
      const result = await chrome.storage.sync.get(['isEnabled', 'proSettings']);
      this.isEnabled = result.isEnabled !== false;
      
      if (result.proSettings) {
        this.settings = { ...this.settings, ...result.proSettings };
      }
    } catch (error) {
      console.log('Storage not available, using default settings');
      this.isEnabled = true;
    }
    
    if (this.isEnabled) {
      this.blockExistingContent();
      this.startObserver();
    }
    
    // Listen for storage changes
    if (chrome && chrome.storage) {
      chrome.storage.onChanged.addListener((changes) => {
        if (changes.isEnabled) {
          this.isEnabled = changes.isEnabled.newValue;
          if (this.isEnabled) {
            this.blockExistingContent();
            this.startObserver();
          } else {
            this.stopObserver();
            this.unblockContent();
          }
        }
        
        if (changes.proSettings) {
          this.settings = { ...this.settings, ...changes.proSettings.newValue };
          this.updateBlockedElements();
        }
      });
    }
  }

  containsTrumpKeywords(text) {
    if (!text) return false;
    const lowerText = text.toLowerCase();
    return this.keywords.some(keyword => lowerText.includes(keyword));
  }

  blockExistingContent() {
    this.blockTextElements();
    this.blockImages();
    this.blockVideos();
  }

  blockTextElements() {
    const textElements = document.querySelectorAll('p, div, span, h1, h2, h3, h4, h5, h6, article, section, li, td, th');
    
    textElements.forEach(element => {
      if (element.dataset.trumpBlocked) return;
      
      if (this.containsTrumpKeywords(element.textContent)) {
        this.replaceWithBlockedMessage(element, 'text');
      }
    });
  }

  blockImages() {
    const images = document.querySelectorAll('img');
    
    images.forEach(img => {
      if (img.dataset.trumpBlocked) return;
      
      const altText = img.alt || '';
      const title = img.title || '';
      const src = img.src || '';
      
      if (this.containsTrumpKeywords(altText) || 
          this.containsTrumpKeywords(title) || 
          this.containsTrumpKeywords(src)) {
        this.replaceWithBlockedMessage(img, 'image');
      }
    });
  }

  blockVideos() {
    const videos = document.querySelectorAll('video, iframe[src*="youtube"], iframe[src*="vimeo"], iframe[src*="twitter"], iframe[src*="facebook"]');
    
    videos.forEach(video => {
      if (video.dataset.trumpBlocked) return;
      
      const title = video.title || '';
      const src = video.src || '';
      
      const parent = video.parentElement;
      const surroundingText = parent ? parent.textContent : '';
      
      if (this.containsTrumpKeywords(title) || 
          this.containsTrumpKeywords(src) || 
          this.containsTrumpKeywords(surroundingText)) {
        this.replaceWithBlockedMessage(video, 'video');
      }
    });
  }

  getThemeStyles(theme) {
    const themes = {
      classic: {
        background: 'linear-gradient(135deg, #ff6b6b, #ee5a52)',
        border: '#d63031',
        textColor: 'white'
      },
      elegant: {
        background: 'linear-gradient(135deg, #667eea, #764ba2)',
        border: '#5a67d8',
        textColor: 'white'
      },
      minimal: {
        background: 'linear-gradient(135deg, #bdc3c7, #2c3e50)',
        border: '#34495e',
        textColor: 'white'
      },
      neon: {
        background: 'linear-gradient(135deg, #ff0080, #7928ca)',
        border: '#9333ea',
        textColor: 'white'
      },
      nature: {
        background: 'linear-gradient(135deg, #11998e, #38ef7d)',
        border: '#059669',
        textColor: 'white'
      },
      sunset: {
        background: 'linear-gradient(135deg, #ff9a9e, #fad0c4)',
        border: '#f59e0b',
        textColor: '#333'
      }
    };
    
    return themes[theme] || themes.classic;
  }

  replaceWithBlockedMessage(element, contentType) {
    if (element.dataset.trumpBlocked) return;
    
    const blockedDiv = document.createElement('div');
    blockedDiv.className = 'trump-blocked-content';
    blockedDiv.dataset.trumpBlocked = 'true';
    blockedDiv.dataset.contentType = contentType;
    
    let width = 'auto';
    let height = 'auto';
    
    if (contentType === 'image' || contentType === 'video') {
      const computedStyle = window.getComputedStyle(element);
      width = element.offsetWidth || computedStyle.width || '300px';
      height = element.offsetHeight || computedStyle.height || '200px';
    }
    
    // Get theme styles
    const themeStyles = this.getThemeStyles(this.settings.theme);
    
    // Create blocked message structure securely
    const messageDiv = document.createElement('div');
    messageDiv.className = 'trump-blocked-message-pro';
    messageDiv.style.cssText = `
      background: ${themeStyles.background};
      border: 2px solid ${themeStyles.border};
      border-radius: 12px;
      padding: 20px;
      text-align: center;
      color: ${themeStyles.textColor};
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100px;
      max-width: 100%;
      position: relative;
      overflow: hidden;
      width: ${width};
      height: ${height};
      ${this.settings.animations ? 'animation: trumpBlockSlideIn 0.3s ease-out;' : ''}
    `;
    
    // Add shimmer effect for animations
    if (this.settings.animations) {
      const shimmer = document.createElement('div');
      shimmer.style.cssText = `
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        animation: trumpShimmer 2s infinite;
      `;
      messageDiv.appendChild(shimmer);
    }
    
    const iconDiv = document.createElement('div');
    iconDiv.className = 'trump-blocked-icon';
    iconDiv.style.cssText = `
      font-size: 2.5em;
      margin-bottom: 10px;
      filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
    `;
    iconDiv.textContent = '🚫';
    
    const textDiv = document.createElement('div');
    textDiv.className = 'trump-blocked-text';
    textDiv.style.cssText = `
      font-size: 1.2em;
      font-weight: 600;
      margin-bottom: 5px;
      text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
    `;
    textDiv.textContent = this.settings.customMessage;
    
    const typeDiv = document.createElement('div');
    typeDiv.className = 'trump-blocked-type';
    typeDiv.style.cssText = `
      font-size: 0.9em;
      opacity: 0.9;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      font-weight: 500;
    `;
    typeDiv.textContent = contentType;
    
    // Add count if enabled
    if (this.settings.showCount) {
      const countDiv = document.createElement('div');
      countDiv.className = 'trump-blocked-count';
      countDiv.style.cssText = `
        position: absolute;
        top: 8px;
        right: 8px;
        background: rgba(0, 0, 0, 0.5);
        color: white;
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 0.7em;
        font-weight: 600;
      `;
      countDiv.textContent = `#${this.blockedCount + 1}`;
      messageDiv.appendChild(countDiv);
    }
    
    messageDiv.appendChild(iconDiv);
    messageDiv.appendChild(textDiv);
    messageDiv.appendChild(typeDiv);
    blockedDiv.appendChild(messageDiv);
    
    // Store original element for potential restoration
    blockedDiv.originalElement = element.cloneNode(true);
    
    // Replace the element
    element.parentNode.replaceChild(blockedDiv, element);
    this.blockedCount++;
    
    // Play sound if enabled
    if (this.settings.sounds) {
      this.playBlockSound();
    }
    
    // Update statistics
    this.updateStatistics(contentType);
  }

  updateBlockedElements() {
    // Update existing blocked elements with new theme/message
    const blockedElements = document.querySelectorAll('.trump-blocked-content');
    blockedElements.forEach(blockedElement => {
      const messageDiv = blockedElement.querySelector('.trump-blocked-message-pro');
      const textDiv = blockedElement.querySelector('.trump-blocked-text');
      
      if (messageDiv && textDiv) {
        const themeStyles = this.getThemeStyles(this.settings.theme);
        messageDiv.style.background = themeStyles.background;
        messageDiv.style.borderColor = themeStyles.border;
        messageDiv.style.color = themeStyles.textColor;
        textDiv.textContent = this.settings.customMessage;
      }
    });
  }

  playBlockSound() {
    // Create a subtle click sound
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
    gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1);
    
    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + 0.1);
  }

  async updateStatistics(contentType) {
    try {
      const result = await chrome.storage.sync.get(['proSettings']);
      let settings = result.proSettings || this.settings;
      
      settings.totalBlocked = (settings.totalBlocked || 0) + 1;
      
      switch(contentType) {
        case 'text':
          settings.textBlocked = (settings.textBlocked || 0) + 1;
          break;
        case 'image':
          settings.imageBlocked = (settings.imageBlocked || 0) + 1;
          break;
        case 'video':
          settings.videoBlocked = (settings.videoBlocked || 0) + 1;
          break;
      }
      
      await chrome.storage.sync.set({ proSettings: settings });
    } catch (error) {
      console.log('Could not update statistics:', error);
    }
  }

  startObserver() {
    if (this.observer) return;
    
    this.observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        mutation.addedNodes.forEach((node) => {
          if (node.nodeType === Node.ELEMENT_NODE) {
            this.checkNewElement(node);
          }
        });
      });
    });
    
    this.observer.observe(document.body, {
      childList: true,
      subtree: true
    });
  }

  stopObserver() {
    if (this.observer) {
      this.observer.disconnect();
      this.observer = null;
    }
  }

  checkNewElement(element) {
    if (!this.isEnabled) return;
    
    // Check if the element itself should be blocked
    if (element.tagName === 'IMG') {
      const altText = element.alt || '';
      const title = element.title || '';
      const src = element.src || '';
      
      if (this.containsTrumpKeywords(altText) || 
          this.containsTrumpKeywords(title) || 
          this.containsTrumpKeywords(src)) {
        this.replaceWithBlockedMessage(element, 'image');
        return;
      }
    }
    
    if (element.tagName === 'VIDEO' || 
        (element.tagName === 'IFRAME' && 
         (element.src.includes('youtube') || element.src.includes('vimeo')))) {
      const title = element.title || '';
      const src = element.src || '';
      const surroundingText = element.parentElement ? element.parentElement.textContent : '';
      
      if (this.containsTrumpKeywords(title) || 
          this.containsTrumpKeywords(src) || 
          this.containsTrumpKeywords(surroundingText)) {
        this.replaceWithBlockedMessage(element, 'video');
        return;
      }
    }
    
    // Check text content
    if (this.containsTrumpKeywords(element.textContent)) {
      const textTags = ['P', 'DIV', 'SPAN', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'ARTICLE', 'SECTION', 'LI', 'TD', 'TH'];
      if (textTags.includes(element.tagName)) {
        this.replaceWithBlockedMessage(element, 'text');
        return;
      }
    }
    
    // Check child elements
    const images = element.querySelectorAll('img');
    const videos = element.querySelectorAll('video, iframe[src*="youtube"], iframe[src*="vimeo"]');
    const textElements = element.querySelectorAll('p, div, span, h1, h2, h3, h4, h5, h6, article, section, li, td, th');
    
    images.forEach(img => {
      if (!img.dataset.trumpBlocked) {
        const altText = img.alt || '';
        const title = img.title || '';
        const src = img.src || '';
        
        if (this.containsTrumpKeywords(altText) || 
            this.containsTrumpKeywords(title) || 
            this.containsTrumpKeywords(src)) {
          this.replaceWithBlockedMessage(img, 'image');
        }
      }
    });
    
    videos.forEach(video => {
      if (!video.dataset.trumpBlocked) {
        const title = video.title || '';
        const src = video.src || '';
        const surroundingText = video.parentElement ? video.parentElement.textContent : '';
        
        if (this.containsTrumpKeywords(title) || 
            this.containsTrumpKeywords(src) || 
            this.containsTrumpKeywords(surroundingText)) {
          this.replaceWithBlockedMessage(video, 'video');
        }
      }
    });
    
    textElements.forEach(textElement => {
      if (!textElement.dataset.trumpBlocked && this.containsTrumpKeywords(textElement.textContent)) {
        this.replaceWithBlockedMessage(textElement, 'text');
      }
    });
  }

  unblockContent() {
    const blockedElements = document.querySelectorAll('.trump-blocked-content');
    blockedElements.forEach(blockedElement => {
      if (blockedElement.originalElement) {
        blockedElement.parentNode.replaceChild(blockedElement.originalElement, blockedElement);
      }
    });
    this.blockedCount = 0;
  }

  getBlockedCount() {
    return this.blockedCount;
  }
}

// Add CSS animations if not already present
if (!document.getElementById('trump-blocker-pro-styles')) {
  const style = document.createElement('style');
  style.id = 'trump-blocker-pro-styles';
  style.textContent = `
    @keyframes trumpBlockSlideIn {
      from {
        opacity: 0;
        transform: scale(0.9);
      }
      to {
        opacity: 1;
        transform: scale(1);
      }
    }
    
    @keyframes trumpShimmer {
      0% { left: -100%; }
      100% { left: 100%; }
    }
  `;
  document.head.appendChild(style);
}

// Initialize the Trump blocker
const trumpBlockerPro = new TrumpBlockerPro();

// Make blocker available for popup communication
window.trumpBlockerPro = trumpBlockerPro;
// Block Trump Chrome Extension Content Script
/* global chrome */

class TrumpBlocker {
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
    
    this.init();
  }

  async init() {
    // Load settings from storage
    try {
      const result = await chrome.storage.sync.get(['isEnabled']);
      this.isEnabled = result.isEnabled !== false; // Default to true
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
      });
    }
  }

  containsTrumpKeywords(text) {
    if (!text) return false;
    const lowerText = text.toLowerCase();
    return this.keywords.some(keyword => lowerText.includes(keyword));
  }

  blockExistingContent() {
    // Block text content
    this.blockTextElements();
    
    // Block images
    this.blockImages();
    
    // Block videos
    this.blockVideos();
  }

  blockTextElements() {
    const textElements = document.querySelectorAll('p, div, span, h1, h2, h3, h4, h5, h6, article, section, li, td, th');
    
    textElements.forEach(element => {
      if (element.dataset.trumpBlocked) return;
      
      // Check if element contains Trump keywords
      if (this.containsTrumpKeywords(element.textContent)) {
        this.replaceWithBlockedMessage(element, 'text');
      }
    });
  }

  blockImages() {
    const images = document.querySelectorAll('img');
    
    images.forEach(img => {
      if (img.dataset.trumpBlocked) return;
      
      // Check alt text, title, src for Trump keywords
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
      
      // Check title, src, and surrounding text for Trump keywords
      const title = video.title || '';
      const src = video.src || '';
      
      // Check surrounding text context
      const parent = video.parentElement;
      const surroundingText = parent ? parent.textContent : '';
      
      if (this.containsTrumpKeywords(title) || 
          this.containsTrumpKeywords(src) || 
          this.containsTrumpKeywords(surroundingText)) {
        this.replaceWithBlockedMessage(video, 'video');
      }
    });
  }

  replaceWithBlockedMessage(element, contentType) {
    if (element.dataset.trumpBlocked) return;
    
    // Create blocked message container
    const blockedDiv = document.createElement('div');
    blockedDiv.className = 'trump-blocked-content';
    blockedDiv.dataset.trumpBlocked = 'true';
    blockedDiv.dataset.contentType = contentType;
    
    // Get original dimensions if it's an image or video
    let width = 'auto';
    let height = 'auto';
    
    if (contentType === 'image' || contentType === 'video') {
      const computedStyle = window.getComputedStyle(element);
      width = element.offsetWidth || computedStyle.width || '300px';
      height = element.offsetHeight || computedStyle.height || '200px';
    }
    
    // Create blocked message structure securely
    const messageDiv = document.createElement('div');
    messageDiv.className = 'trump-blocked-message';
    messageDiv.style.width = width;
    messageDiv.style.height = height;
    
    const iconDiv = document.createElement('div');
    iconDiv.className = 'trump-blocked-icon';
    iconDiv.textContent = '🚫';
    
    const textDiv = document.createElement('div');
    textDiv.className = 'trump-blocked-text';
    textDiv.textContent = 'Trump content blocked';
    
    const typeDiv = document.createElement('div');
    typeDiv.className = 'trump-blocked-type';
    typeDiv.textContent = contentType;
    
    messageDiv.appendChild(iconDiv);
    messageDiv.appendChild(textDiv);
    messageDiv.appendChild(typeDiv);
    blockedDiv.appendChild(messageDiv);
    
    // Store original element for potential restoration
    blockedDiv.originalElement = element.cloneNode(true);
    
    // Replace the element
    element.parentNode.replaceChild(blockedDiv, element);
    this.blockedCount++;
  }

  startObserver() {
    if (this.observer) return;
    
    this.observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        mutation.addedNodes.forEach((node) => {
          if (node.nodeType === Node.ELEMENT_NODE) {
            // Check the new element and its children
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
      // Check if it's a text element we should block
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

// Initialize the Trump blocker when the page loads
const trumpBlocker = new TrumpBlocker();

// Make blocker available for popup communication
window.trumpBlocker = trumpBlocker;
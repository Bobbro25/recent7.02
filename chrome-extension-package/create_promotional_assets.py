#!/usr/bin/env python3
"""
Create Chrome Web Store promotional images
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import requests
from io import BytesIO

def download_image(url, local_path):
    """Download image from URL"""
    try:
        response = requests.get(url)
        with open(local_path, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

def create_promotional_tile(output_path, width=440, height=280):
    """Create promotional tile image (440x280)"""
    
    # Create base image with gradient background
    img = Image.new('RGBA', (width, height), (214, 48, 49, 255))
    draw = ImageDraw.Draw(img)
    
    # Create gradient effect
    for i in range(height):
        alpha = int(255 * (i / height))
        color = (180, 40, 40, alpha)
        draw.line([(0, i), (width, i)], fill=color)
    
    # Add text
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
        subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
    
    # Main title
    title_text = "Block Trump"
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    draw.text((title_x, 80), title_text, fill=(255, 255, 255, 255), font=title_font)
    
    # Subtitle
    subtitle_text = "Content Blocker Extension"
    subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    draw.text((subtitle_x, 130), subtitle_text, fill=(255, 255, 255, 200), font=subtitle_font)
    
    # Add prohibition symbol
    symbol_size = 60
    symbol_x = (width - symbol_size) // 2
    symbol_y = 20
    
    # White circle
    draw.ellipse([symbol_x, symbol_y, symbol_x + symbol_size, symbol_y + symbol_size], 
                fill=(255, 255, 255, 255))
    
    # Red prohibition symbol
    draw.ellipse([symbol_x + 5, symbol_y + 5, symbol_x + symbol_size - 5, symbol_y + symbol_size - 5], 
                fill=None, outline=(214, 48, 49, 255), width=4)
    
    # Diagonal line
    draw.line([symbol_x + 15, symbol_y + 15, symbol_x + symbol_size - 15, symbol_y + symbol_size - 15], 
              fill=(214, 48, 49, 255), width=4)
    
    # Add feature points
    feature_font = subtitle_font
    features = ["✓ Blocks all Trump content", "✓ Works on all websites", "✓ Supports ACLU"]
    
    for i, feature in enumerate(features):
        draw.text((20, 180 + (i * 25)), feature, fill=(255, 255, 255, 220), font=feature_font)
    
    img.save(output_path, 'PNG')
    print(f"Created promotional tile: {output_path}")

def create_marquee_image(output_path, width=1400, height=560):
    """Create marquee promotional image (1400x560)"""
    
    # Create base image with gradient
    img = Image.new('RGBA', (width, height), (214, 48, 49, 255))
    draw = ImageDraw.Draw(img)
    
    # Create sophisticated gradient
    for i in range(height):
        ratio = i / height
        r = int(214 - (50 * ratio))
        g = int(48 - (10 * ratio))
        b = int(49 - (10 * ratio))
        draw.line([(0, i), (width, i)], fill=(r, g, b, 255))
    
    # Load fonts
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
        subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
        feature_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        feature_font = ImageFont.load_default()
    
    # Main title
    title_text = "Block Trump Extension"
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    draw.text((title_x, 120), title_text, fill=(255, 255, 255, 255), font=title_font)
    
    # Subtitle
    subtitle_text = "Clean, Trump-free browsing experience"
    subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    draw.text((subtitle_x, 220), subtitle_text, fill=(255, 255, 255, 200), font=subtitle_font)
    
    # Add large prohibition symbol
    symbol_size = 100
    symbol_x = (width - symbol_size) // 2
    symbol_y = 20
    
    # White circle
    draw.ellipse([symbol_x, symbol_y, symbol_x + symbol_size, symbol_y + symbol_size], 
                fill=(255, 255, 255, 255))
    
    # Red prohibition symbol
    draw.ellipse([symbol_x + 8, symbol_y + 8, symbol_x + symbol_size - 8, symbol_y + symbol_size - 8], 
                fill=None, outline=(214, 48, 49, 255), width=6)
    
    # Diagonal line
    draw.line([symbol_x + 20, symbol_y + 20, symbol_x + symbol_size - 20, symbol_y + symbol_size - 20], 
              fill=(214, 48, 49, 255), width=6)
    
    # Feature highlights in columns
    left_features = [
        "🚫 Automatic content blocking",
        "⚡ Real-time detection",
        "🌐 Works on all websites"
    ]
    
    right_features = [
        "🔒 Privacy-focused design",
        "📊 Live statistics",
        "💖 Supports ACLU"
    ]
    
    # Left column
    for i, feature in enumerate(left_features):
        draw.text((100, 320 + (i * 50)), feature, fill=(255, 255, 255, 220), font=feature_font)
    
    # Right column
    for i, feature in enumerate(right_features):
        draw.text((width//2 + 100, 320 + (i * 50)), feature, fill=(255, 255, 255, 220), font=feature_font)
    
    # Call-to-action
    cta_text = "Install now for a cleaner web experience!"
    cta_bbox = draw.textbbox((0, 0), cta_text, font=subtitle_font)
    cta_width = cta_bbox[2] - cta_bbox[0]
    cta_x = (width - cta_width) // 2
    draw.text((cta_x, 500), cta_text, fill=(255, 255, 255, 255), font=subtitle_font)
    
    img.save(output_path, 'PNG')
    print(f"Created marquee image: {output_path}")

def create_screenshot_mockup(output_path, width=1280, height=800):
    """Create screenshot showing extension functionality"""
    
    img = Image.new('RGBA', (width, height), (240, 240, 240, 255))
    draw = ImageDraw.Draw(img)
    
    # Create browser mockup
    browser_height = 600
    browser_y = (height - browser_height) // 2
    
    # Browser window
    draw.rounded_rectangle([50, browser_y, width-50, browser_y + browser_height], 
                          radius=10, fill=(255, 255, 255, 255), outline=(200, 200, 200, 255), width=2)
    
    # Browser address bar
    draw.rounded_rectangle([70, browser_y + 20, width-70, browser_y + 60], 
                          radius=5, fill=(248, 248, 248, 255), outline=(220, 220, 220, 255))
    
    # Mock content with blocked elements
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
    except:
        font = ImageFont.load_default()
        title_font = ImageFont.load_default()
    
    # Mock news article
    draw.text((90, browser_y + 80), "Latest News", fill=(50, 50, 50, 255), font=title_font)
    draw.text((90, browser_y + 110), "• Regular news article about politics", fill=(100, 100, 100, 255), font=font)
    draw.text((90, browser_y + 140), "• Another normal article", fill=(100, 100, 100, 255), font=font)
    
    # Blocked content area
    blocked_y = browser_y + 180
    draw.rounded_rectangle([90, blocked_y, width-90, blocked_y + 80], 
                          radius=8, fill=(214, 48, 49, 255))
    
    # Blocked message
    draw.text((110, blocked_y + 15), "🚫", fill=(255, 255, 255, 255), font=title_font)
    draw.text((140, blocked_y + 15), "Trump content blocked", fill=(255, 255, 255, 255), font=title_font)
    draw.text((140, blocked_y + 45), "TEXT", fill=(255, 255, 255, 200), font=font)
    
    # More content
    draw.text((90, blocked_y + 100), "• More regular news continues...", fill=(100, 100, 100, 255), font=font)
    
    # Extension popup mockup
    popup_x = width - 350
    popup_y = browser_y + 80
    
    # Popup background with gradient
    popup_width = 280
    popup_height = 200
    
    # Create popup gradient
    popup_img = Image.new('RGBA', (popup_width, popup_height), (102, 126, 234, 255))
    popup_draw = ImageDraw.Draw(popup_img)
    
    for i in range(popup_height):
        ratio = i / popup_height
        r = int(102 + (16 * ratio))
        g = int(126 - (8 * ratio))
        b = int(234 - (72 * ratio))
        popup_draw.line([(0, i), (popup_width, i)], fill=(r, g, b, 255))
    
    # Paste popup onto main image
    img.paste(popup_img, (popup_x, popup_y))
    
    # Popup content
    popup_draw = ImageDraw.Draw(img)
    
    # Title
    popup_draw.text((popup_x + 20, popup_y + 20), "🚫", fill=(255, 255, 255, 255), font=title_font)
    popup_draw.text((popup_x + 20, popup_y + 50), "Block Trump", fill=(255, 255, 255, 255), font=title_font)
    
    # Stats
    popup_draw.text((popup_x + 20, popup_y + 90), "3", fill=(255, 255, 255, 255), font=title_font)
    popup_draw.text((popup_x + 20, popup_y + 115), "Items Blocked", fill=(255, 255, 255, 200), font=font)
    
    # Toggle
    popup_draw.text((popup_x + 20, popup_y + 150), "Extension: ON", fill=(76, 175, 80, 255), font=font)
    
    img.save(output_path, 'PNG')
    print(f"Created screenshot mockup: {output_path}")

def main():
    """Create all promotional images"""
    
    # Create promotional directory
    promo_dir = 'promotional_assets'
    os.makedirs(promo_dir, exist_ok=True)
    
    print("Creating promotional assets...")
    
    # Create all promotional images
    create_promotional_tile(os.path.join(promo_dir, 'tile_440x280.png'))
    create_marquee_image(os.path.join(promo_dir, 'marquee_1400x560.png'))
    create_screenshot_mockup(os.path.join(promo_dir, 'screenshot_1280x800.png'))
    
    print("\nAll promotional assets created successfully!")
    print(f"Assets saved in: {promo_dir}/")

if __name__ == '__main__':
    main()
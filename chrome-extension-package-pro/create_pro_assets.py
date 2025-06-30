#!/usr/bin/env python3
"""
Create Pro Version promotional graphics with Enhanced UI emphasis
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_pro_promotional_tile(output_path, width=440, height=280):
    """Create promotional tile for Pro version (440x280)"""
    
    # Create base with premium gradient
    img = Image.new('RGBA', (width, height), (102, 126, 234, 255))
    draw = ImageDraw.Draw(img)
    
    # Create premium gradient effect
    for i in range(height):
        ratio = i / height
        r = int(102 + (50 * ratio))
        g = int(126 - (20 * ratio))
        b = int(234 - (50 * ratio))
        draw.line([(0, i), (width, i)], fill=(r, g, b, 255))
    
    # Add gold accents
    for i in range(0, width, 40):
        alpha = int(100 * (1 - abs(i - width/2) / (width/2)))
        draw.line([(i, 0), (i, height)], fill=(255, 215, 0, alpha))
    
    # Load fonts
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
        subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
        pro_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        pro_font = ImageFont.load_default()
    
    # Main title
    title_text = "Block Trump"
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width - 60) // 2
    draw.text((title_x, 70), title_text, fill=(255, 255, 255, 255), font=title_font)
    
    # PRO badge
    pro_text = "PRO"
    pro_bbox = draw.textbbox((0, 0), pro_text, font=pro_font)
    pro_width = pro_bbox[2] - pro_bbox[0]
    pro_x = title_x + title_width + 15
    
    # PRO badge background
    draw.rounded_rectangle([pro_x - 5, 70, pro_x + pro_width + 5, 90], 
                          radius=8, fill=(255, 215, 0, 255))
    draw.text((pro_x, 72), pro_text, fill=(51, 51, 51, 255), font=pro_font)
    
    # Subtitle
    subtitle_text = "Enhanced UI • Custom Themes • Advanced Analytics"
    subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    draw.text((subtitle_x, 110), subtitle_text, fill=(255, 255, 255, 200), font=subtitle_font)
    
    # Add prohibition symbol with premium effect
    symbol_size = 50
    symbol_x = (width - symbol_size) // 2
    symbol_y = 15
    
    # Gold outline
    draw.ellipse([symbol_x-2, symbol_y-2, symbol_x + symbol_size+2, symbol_y + symbol_size+2], 
                fill=(255, 215, 0, 255))
    
    # White circle
    draw.ellipse([symbol_x, symbol_y, symbol_x + symbol_size, symbol_y + symbol_size], 
                fill=(255, 255, 255, 255))
    
    # Red prohibition symbol
    draw.ellipse([symbol_x + 4, symbol_y + 4, symbol_x + symbol_size - 4, symbol_y + symbol_size - 4], 
                fill=None, outline=(214, 48, 49, 255), width=3)
    
    # Diagonal line
    draw.line([symbol_x + 12, symbol_y + 12, symbol_x + symbol_size - 12, symbol_y + symbol_size - 12], 
              fill=(214, 48, 49, 255), width=3)
    
    # Enhanced features list
    features = [
        "🎨 6 Custom Themes",
        "📊 Detailed Analytics", 
        "⚙️ Advanced Settings",
        "💬 Custom Messages"
    ]
    
    for i, feature in enumerate(features):
        x = 20 if i < 2 else width - 180
        y = 150 + ((i % 2) * 25)
        draw.text((x, y), feature, fill=(255, 255, 255, 220), font=subtitle_font)
    
    # Version indicator
    draw.text((width - 80, height - 25), "v1.0.1", fill=(255, 215, 0, 180), font=subtitle_font)
    
    img.save(output_path, 'PNG')
    print(f"Created Pro promotional tile: {output_path}")

def create_pro_marquee_image(output_path, width=1400, height=560):
    """Create Pro marquee promotional image (1400x560)"""
    
    # Create premium base
    img = Image.new('RGBA', (width, height), (102, 126, 234, 255))
    draw = ImageDraw.Draw(img)
    
    # Create sophisticated gradient with gold accents
    for i in range(height):
        ratio = i / height
        r = int(102 + (80 * ratio))
        g = int(126 - (30 * ratio))
        b = int(234 - (80 * ratio))
        draw.line([(0, i), (width, i)], fill=(r, g, b, 255))
    
    # Add premium texture
    for i in range(0, width, 60):
        for j in range(0, height, 60):
            alpha = int(50 * (1 - abs(i - width/2) / (width/2)))
            draw.ellipse([i, j, i+20, j+20], fill=(255, 215, 0, alpha))
    
    # Load fonts
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 64)
        subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
        feature_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        pro_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        feature_font = ImageFont.load_default()
        pro_font = ImageFont.load_default()
    
    # Main title with PRO
    title_text = "Block Trump Extension"
    title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width - 150) // 2
    draw.text((title_x, 100), title_text, fill=(255, 255, 255, 255), font=title_font)
    
    # PRO badge (large)
    pro_text = "PRO"
    pro_x = title_x + title_width + 30
    
    # PRO badge background with shadow
    draw.rounded_rectangle([pro_x - 10, 95, pro_x + 120, 145], 
                          radius=15, fill=(0, 0, 0, 100))
    draw.rounded_rectangle([pro_x - 8, 97, pro_x + 118, 147], 
                          radius=15, fill=(255, 215, 0, 255))
    draw.text((pro_x, 105), pro_text, fill=(51, 51, 51, 255), font=pro_font)
    
    # Subtitle
    subtitle_text = "Enhanced UI Features • Premium Content Blocking Experience"
    subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    draw.text((subtitle_x, 180), subtitle_text, fill=(255, 255, 255, 200), font=subtitle_font)
    
    # Large prohibition symbol with premium styling
    symbol_size = 80
    symbol_x = (width - symbol_size) // 2
    symbol_y = 20
    
    # Gold shadow
    draw.ellipse([symbol_x-3, symbol_y-3, symbol_x + symbol_size+3, symbol_y + symbol_size+3], 
                fill=(255, 215, 0, 150))
    
    # White circle
    draw.ellipse([symbol_x, symbol_y, symbol_x + symbol_size, symbol_y + symbol_size], 
                fill=(255, 255, 255, 255))
    
    # Red prohibition symbol
    draw.ellipse([symbol_x + 6, symbol_y + 6, symbol_x + symbol_size - 6, symbol_y + symbol_size - 6], 
                fill=None, outline=(214, 48, 49, 255), width=5)
    
    # Diagonal line
    draw.line([symbol_x + 16, symbol_y + 16, symbol_x + symbol_size - 16, symbol_y + symbol_size - 16], 
              fill=(214, 48, 49, 255), width=5)
    
    # Feature showcase in three columns
    left_features = [
        "🎨 6 Beautiful Themes",
        "💬 Custom Block Messages",
        "🔊 Sound Notifications"
    ]
    
    center_features = [
        "📊 Advanced Analytics",
        "📈 Detailed Statistics",
        "📁 Export Data"
    ]
    
    right_features = [
        "⚙️ Enhanced Settings",
        "🎛️ Animation Controls",
        "🔄 Real-time Updates"
    ]
    
    # Left column
    for i, feature in enumerate(left_features):
        draw.text((80, 280 + (i * 45)), feature, fill=(255, 255, 255, 220), font=feature_font)
    
    # Center column  
    for i, feature in enumerate(center_features):
        draw.text((width//2 - 100, 280 + (i * 45)), feature, fill=(255, 255, 255, 220), font=feature_font)
    
    # Right column
    for i, feature in enumerate(right_features):
        draw.text((width - 280, 280 + (i * 45)), feature, fill=(255, 255, 255, 220), font=feature_font)
    
    # Call-to-action
    cta_text = "Upgrade to Pro for Enhanced UI Experience!"
    cta_bbox = draw.textbbox((0, 0), cta_text, font=subtitle_font)
    cta_width = cta_bbox[2] - cta_bbox[0]
    cta_x = (width - cta_width) // 2
    
    # CTA background
    draw.rounded_rectangle([cta_x - 20, 470, cta_x + cta_width + 20, 510], 
                          radius=20, fill=(255, 215, 0, 200))
    draw.text((cta_x, 480), cta_text, fill=(51, 51, 51, 255), font=subtitle_font)
    
    img.save(output_path, 'PNG')
    print(f"Created Pro marquee image: {output_path}")

def create_pro_screenshot_mockup(output_path, width=1280, height=800):
    """Create Pro screenshot showing enhanced UI"""
    
    img = Image.new('RGBA', (width, height), (240, 240, 240, 255))
    draw = ImageDraw.Draw(img)
    
    # Browser mockup
    browser_height = 650
    browser_y = (height - browser_height) // 2
    
    # Browser window with shadow
    draw.rounded_rectangle([45, browser_y-5, width-45, browser_y + browser_height+5], 
                          radius=12, fill=(0, 0, 0, 50))
    draw.rounded_rectangle([50, browser_y, width-50, browser_y + browser_height], 
                          radius=10, fill=(255, 255, 255, 255), outline=(200, 200, 200, 255), width=2)
    
    # Browser address bar
    draw.rounded_rectangle([70, browser_y + 20, width-70, browser_y + 60], 
                          radius=5, fill=(248, 248, 248, 255), outline=(220, 220, 220, 255))
    
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
    except:
        font = ImageFont.load_default()
        title_font = ImageFont.load_default()
    
    # Mock content
    draw.text((90, browser_y + 80), "News Website - Latest Headlines", fill=(50, 50, 50, 255), font=title_font)
    
    # Pro version blocked content with theme
    blocked_y = browser_y + 120
    
    # Elegant theme example
    draw.rounded_rectangle([90, blocked_y, width-300, blocked_y + 80], 
                          radius=12, fill=(102, 126, 234, 255))
    draw.text((110, blocked_y + 15), "🚫", fill=(255, 255, 255, 255), font=title_font)
    draw.text((140, blocked_y + 15), "Content blocked with elegant theme", fill=(255, 255, 255, 255), font=title_font)
    draw.text((140, blocked_y + 40), "Custom message: 'This content has been filtered'", fill=(255, 255, 255, 200), font=font)
    draw.text((140, blocked_y + 55), "TEXT • Block #3", fill=(255, 255, 255, 150), font=font)
    
    # Enhanced Pro popup
    popup_x = width - 420
    popup_y = browser_y + 80
    popup_width = 380
    popup_height = 350
    
    # Popup shadow
    draw.rounded_rectangle([popup_x+5, popup_y+5, popup_x + popup_width+5, popup_y + popup_height+5], 
                          radius=15, fill=(0, 0, 0, 100))
    
    # Popup gradient background
    popup_img = Image.new('RGBA', (popup_width, popup_height), (102, 126, 234, 255))
    popup_draw = ImageDraw.Draw(popup_img)
    
    for i in range(popup_height):
        ratio = i / popup_height
        r = int(102 + (16 * ratio))
        g = int(126 - (8 * ratio))
        b = int(234 - (72 * ratio))
        popup_draw.line([(0, i), (popup_width, i)], fill=(r, g, b, 255))
    
    img.paste(popup_img, (popup_x, popup_y))
    
    # Popup content
    popup_draw = ImageDraw.Draw(img)
    
    # Header with PRO badge
    popup_draw.text((popup_x + 20, popup_y + 20), "🚫", fill=(255, 255, 255, 255), font=title_font)
    popup_draw.text((popup_x + 55, popup_y + 20), "Block Trump", fill=(255, 255, 255, 255), font=title_font)
    
    # PRO badge
    popup_draw.rounded_rectangle([popup_x + 180, popup_y + 20, popup_x + 220, popup_y + 40], 
                                radius=8, fill=(255, 215, 0, 255))
    popup_draw.text((popup_x + 188, popup_y + 23), "PRO", fill=(51, 51, 51, 255), font=font)
    
    # Tabs
    tabs = ["Main", "Themes", "Analytics", "Settings"]
    tab_width = 80
    for i, tab in enumerate(tabs):
        x = popup_x + 20 + (i * tab_width)
        y = popup_y + 60
        if i == 1:  # Themes tab active
            popup_draw.rounded_rectangle([x, y, x + tab_width - 5, y + 25], 
                                       radius=5, fill=(255, 255, 255, 50))
        popup_draw.text((x + 10, y + 5), tab, fill=(255, 255, 255, 200), font=font)
    
    # Theme selection showcase
    theme_y = popup_y + 100
    popup_draw.text((popup_x + 20, theme_y), "Choose Theme:", fill=(255, 255, 255, 255), font=title_font)
    
    # Theme previews
    themes = [
        ("Classic", (214, 48, 49)),
        ("Elegant", (102, 126, 234)),
        ("Minimal", (189, 195, 199))
    ]
    
    for i, (name, color) in enumerate(themes):
        x = popup_x + 30 + (i * 100)
        y = theme_y + 30
        popup_draw.rounded_rectangle([x, y, x + 80, y + 40], 
                                   radius=8, fill=color)
        popup_draw.text((x + 10, y + 15), name, fill=(255, 255, 255, 255), font=font)
    
    # Custom message input
    popup_draw.text((popup_x + 20, theme_y + 85), "Custom Message:", fill=(255, 255, 255, 255), font=font)
    popup_draw.rounded_rectangle([popup_x + 20, theme_y + 105, popup_x + 340, theme_y + 130], 
                                radius=5, fill=(255, 255, 255, 200))
    popup_draw.text((popup_x + 30, theme_y + 110), "Content filtered for your viewing preference", 
                   fill=(51, 51, 51, 255), font=font)
    
    # Statistics
    popup_draw.text((popup_x + 20, theme_y + 150), "Statistics:", fill=(255, 255, 255, 255), font=font)
    popup_draw.text((popup_x + 30, theme_y + 170), "• Text: 15 blocked", fill=(255, 255, 255, 200), font=font)
    popup_draw.text((popup_x + 30, theme_y + 185), "• Images: 8 blocked", fill=(255, 255, 255, 200), font=font)
    popup_draw.text((popup_x + 30, theme_y + 200), "• Videos: 3 blocked", fill=(255, 255, 255, 200), font=font)
    
    img.save(output_path, 'PNG')
    print(f"Created Pro screenshot mockup: {output_path}")

def main():
    """Create all Pro promotional images"""
    promo_dir = '/app/chrome-extension-package-pro/promotional_assets'
    
    print("Creating Pro version promotional assets...")
    
    create_pro_promotional_tile(os.path.join(promo_dir, 'pro_tile_440x280.png'))
    create_pro_marquee_image(os.path.join(promo_dir, 'pro_marquee_1400x560.png'))
    create_pro_screenshot_mockup(os.path.join(promo_dir, 'pro_screenshot_1280x800.png'))
    
    print("\nAll Pro promotional assets created successfully!")

if __name__ == '__main__':
    main()
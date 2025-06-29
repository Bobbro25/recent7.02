#!/usr/bin/env python3
"""
Create Chrome extension icons using PIL
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, output_path):
    """Create a professional icon with red background and stop symbol"""
    # Create image with red background
    img = Image.new('RGBA', (size, size), (214, 48, 49, 255))  # Red background
    draw = ImageDraw.Draw(img)
    
    # Add white circle background for the symbol
    margin = size // 8
    circle_size = size - (2 * margin)
    draw.ellipse([margin, margin, margin + circle_size, margin + circle_size], 
                fill=(255, 255, 255, 255), outline=None)
    
    # Add the prohibition symbol (circle with diagonal line)
    line_width = max(2, size // 16)
    # Outer circle
    draw.ellipse([margin + line_width, margin + line_width, 
                 margin + circle_size - line_width, margin + circle_size - line_width], 
                fill=None, outline=(214, 48, 49, 255), width=line_width)
    
    # Diagonal line
    diagonal_margin = margin + size // 4
    draw.line([diagonal_margin, diagonal_margin, 
              size - diagonal_margin, size - diagonal_margin], 
              fill=(214, 48, 49, 255), width=line_width)
    
    # Save the image
    img.save(output_path, 'PNG')
    print(f"Created icon: {output_path} ({size}x{size})")

def main():
    """Create all required icon sizes"""
    icons_dir = 'icons'
    
    # Create icons directory if it doesn't exist
    os.makedirs(icons_dir, exist_ok=True)
    
    # Create all required sizes
    sizes = [16, 48, 128]
    
    for size in sizes:
        output_path = os.path.join(icons_dir, f'icon{size}.png')
        create_icon(size, output_path)
    
    print("All icons created successfully!")

if __name__ == '__main__':
    main()
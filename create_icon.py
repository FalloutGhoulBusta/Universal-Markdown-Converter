#!/usr/bin/env python3
"""
Create a simple icon for the Universal Markdown Converter
This script creates a basic ICO file for the Windows executable
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

import os

def create_simple_icon():
    """Create a simple icon using PIL if available"""
    if not PIL_AVAILABLE:
        print("PIL (Pillow) not available. Skipping icon creation.")
        print("Install with: pip install Pillow")
        return False
    
    # Create a 64x64 image with a blue background
    size = 64
    img = Image.new('RGBA', (size, size), (52, 152, 219, 255))  # Blue background
    draw = ImageDraw.Draw(img)
    
    # Draw a simple "MD" text
    try:
        # Try to use a system font
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        try:
            font = ImageFont.truetype("calibri.ttf", 24)
        except:
            # Fallback to default font
            font = ImageFont.load_default()
    
    # Draw white "MD" text
    text = "MD"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
    
    # Add a small arrow or conversion symbol
    draw.polygon([(45, 15), (55, 20), (45, 25)], fill=(255, 255, 255, 255))  # Right arrow
    
    # Save as ICO
    img.save('icon.ico', format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    print("✓ Icon created: icon.ico")
    return True

def create_fallback_icon():
    """Create a minimal ICO file without PIL"""
    # This is a minimal 16x16 ICO file in hex format
    # It creates a simple blue square icon
    ico_data = bytes([
        # ICO header
        0x00, 0x00, 0x01, 0x00, 0x01, 0x00,
        # Image directory entry
        0x10, 0x10, 0x00, 0x00, 0x01, 0x00, 0x20, 0x00,
        0x68, 0x04, 0x00, 0x00, 0x16, 0x00, 0x00, 0x00,
        # Bitmap header
        0x28, 0x00, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00,
        0x20, 0x00, 0x00, 0x00, 0x01, 0x00, 0x20, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    ])
    
    # Add blue pixels (16x16 = 256 pixels, 4 bytes each)
    blue_pixel = bytes([0x3498db, 0xff])  # Blue color with alpha
    for _ in range(256):
        ico_data += blue_pixel
    
    # Add AND mask (all zeros for no transparency)
    ico_data += bytes(32)  # 16x16 bits = 32 bytes
    
    try:
        with open('icon.ico', 'wb') as f:
            f.write(ico_data)
        print("✓ Fallback icon created: icon.ico")
        return True
    except Exception as e:
        print(f"✗ Failed to create fallback icon: {e}")
        return False

if __name__ == "__main__":
    print("Creating icon for Universal Markdown Converter...")
    
    if not create_simple_icon():
        print("Trying fallback icon creation...")
        if not create_fallback_icon():
            print("Icon creation failed. The executable will use default icon.")
    
    print("Done!")

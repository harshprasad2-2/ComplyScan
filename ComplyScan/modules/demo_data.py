"""
ComplyScan Demo Data Generator
Creates synthetic demo package images for testing and demonstration.
"""

import cv2
import numpy as np
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from modules.config import DEMO_IMAGES_FOLDER

def create_demo_image(filename: str, content: str, image_size: tuple = (400, 600)) -> str:
    """
    Create a synthetic demo package label image.
    
    Args:
        filename (str): Output filename
        content (str): Text content for the label
        image_size (tuple): Image dimensions
    
    Returns:
        str: Path to created image
    """
    # Create image with white background
    img = Image.new('RGB', image_size, color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Try to use default font, fallback if needed
    try:
        font = ImageFont.truetype("arial.ttf", 16)
        small_font = ImageFont.truetype("arial.ttf", 12)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Add border
    border_color = (100, 100, 100)
    draw.rectangle([5, 5, image_size[0] - 5, image_size[1] - 5], outline=border_color, width=2)
    
    # Add content (word-wrapped)
    y_offset = 20
    x_offset = 20
    line_spacing = 25
    max_width = image_size[0] - 40
    
    for line in content.split('\n'):
        # Simple text wrapping
        if len(line) > 40:
            words = line.split()
            current_line = ""
            for word in words:
                if len(current_line) + len(word) + 1 < 40:
                    current_line += word + " "
                else:
                    if current_line:
                        draw.text((x_offset, y_offset), current_line, fill=(0, 0, 0), font=small_font)
                        y_offset += line_spacing
                    current_line = word + " "
            if current_line:
                draw.text((x_offset, y_offset), current_line, fill=(0, 0, 0), font=small_font)
                y_offset += line_spacing
        else:
            draw.text((x_offset, y_offset), line, fill=(0, 0, 0), font=font)
            y_offset += line_spacing
    
    # Save image
    DEMO_IMAGES_FOLDER.mkdir(parents=True, exist_ok=True)
    output_path = DEMO_IMAGES_FOLDER / filename
    img.save(str(output_path))
    
    return str(output_path)

def generate_all_demo_images():
    """Generate all demo images for testing."""
    
    # Demo A: Compliant package
    demo_a_content = """SUNRISE PREMIUM RICE
    
Basmati Rice

Net Qty: 5 kg

MRP Rs. 620
Inclusive of All Taxes

Packed: 08/2026

Packed by:
Sunrise Foods Pvt. Ltd.
12 Industrial Area
Kolkata, West Bengal - 700001

Consumer Care:
1800-123-4567
care@sunrise.example

Country of Origin: India"""
    
    create_demo_image("demo_a_compliant.png", demo_a_content)
    
    # Demo B: Missing consumer care
    demo_b_content = """VALLEY COOKING OIL
    
Sunflower Oil

Net Qty: 1 L

MRP Rs. 180
Inclusive of All Taxes

Packed: 07/2026

Packed by:
Valley Oils Ltd.
5 Commerce Zone
Mumbai - 400001"""
    
    create_demo_image("demo_b_missing_care.png", demo_b_content)
    
    # Demo C: MRP without tax declaration
    demo_c_content = """GOLDEN FLOUR
    
Wheat Flour

Net Qty: 2 kg

MRP Rs. 95

Packed: 06/2026

Packed by:
Golden Grains Factory
Plot 45, Industrial Estate
Delhi - 110012

Consumer Care:
011-4567-8901
support@golden.example

Country of Origin: India"""
    
    create_demo_image("demo_c_mrp_issue.png", demo_c_content)
    
    print(f"✅ Demo images created in {DEMO_IMAGES_FOLDER}")

if __name__ == "__main__":
    generate_all_demo_images()

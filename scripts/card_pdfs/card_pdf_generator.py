#!/usr/bin/env python3
"""
Unified Card PDF Generator for Murder Mystery Game
Generates printable card PDFs from JSON data or config files
Supports multiple card types: fact cards, character cards, rumor cards, etc.
"""

import json
import math
import textwrap
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def draw_ornate_border(draw, x, y, width, height, line_width=2, color='#8B7355'):
    """Draw ornate 1920s style border"""
    draw.rectangle([x, y, x + width, y + height], outline=color, width=line_width)
    inner_margin = line_width + 2
    draw.rectangle([x + inner_margin, y + inner_margin, 
                   x + width - inner_margin, y + height - inner_margin], 
                  outline=color, width=1)
    corner_size = 4
    corners = [(x + 8, y + 8), (x + width - 8, y + 8),
               (x + 8, y + height - 8), (x + width - 8, y + height - 8)]
    for cx, cy in corners:
        draw.ellipse([cx - corner_size, cy - corner_size, 
                     cx + corner_size, cy + corner_size], fill=color)

def load_font(size, fallback_sizes=[24, 18, 14]):
    """Load font with fallbacks"""
    for font_size in [size] + fallback_sizes:
        try:
            return ImageFont.truetype("/System/Library/Fonts/Georgia.ttf", font_size)
        except:
            try:
                return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
            except:
                pass
    return ImageFont.load_default()

def create_card_pdf(config_file, output_file):
    """
    Create PDF from config file
    
    Config format:
    {
        "card_size": {"width": 2.5, "height": 3.5},
        "page_size": {"width": 8.5, "height": 11.0},
        "margin": 0.5,
        "dpi": 72,
        "title": "FACT",
        "data_source": "data/rumors.json",
        "data_key": "rumors",
        "fields": {
            "text": "text",
            "possession": "possession",
            "title": "title",
            "description": "description"
        },
        "image_path_template": "fact_images/fact_{id:02d}.png",
        "qr_path_template": "qr_codes/character_{id}.png",
        "photo_path_template": "assets/{id}.png"
    }
    """
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    # Extract config
    card_w = config.get('card_size', {}).get('width', 2.5)
    card_h = config.get('card_size', {}).get('height', 3.5)
    page_w = config.get('page_size', {}).get('width', 8.5)
    page_h = config.get('page_size', {}).get('height', 11.0)
    margin = config.get('margin', 0.5)
    dpi = config.get('dpi', 72)
    title_text = config.get('title', 'CARD')
    
    # Convert to pixels
    page_w_px = int(page_w * dpi)
    page_h_px = int(page_h * dpi)
    margin_px = int(margin * dpi)
    card_w_px = int(card_w * dpi)
    card_h_px = int(card_h * dpi)
    
    # Calculate grid
    usable_w = page_w_px - (2 * margin_px)
    usable_h = page_h_px - (2 * margin_px)
    cols = int(usable_w / card_w_px)
    rows = int(usable_h / card_h_px)
    cards_per_page = cols * rows
    
    # Load data
    data_source = config.get('data_source')
    data_key = config.get('data_key', 'rumors')
    
    if data_source:
        with open(data_source, 'r') as f:
            data = json.load(f)
        items = data.get(data_key, [])
    else:
        items = config.get('items', [])
    
    if not items:
        print(f"❌ Error: No items found")
        return False
    
    # Create pages
    pages = []
    card_index = 0
    num_pages = math.ceil(len(items) / cards_per_page)
    
    title_font = load_font(32)
    text_font = load_font(14)
    small_font = load_font(10)
    
    for page_num in range(num_pages):
        page_img = Image.new('RGB', (page_w_px, page_h_px), color='white')
        draw = ImageDraw.Draw(page_img)
        
        for row in range(rows):
            if card_index >= len(items):
                break
            for col in range(cols):
                if card_index >= len(items):
                    break
                
                x = margin_px + (col * card_w_px)
                y = margin_px + (row * card_h_px)
                center_x = x + (card_w_px // 2)
                
                item = items[card_index]
                fields = config.get('fields', {})
                
                # Draw border
                draw_ornate_border(draw, x, y, card_w_px, card_h_px)
                
                # Draw title
                title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
                title_w = title_bbox[2] - title_bbox[0]
                draw.text((center_x - title_w//2, y + 10), title_text, 
                         fill='#1a1a1a', font=title_font)
                
                current_y = y + 50
                
                # Load and paste image if template provided
                img_template = config.get('image_path_template')
                if img_template and 'id' in item:
                    img_path = img_template.format(**item)
                    if Path(img_path).exists():
                        img = Image.open(img_path)
                        img.thumbnail((card_w_px - 20, int(card_h_px * 0.4)), Image.Resampling.LANCZOS)
                        img_x = center_x - (img.width // 2)
                        page_img.paste(img, (img_x, current_y))
                        current_y += img.height + 10
                
                # Load and paste photo if template provided
                photo_template = config.get('photo_path_template')
                if photo_template and 'id' in item:
                    photo_path = photo_template.format(**item)
                    if Path(photo_path).exists():
                        photo = Image.open(photo_path)
                        photo.thumbnail((card_w_px - 40, int(card_h_px * 0.25)), Image.Resampling.LANCZOS)
                        photo_x = center_x - (photo.width // 2)
                        page_img.paste(photo, (photo_x, current_y))
                        current_y += photo.height + 8
                
                # Load and paste QR code if template provided
                qr_template = config.get('qr_path_template')
                if qr_template and 'id' in item:
                    qr_path = qr_template.format(**item)
                    if Path(qr_path).exists():
                        qr = Image.open(qr_path)
                        qr_size = int(card_w_px * 0.6)
                        qr.thumbnail((qr_size, qr_size), Image.Resampling.LANCZOS)
                        qr_x = center_x - (qr.width // 2)
                        page_img.paste(qr, (qr_x, current_y))
                        current_y += qr.height + 8
                
                # Draw text content
                text_field = fields.get('text') or fields.get('description')
                if text_field and text_field in item:
                    text = item[text_field]
                    lines = textwrap.wrap(text, width=20)
                    max_lines = int((y + card_h_px - current_y - 30) / 16)
                    lines = lines[:max_lines]
                    
                    for line in lines:
                        line_bbox = draw.textbbox((0, 0), line, font=text_font)
                        line_w = line_bbox[2] - line_bbox[0]
                        draw.text((center_x - line_w//2, current_y), line,
                                 fill='#1a1a1a', font=text_font)
                        current_y += 16
                
                # Draw possession/attribution
                possession_field = fields.get('possession')
                if possession_field and possession_field in item:
                    pos_text = f"— {item[possession_field].upper()} —"
                    pos_bbox = draw.textbbox((0, 0), pos_text, font=small_font)
                    pos_w = pos_bbox[2] - pos_bbox[0]
                    draw.text((center_x - pos_w//2, y + card_h_px - 24),
                             pos_text, fill='#1a1a1a', font=small_font)
                
                card_index += 1
        
        pages.append(page_img)
    
    # Save PDF
    if pages:
        pages[0].save(output_file, save_all=True, append_images=pages[1:])
        print(f"✅ Generated: {output_file} ({len(pages)} pages, {len(items)} cards)")
        return True
    return False

def main():
    parser = argparse.ArgumentParser(description="Generate card PDF from config")
    parser.add_argument("--config", required=True, help="JSON config file")
    parser.add_argument("--output", required=True, help="Output PDF filename")
    args = parser.parse_args()
    
    create_card_pdf(args.config, args.output)

if __name__ == "__main__":
    main()

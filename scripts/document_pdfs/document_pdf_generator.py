#!/usr/bin/env python3
"""
Unified Document/Photo PDF Generator
Creates PDFs from images with optional QR code overlays
Supports full page, half page, and grid layouts
"""

import json
import argparse
import math
from pathlib import Path
from PIL import Image, ImageDraw

def create_document_pdf(config_file, output_file):
    """
    Create PDF from config file
    
    Config format:
    {
        "page_size": {"width": 8.5, "height": 11.0},
        "dpi": 72,
        "layout": "full" | "half" | "grid",
        "items": [
            {"image": "path/to/image.png", "qr": "path/to/qr.png", "title": "Title"}
        ],
        "image_dir": "assets/clue_images_documents",
        "qr_dir": "qr_codes",
        "qr_overlay": true,
        "qr_size_ratio": 0.33
    }
    """
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    page_w = config.get('page_size', {}).get('width', 8.5)
    page_h = config.get('page_size', {}).get('height', 11.0)
    dpi = config.get('dpi', 72)
    layout = config.get('layout', 'full')
    
    page_w_px = int(page_w * dpi)
    page_h_px = int(page_h * dpi)
    
    # Load items
    items = config.get('items', [])
    if not items:
        print("❌ Error: No items found")
        return False
    
    pages = []
    
    if layout == 'grid':
        # Grid layout (e.g., 2 photos per page)
        cols = config.get('grid_cols', 1)
        rows = config.get('grid_rows', 2)
        frame_w = config.get('frame_width', 4.0)
        frame_h = config.get('frame_height', 6.0)
        frame_w_px = int(frame_w * dpi)
        frame_h_px = int(frame_h * dpi)
        margin = int(0.5 * dpi)
        
        items_per_page = cols * rows
        num_pages = math.ceil(len(items) / items_per_page)
        
        for page_num in range(num_pages):
            page_img = Image.new('RGB', (page_w_px, page_h_px), color='white')
            
            for i in range(items_per_page):
                idx = page_num * items_per_page + i
                if idx >= len(items):
                    break
                
                item = items[idx]
                image_path = Path(item.get('image', ''))
                if not image_path.exists():
                    continue
                
                img = Image.open(image_path)
                img.thumbnail((frame_w_px, frame_h_px), Image.Resampling.LANCZOS)
                
                col = i % cols
                row = i // cols
                x = margin + col * (frame_w_px + margin)
                y = margin + row * (frame_h_px + margin)
                
                page_img.paste(img, (x, y))
            
            pages.append(page_img)
    
    elif layout == 'half':
        # Half page layout
        items_per_page = 2
        num_pages = math.ceil(len(items) / items_per_page)
        half_h = page_h_px // 2
        margin = int(0.5 * dpi)
        
        for page_num in range(num_pages):
            page_img = Image.new('RGB', (page_w_px, page_h_px), color='white')
            
            for i in range(items_per_page):
                idx = page_num * items_per_page + i
                if idx >= len(items):
                    break
                
                item = items[idx]
                image_path = Path(item.get('image', ''))
                if not image_path.exists():
                    continue
                
                img = Image.open(image_path)
                img.thumbnail((page_w_px - 2*margin, half_h - 2*margin), Image.Resampling.LANCZOS)
                
                y = i * half_h + margin
                x = (page_w_px - img.width) // 2
                
                # Add QR overlay if configured
                if config.get('qr_overlay') and 'qr' in item:
                    qr_path = Path(item['qr'])
                    if qr_path.exists():
                        qr = Image.open(qr_path)
                        qr_size = int(min(img.width, img.height) * config.get('qr_size_ratio', 0.33))
                        qr.thumbnail((qr_size, qr_size), Image.Resampling.LANCZOS)
                        qr_x = (img.width - qr.width) // 2
                        qr_y = (img.height - qr.height) // 2
                        img.paste(qr, (qr_x, qr_y))
                
                page_img.paste(img, (x, y))
            
            pages.append(page_img)
    
    else:  # full page
        for item in items:
            image_path = Path(item.get('image', ''))
            if not image_path.exists():
                continue
            
            img = Image.open(image_path)
            img.thumbnail((page_w_px, page_h_px), Image.Resampling.LANCZOS)
            
            page_img = Image.new('RGB', (page_w_px, page_h_px), color='white')
            x = (page_w_px - img.width) // 2
            y = (page_h_px - img.height) // 2
            
            # Add QR overlay if configured
            if config.get('qr_overlay') and 'qr' in item:
                qr_path = Path(item.get('qr', ''))
                if qr_path.exists():
                    qr = Image.open(qr_path)
                    qr_size = int(min(img.width, img.height) * config.get('qr_size_ratio', 0.33))
                    qr.thumbnail((qr_size, qr_size), Image.Resampling.LANCZOS)
                    qr_x = x + (img.width - qr.width) // 2
                    qr_y = y + (img.height - qr.height) // 2
                    img.paste(qr, (qr_x - x, qr_y - y))
            
            page_img.paste(img, (x, y))
            pages.append(page_img)
    
    # Save PDF
    if pages:
        pages[0].save(output_file, save_all=True, append_images=pages[1:])
        print(f"✅ Generated: {output_file} ({len(pages)} pages, {len(items)} items)")
        return True
    return False

def main():
    parser = argparse.ArgumentParser(description="Generate document/photo PDF from config")
    parser.add_argument("--config", required=True, help="JSON config file")
    parser.add_argument("--output", required=True, help="Output PDF filename")
    args = parser.parse_args()
    
    create_document_pdf(args.config, args.output)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Main QR Codes PDF Generator for Murder Mystery Game
Creates a single-page PDF with 4 key QR codes linking to main sections
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import qrcode

# Base URL for the game
BASE_URL = "https://elenafilatova.github.io/murder_mystery"

# Main sections: (id, title, description, url_path)
MAIN_SECTIONS = [
    ("characters", "CHARACTERS", "All playable character cards", "/character/characters.html"),
    ("clues", "CLUES", "All clue types and evidence", "/clue/clues.html"),
    ("rumors", "RUMORS & FACTS", "Rumors and knowledge cards", "/index.html"),  # or specific page
    ("book", "STORY BOOK", "The complete narrative", "/book/book_index.html"),
]

def generate_qr_code(url, size=300):
    """Generate a QR code image for the given URL"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    return img

def create_main_qr_pdf(output_file="main_qr_codes.pdf"):
    """
    Create a single-page PDF with 4 main QR codes in a 2x2 grid.
    """
    
    # Page settings
    page_width = 8.5
    page_height = 11.0
    margin = 0.75
    dpi = 150
    
    # Convert to pixels
    page_width_px = int(page_width * dpi)
    page_height_px = int(page_height * dpi)
    margin_px = int(margin * dpi)
    
    # QR code size: 2.5" x 2.5"
    qr_size_px = int(2.5 * dpi)
    
    print(f"\n{'='*60}")
    print(f"Main QR Codes PDF Generator")
    print(f"{'='*60}")
    print(f"Page size: {page_width}\" x {page_height}\"")
    print(f"QR code size: 2.5\" x 2.5\"")
    print(f"Base URL: {BASE_URL}")
    print(f"{'='*60}\n")
    
    # Create page
    page_img = Image.new('RGB', (page_width_px, page_height_px), color='white')
    draw = ImageDraw.Draw(page_img)
    
    # Load fonts
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Georgia.ttf", 36)
        header_font = ImageFont.truetype("/System/Library/Fonts/Georgia.ttf", 24)
        desc_font = ImageFont.truetype("/System/Library/Fonts/Georgia.ttf", 14)
    except:
        try:
            title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
            header_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
            desc_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
        except:
            title_font = ImageFont.load_default()
            header_font = ImageFont.load_default()
            desc_font = ImageFont.load_default()
    
    # Page title
    current_y = margin_px
    page_title = "THE LOST SOULS OF KENNEBEC AVENUE"
    title_bbox = draw.textbbox((0, 0), page_title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (page_width_px - title_width) // 2
    draw.text((title_x, current_y), page_title, fill='#1a1a1a', font=title_font)
    current_y += 50
    
    # Subtitle
    subtitle = "Quick Access QR Codes"
    sub_bbox = draw.textbbox((0, 0), subtitle, font=desc_font)
    sub_width = sub_bbox[2] - sub_bbox[0]
    sub_x = (page_width_px - sub_width) // 2
    draw.text((sub_x, current_y), subtitle, fill='#666666', font=desc_font)
    current_y += 30
    
    # Decorative line
    line_start = margin_px + 100
    line_end = page_width_px - margin_px - 100
    draw.line([(line_start, current_y), (line_end, current_y)], fill='#2a2a2a', width=2)
    draw.ellipse([(line_start - 4, current_y - 3), (line_start + 4, current_y + 3)], fill='#2a2a2a')
    draw.ellipse([(line_end - 4, current_y - 3), (line_end + 4, current_y + 3)], fill='#2a2a2a')
    current_y += 40
    
    # Calculate grid positions (2x2)
    usable_width = page_width_px - 2 * margin_px
    usable_height = page_height_px - current_y - margin_px
    
    cell_width = usable_width // 2
    cell_height = usable_height // 2
    
    # Draw 4 QR codes in 2x2 grid
    for idx, (section_id, title, description, url_path) in enumerate(MAIN_SECTIONS):
        row = idx // 2
        col = idx % 2
        
        cell_x = margin_px + col * cell_width
        cell_y = current_y + row * cell_height
        cell_center_x = cell_x + cell_width // 2
        
        # Generate QR code
        full_url = BASE_URL + url_path
        print(f"  Generating QR: {title} → {url_path}")
        qr_img = generate_qr_code(full_url, qr_size_px)
        
        # Center QR in cell
        qr_x = cell_center_x - qr_size_px // 2
        qr_y = cell_y + 50  # Space for title
        
        # Draw title above QR
        title_bbox = draw.textbbox((0, 0), title, font=header_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = cell_center_x - title_width // 2
        draw.text((title_x, cell_y + 15), title, fill='#1a1a1a', font=header_font)
        
        # Paste QR code
        page_img.paste(qr_img, (qr_x, qr_y))
        
        # Draw border around QR
        draw.rectangle(
            [qr_x - 3, qr_y - 3, qr_x + qr_size_px + 3, qr_y + qr_size_px + 3],
            outline='#1a1a1a',
            width=2
        )
        
        # Description below QR
        desc_bbox = draw.textbbox((0, 0), description, font=desc_font)
        desc_width = desc_bbox[2] - desc_bbox[0]
        desc_x = cell_center_x - desc_width // 2
        desc_y = qr_y + qr_size_px + 10
        draw.text((desc_x, desc_y), description, fill='#666666', font=desc_font)
    
    # Save as PDF
    page_img.save(output_file)
    
    print(f"\n{'='*60}")
    print(f"✅ PDF successfully created!")
    print(f"{'='*60}")
    print(f"📄 Filename: {output_file}")
    print(f"📦 QR codes: {len(MAIN_SECTIONS)}")
    print(f"{'='*60}\n")
    
    return True

def main():
    """Main entry point"""
    import argparse
    parser = argparse.ArgumentParser(
        description="Generate PDF with main QR codes"
    )
    parser.add_argument(
        "--output",
        default="main_qr_codes.pdf",
        help="Output PDF filename (default: main_qr_codes.pdf)"
    )
    
    args = parser.parse_args()
    
    success = create_main_qr_pdf(args.output)
    exit(0 if success else 1)

if __name__ == "__main__":
    main()


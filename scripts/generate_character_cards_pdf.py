#!/usr/bin/env python3
"""
Character Cards PDF Generator for Murder Mystery Game
Creates printable 3x4 inch character cards in a 1920s mystery style
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

# Character data: (id, title, description)
CHARACTERS = [
    ("professor", "The Professor", "Distracted genius obsessed with deadly plants. Your ancestor's secrets are tangled in the 1925 deaths."),
    ("explorer", "The Explorer", "Rugged adventurer hunting treasure. Something about this place feels strangely familiar."),
    ("baker", "The Baker", "Genuinely cheerful, warm, perpetually covered in flour. An orphan with a mysterious past."),
    ("heiress", "The Heiress", "Elegant, composed, harboring family secrets. The Montrose fortune may not be rightfully yours."),
    ("fiduciary", "The Fiduciary", "Meticulous, suspicious of everyone. The estate's finances hide dark secrets from 1925."),
    ("doctor", "The Doctor", "Compassionate healer with a dark family legacy. Your ancestor Dr. Crane signed three death certificates."),
    ("mortician", "The Mortician", "Calm, observant, comfortable with death. Your ancestor Silas knew the truth about the bodies."),
    ("clockmaker", "The Clockmaker", "Precise, methodical, obsessed with time. A mysterious pocket watch holds the key to everything."),
    ("dressmaker", "The Dressmaker", "Creative, romantic, haunted by the past. Your ancestor Elias loved Cordelia in secret."),
    ("artcollector", "The Art Collector", "Sophisticated, worldly, seeking family treasure. The Romano legacy is more than paintings."),
    ("influencer", "The Influencer", "Charismatic podcaster hunting the ultimate story. Three unsolved deaths make perfect content."),
    ("psychic", "The Psychic", "Mysterious, intuitive, connected to spirits. The dead have messages for the living."),
]

def create_character_cards_pdf(output_file="character_cards.pdf"):
    """
    Create a PDF with character cards arranged in a grid (1920s style).
    
    Layout:
    - Page size: 8.5" x 11" (letter)
    - Margins: 0.5" on all sides
    - Card size: 3" wide x 4" high
    - Grid: 2 columns x 2 rows = 4 cards per page
    - DPI: 150
    - Style: 1920s mystery matching fact cards
    """
    
    # Page settings (in inches)
    page_width = 8.5
    page_height = 11.0
    margin = 0.5
    card_width = 3.0
    card_height = 4.0
    dpi = 150
    
    # Convert to pixels
    page_width_px = int(page_width * dpi)
    page_height_px = int(page_height * dpi)
    margin_px = int(margin * dpi)
    card_width_px = int(card_width * dpi)
    card_height_px = int(card_height * dpi)
    
    # QR code size: 2" x 2"
    qr_size_px = int(2.0 * dpi)
    
    # Photo size: small, about 1" tall
    photo_height_px = int(1.0 * dpi)
    
    # Calculate grid
    cols_per_page = 2
    rows_per_page = 2
    cards_per_page = cols_per_page * rows_per_page
    
    # Calculate horizontal spacing to center cards
    total_cards_width = cols_per_page * card_width_px
    h_spacing = (page_width_px - 2 * margin_px - total_cards_width) // (cols_per_page + 1)
    
    # Calculate vertical spacing
    total_cards_height = rows_per_page * card_height_px
    v_spacing = (page_height_px - 2 * margin_px - total_cards_height) // (rows_per_page + 1)
    
    print(f"\n{'='*60}")
    print(f"Character Cards PDF Generator - 1920s Mystery Style")
    print(f"{'='*60}")
    print(f"Page size: {page_width}\" x {page_height}\"")
    print(f"Card size: {card_width}\" x {card_height}\"")
    print(f"QR code size: 2\" x 2\"")
    print(f"Grid layout: {cols_per_page} columns × {rows_per_page} rows")
    print(f"Cards per page: {cards_per_page}")
    print(f"{'='*60}\n")
    
    print(f"📊 Processing {len(CHARACTERS)} characters")
    print(f"📄 Generating PDF...\n")
    
    # Calculate number of pages
    num_pages = math.ceil(len(CHARACTERS) / cards_per_page)
    
    # Create pages
    pages = []
    card_index = 0
    
    for page_num in range(1, num_pages + 1):
        # Create new page image
        page_img = Image.new('RGB', (page_width_px, page_height_px), color='white')
        draw = ImageDraw.Draw(page_img)
        
        # Load fonts
        try:
            title_font = ImageFont.truetype("/System/Library/Fonts/Georgia.ttf", 24)
            text_font = ImageFont.truetype("/System/Library/Fonts/Georgia.ttf", 11)
        except:
            try:
                title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
                text_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 11)
            except:
                title_font = ImageFont.load_default()
                text_font = ImageFont.load_default()
        
        # Draw grid of cards
        for row in range(rows_per_page):
            if card_index >= len(CHARACTERS):
                break
                
            for col in range(cols_per_page):
                if card_index >= len(CHARACTERS):
                    break
                
                # Calculate position with spacing
                x = margin_px + h_spacing + col * (card_width_px + h_spacing)
                y = margin_px + v_spacing + row * (card_height_px + v_spacing)
                card_center_x = x + (card_width_px // 2)
                
                # Get character data
                char_id, char_title, char_desc = CHARACTERS[card_index]
                
                try:
                    # Draw ornate card border (1920s style)
                    # Outer border
                    draw.rectangle(
                        [x, y, x + card_width_px, y + card_height_px],
                        outline='#1a1a1a',
                        width=3
                    )
                    # Inner decorative border
                    draw.rectangle(
                        [x + 6, y + 6, x + card_width_px - 6, y + card_height_px - 6],
                        outline='#4a4a4a',
                        width=1
                    )
                    
                    # Decorative corner elements
                    corner_len = 12
                    # Top-left
                    draw.line([(x + 10, y + 8), (x + 10 + corner_len, y + 8)], fill='#1a1a1a', width=2)
                    draw.line([(x + 8, y + 10), (x + 8, y + 10 + corner_len)], fill='#1a1a1a', width=2)
                    # Top-right
                    draw.line([(x + card_width_px - 10 - corner_len, y + 8), (x + card_width_px - 10, y + 8)], fill='#1a1a1a', width=2)
                    draw.line([(x + card_width_px - 8, y + 10), (x + card_width_px - 8, y + 10 + corner_len)], fill='#1a1a1a', width=2)
                    # Bottom-left
                    draw.line([(x + 10, y + card_height_px - 8), (x + 10 + corner_len, y + card_height_px - 8)], fill='#1a1a1a', width=2)
                    draw.line([(x + 8, y + card_height_px - 10 - corner_len), (x + 8, y + card_height_px - 10)], fill='#1a1a1a', width=2)
                    # Bottom-right
                    draw.line([(x + card_width_px - 10 - corner_len, y + card_height_px - 8), (x + card_width_px - 10, y + card_height_px - 8)], fill='#1a1a1a', width=2)
                    draw.line([(x + card_width_px - 8, y + card_height_px - 10 - corner_len), (x + card_width_px - 8, y + card_height_px - 10)], fill='#1a1a1a', width=2)
                    
                    # Current Y position for layout
                    current_y = y + 15
                    
                    # Draw title centered at top
                    title_upper = char_title.upper()
                    title_bbox = draw.textbbox((0, 0), title_upper, font=title_font)
                    title_width = title_bbox[2] - title_bbox[0]
                    title_x = card_center_x - (title_width // 2)
                    draw.text(
                        (title_x, current_y),
                        title_upper,
                        fill='#1a1a1a',
                        font=title_font
                    )
                    current_y += title_bbox[3] - title_bbox[1] + 8
                    
                    # Decorative line under title with dots
                    line_y = current_y
                    line_start = x + 20
                    line_end = x + card_width_px - 20
                    draw.line([(line_start, line_y), (line_end, line_y)], fill='#2a2a2a', width=2)
                    # Decorative dots
                    draw.ellipse([(line_start - 4, line_y - 3), (line_start + 4, line_y + 3)], fill='#2a2a2a')
                    draw.ellipse([(line_end - 4, line_y - 3), (line_end + 4, line_y + 3)], fill='#2a2a2a')
                    current_y += 12
                    
                    # Load and paste character photo
                    photo_path = Path(f"assets/{char_id}.png")
                    if photo_path.exists():
                        photo = Image.open(photo_path)
                        # Calculate size maintaining aspect ratio
                        aspect = photo.width / photo.height
                        new_height = photo_height_px
                        new_width = int(new_height * aspect)
                        # Cap width to fit card
                        max_width = card_width_px - 40
                        if new_width > max_width:
                            new_width = max_width
                            new_height = int(new_width / aspect)
                        photo = photo.resize((new_width, new_height), Image.Resampling.LANCZOS)
                        photo_x = card_center_x - (new_width // 2)
                        page_img.paste(photo, (photo_x, current_y))
                        current_y += new_height + 8
                    else:
                        print(f"  ⚠️  Photo not found: {photo_path}")
                        current_y += photo_height_px + 8
                    
                    # Load and paste QR code
                    qr_path = Path(f"qr_codes/character_{char_id}.png")
                    if qr_path.exists():
                        qr = Image.open(qr_path)
                        qr = qr.resize((qr_size_px, qr_size_px), Image.Resampling.LANCZOS)
                        qr_x = card_center_x - (qr_size_px // 2)
                        page_img.paste(qr, (qr_x, current_y))
                        current_y += qr_size_px + 8
                    else:
                        print(f"  ⚠️  QR code not found: {qr_path}")
                        current_y += qr_size_px + 8
                    
                    # Decorative line before description
                    line_y = current_y - 4
                    draw.line([(x + 20, line_y), (x + card_width_px - 20, line_y)], fill='#2a2a2a', width=1)
                    
                    # Draw description text (word wrapped, centered)
                    import textwrap
                    desc_lines = textwrap.wrap(char_desc, width=28)
                    
                    # Calculate available space and fit lines
                    available_height = (y + card_height_px - 15) - current_y
                    line_height = 13
                    max_lines = int(available_height / line_height)
                    
                    if len(desc_lines) > max_lines:
                        desc_lines = desc_lines[:max_lines - 1]
                        if desc_lines:
                            desc_lines[-1] = desc_lines[-1].rstrip() + "..."
                    
                    for line in desc_lines:
                        line_bbox = draw.textbbox((0, 0), line, font=text_font)
                        line_width = line_bbox[2] - line_bbox[0]
                        line_x = card_center_x - (line_width // 2)
                        draw.text(
                            (line_x, current_y),
                            line,
                            fill='#1a1a1a',
                            font=text_font
                        )
                        current_y += line_height
                    
                    print(f"  ✓ {char_title}")
                    card_index += 1
                    
                except Exception as e:
                    print(f"  ⚠️  Error processing {char_id}: {e}")
                    card_index += 1
        
        pages.append(page_img)
    
    # Save as PDF
    if pages:
        pages[0].save(output_file, save_all=True, append_images=pages[1:])
        
        print(f"\n{'='*60}")
        print(f"✅ PDF successfully created!")
        print(f"{'='*60}")
        print(f"📄 Filename: {output_file}")
        print(f"📊 Total pages: {len(pages)}")
        print(f"📦 Total character cards: {len(CHARACTERS)}")
        print(f"✨ Style: 1920s Mystery")
        print(f"{'='*60}\n")
        
        return True
    else:
        print(f"❌ Error: No pages created")
        return False

def main():
    """Main entry point"""
    import argparse
    parser = argparse.ArgumentParser(
        description="Generate PDF with 1920s-styled character cards"
    )
    parser.add_argument(
        "--output",
        default="character_cards.pdf",
        help="Output PDF filename (default: character_cards.pdf)"
    )
    
    args = parser.parse_args()
    
    success = create_character_cards_pdf(args.output)
    exit(0 if success else 1)

if __name__ == "__main__":
    main()


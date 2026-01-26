#!/usr/bin/env python3
"""
Clue Examples PDF Generator for Murder Mystery Game
Creates a reference PDF with 2 example QR codes for each clue type
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

# Clue types with their examples (type_name, display_name, [(qr_file, label), ...])
CLUE_TYPES = [
    ("visions", "Visions (Ghost Manifestations)", [
        ("vision_alice.png", "Alice's Ghost"),
        ("vision_cordelia.png", "Cordelia's Ghost"),
    ]),
    ("botanicals", "Botanical Clues", [
        ("botanical_foxglove.png", "Foxglove (Poison)"),
        ("botanical_valerian.png", "Valerian"),
    ]),
    ("documents", "Documents (Legal & Financial)", [
        ("document_death_cert_cordelia.png", "Death Certificate - Cordelia"),
        ("document_prenup_agreement.png", "Pre-Nuptial Agreement"),
    ]),
    ("journals", "Journals (Personal Diaries)", [
        ("journal_cordelia_cordelia_diary.png", "Cordelia's Diary"),
        ("journal_thaddeus_thaddeus_diary.png", "Dr. Thaddeus's Diary"),
    ]),
    ("artifacts", "Artifacts (Physical Objects)", [
        ("artifact_pocket-watch.png", "The Pocket Watch"),
        ("artifact_cordelia-wedding-dress.png", "Wedding Dress"),
    ]),
]

def create_clue_examples_pdf(output_file="clue_examples.pdf"):
    """
    Create a PDF with example QR codes organized by clue type.
    
    Layout:
    - Page size: 8.5" x 11" (letter)
    - Each clue type gets a section with header
    - 2 QR codes per type side by side
    - 1920s mystery style
    """
    
    # Page settings
    page_width = 8.5
    page_height = 11.0
    margin = 0.5
    dpi = 150
    
    # Convert to pixels
    page_width_px = int(page_width * dpi)
    page_height_px = int(page_height * dpi)
    margin_px = int(margin * dpi)
    
    # QR code size: 2" x 2"
    qr_size_px = int(2.0 * dpi)
    
    # Section settings
    section_header_height = 60
    qr_row_height = qr_size_px + 80  # QR + label space
    section_height = section_header_height + qr_row_height + 30  # padding
    
    # Calculate sections per page
    usable_height = page_height_px - 2 * margin_px
    sections_per_page = int(usable_height / section_height)
    
    print(f"\n{'='*60}")
    print(f"Clue Examples PDF Generator - 1920s Mystery Style")
    print(f"{'='*60}")
    print(f"Page size: {page_width}\" x {page_height}\"")
    print(f"QR code size: 2\" x 2\"")
    print(f"Sections per page: {sections_per_page}")
    print(f"{'='*60}\n")
    
    print(f"📊 Processing {len(CLUE_TYPES)} clue types")
    print(f"📄 Generating PDF...\n")
    
    # Calculate number of pages
    num_pages = math.ceil(len(CLUE_TYPES) / sections_per_page)
    
    # Create pages
    pages = []
    section_index = 0
    
    for page_num in range(1, num_pages + 1):
        # Create new page image
        page_img = Image.new('RGB', (page_width_px, page_height_px), color='white')
        draw = ImageDraw.Draw(page_img)
        
        # Load fonts
        try:
            title_font = ImageFont.truetype("/System/Library/Fonts/Georgia.ttf", 28)
            header_font = ImageFont.truetype("/System/Library/Fonts/Georgia.ttf", 20)
            label_font = ImageFont.truetype("/System/Library/Fonts/Georgia.ttf", 14)
        except:
            try:
                title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
                header_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
                label_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
            except:
                title_font = ImageFont.load_default()
                header_font = ImageFont.load_default()
                label_font = ImageFont.load_default()
        
        # Page title (only on first page)
        current_y = margin_px
        if page_num == 1:
            page_title = "CLUE TYPE EXAMPLES"
            title_bbox = draw.textbbox((0, 0), page_title, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = (page_width_px - title_width) // 2
            draw.text((title_x, current_y), page_title, fill='#1a1a1a', font=title_font)
            current_y += 50
            
            # Decorative line
            line_start = margin_px + 50
            line_end = page_width_px - margin_px - 50
            draw.line([(line_start, current_y), (line_end, current_y)], fill='#2a2a2a', width=2)
            draw.ellipse([(line_start - 4, current_y - 3), (line_start + 4, current_y + 3)], fill='#2a2a2a')
            draw.ellipse([(line_end - 4, current_y - 3), (line_end + 4, current_y + 3)], fill='#2a2a2a')
            current_y += 30
        
        # Draw sections
        for _ in range(sections_per_page):
            if section_index >= len(CLUE_TYPES):
                break
            
            type_id, type_name, examples = CLUE_TYPES[section_index]
            
            # Section header background
            header_bg_y = current_y
            draw.rectangle(
                [margin_px, header_bg_y, page_width_px - margin_px, header_bg_y + section_header_height],
                fill='#2a2a2a'
            )
            
            # Section header text
            header_bbox = draw.textbbox((0, 0), type_name.upper(), font=header_font)
            header_width = header_bbox[2] - header_bbox[0]
            header_x = (page_width_px - header_width) // 2
            draw.text(
                (header_x, current_y + 18),
                type_name.upper(),
                fill='#d4a574',
                font=header_font
            )
            current_y += section_header_height + 15
            
            # Draw 2 QR codes side by side
            usable_width = page_width_px - 2 * margin_px
            qr_spacing = (usable_width - 2 * qr_size_px) // 3
            
            for i, (qr_file, label) in enumerate(examples[:2]):
                qr_x = margin_px + qr_spacing + i * (qr_size_px + qr_spacing)
                qr_y = current_y
                
                # Load and paste QR code
                qr_path = Path(f"qr_codes/{qr_file}")
                if qr_path.exists():
                    qr = Image.open(qr_path)
                    qr = qr.resize((qr_size_px, qr_size_px), Image.Resampling.LANCZOS)
                    page_img.paste(qr, (qr_x, qr_y))
                    
                    # Draw border around QR
                    draw.rectangle(
                        [qr_x - 2, qr_y - 2, qr_x + qr_size_px + 2, qr_y + qr_size_px + 2],
                        outline='#1a1a1a',
                        width=2
                    )
                else:
                    # Placeholder if QR not found
                    draw.rectangle(
                        [qr_x, qr_y, qr_x + qr_size_px, qr_y + qr_size_px],
                        outline='#1a1a1a',
                        fill='#f0f0f0',
                        width=2
                    )
                    draw.text((qr_x + 20, qr_y + qr_size_px//2), "QR Not Found", fill='#666666', font=label_font)
                    print(f"  ⚠️  QR not found: {qr_path}")
                
                # Label below QR
                label_bbox = draw.textbbox((0, 0), label, font=label_font)
                label_width = label_bbox[2] - label_bbox[0]
                label_x = qr_x + (qr_size_px - label_width) // 2
                label_y = qr_y + qr_size_px + 8
                draw.text((label_x, label_y), label, fill='#1a1a1a', font=label_font)
            
            print(f"  ✓ {type_name}")
            current_y += qr_row_height + 20
            section_index += 1
        
        pages.append(page_img)
    
    # Save as PDF
    if pages:
        pages[0].save(output_file, save_all=True, append_images=pages[1:])
        
        print(f"\n{'='*60}")
        print(f"✅ PDF successfully created!")
        print(f"{'='*60}")
        print(f"📄 Filename: {output_file}")
        print(f"📊 Total pages: {len(pages)}")
        print(f"📦 Total clue types: {len(CLUE_TYPES)}")
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
        description="Generate PDF with clue type examples"
    )
    parser.add_argument(
        "--output",
        default="clue_examples.pdf",
        help="Output PDF filename (default: clue_examples.pdf)"
    )
    
    args = parser.parse_args()
    
    success = create_clue_examples_pdf(args.output)
    exit(0 if success else 1)

if __name__ == "__main__":
    main()


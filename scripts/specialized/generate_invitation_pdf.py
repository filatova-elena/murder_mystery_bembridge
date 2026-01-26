#!/usr/bin/env python3
"""
Murder Mystery Invitation PDF Generator
Creates an elegant 1920s-styled invitation
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def create_invitation_pdf(output_file="invitation.pdf"):
    """
    Create an elegant 1920s-styled invitation PDF.
    """
    
    # Page settings (5x7 inches - standard invitation size)
    page_width = 5.0
    page_height = 7.0
    dpi = 300  # High quality for printing
    
    # Convert to pixels
    page_width_px = int(page_width * dpi)
    page_height_px = int(page_height * dpi)
    
    print(f"\n{'='*60}")
    print(f"Invitation PDF Generator - 1920s Style")
    print(f"{'='*60}")
    print(f"Size: {page_width}\" x {page_height}\"")
    print(f"DPI: {dpi}")
    print(f"{'='*60}\n")
    
    # Create page with cream/ivory background
    page_img = Image.new('RGB', (page_width_px, page_height_px), color='#f5f0e6')
    draw = ImageDraw.Draw(page_img)
    
    # Load fonts - Snell Roundhand for headers, Georgia for body
    try:
        # Snell Roundhand for elegant script headers
        script_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/SnellRoundhand.ttc", 42)
        script_large = ImageFont.truetype("/System/Library/Fonts/Supplemental/SnellRoundhand.ttc", 52)
        signature_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/SnellRoundhand.ttc", 48)
        # Georgia for readable body text
        body_font = ImageFont.truetype("/System/Library/Fonts/Georgia.ttf", 30)
        italic_font = ImageFont.truetype("/System/Library/Fonts/Georgia.ttf", 30)
        small_font = ImageFont.truetype("/System/Library/Fonts/Georgia.ttf", 26)
        title_font = script_large
    except:
        try:
            script_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/SnellRoundhand.ttc", 42)
            script_large = ImageFont.truetype("/System/Library/Fonts/Supplemental/SnellRoundhand.ttc", 52)
            signature_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/SnellRoundhand.ttc", 48)
            body_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", 30)
            italic_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", 30)
            small_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", 26)
            title_font = script_large
        except:
            title_font = ImageFont.load_default()
            body_font = ImageFont.load_default()
            italic_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
            signature_font = ImageFont.load_default()
            script_font = ImageFont.load_default()
            script_large = ImageFont.load_default()
    
    # Colors
    dark_brown = '#2a1810'
    gold = '#8b7355'
    
    # Margins
    margin = 80
    center_x = page_width_px // 2
    
    # Draw decorative border
    border_margin = 40
    # Outer border
    draw.rectangle(
        [border_margin, border_margin, 
         page_width_px - border_margin, page_height_px - border_margin],
        outline=gold, width=3
    )
    # Inner border
    draw.rectangle(
        [border_margin + 15, border_margin + 15, 
         page_width_px - border_margin - 15, page_height_px - border_margin - 15],
        outline=gold, width=1
    )
    
    # Decorative corners
    corner_size = 30
    corners = [
        (border_margin + 8, border_margin + 8),  # top-left
        (page_width_px - border_margin - 8, border_margin + 8),  # top-right
        (border_margin + 8, page_height_px - border_margin - 8),  # bottom-left
        (page_width_px - border_margin - 8, page_height_px - border_margin - 8),  # bottom-right
    ]
    for cx, cy in corners:
        draw.line([(cx - corner_size//2, cy), (cx + corner_size//2, cy)], fill=gold, width=2)
        draw.line([(cx, cy - corner_size//2), (cx, cy + corner_size//2)], fill=gold, width=2)
    
    current_y = margin + 30
    
    # Large header font for "You Are Invited"
    try:
        header_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/SnellRoundhand.ttc", 72)
    except:
        header_font = script_large
    
    # "You Are Invited" - big elegant header
    text = "You Are Invited"
    bbox = draw.textbbox((0, 0), text, font=header_font)
    text_width = bbox[2] - bbox[0]
    draw.text((center_x - text_width // 2, current_y), text, fill=dark_brown, font=header_font)
    current_y += 100
    
    # Decorative flourish under header
    flourish_width = 150
    draw.line([(center_x - flourish_width, current_y), (center_x + flourish_width, current_y)], 
              fill=gold, width=2)
    draw.ellipse([(center_x - 6, current_y - 6), (center_x + 6, current_y + 6)], fill=gold)
    current_y += 50
    
    # "Dear friend," in elegant script
    text = "Dear friend,"
    bbox = draw.textbbox((0, 0), text, font=script_large)
    text_width = bbox[2] - bbox[0]
    draw.text((center_x - text_width // 2, current_y), text, fill=dark_brown, font=script_large)
    current_y += 90
    
    # Main invitation text - shorter version
    lines = [
        ("You are hereby cordially invited to", body_font),
        ("an evening of extraordinary purpose.", body_font),
        ("", None),
        ("For one hundred years, three souls have", body_font),
        ("been trapped at the Mansion on Park Circle", body_font),
        ("haunting its halls.", body_font),
        ("", None),
        ("On February 26th, I am assembling a group", body_font),
        ("of investigators who I believe possess the", body_font),
        ("ability to finally uncover the truth. I ask that", body_font),
        ("you come with an open mind and", body_font),
        ("a willingness to listen.", body_font),
        ("", None),
        ("The dead have waited long enough.", script_font),
        ("", None),
        ("I do hope you will join us.", script_font),
    ]
    
    line_spacing = 38
    for text, font in lines:
        if text == "":
            current_y += 20
            continue
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        x = center_x - text_width // 2
        draw.text((x, current_y), text, fill=dark_brown, font=font)
        current_y += line_spacing
    
    current_y += 20
    
    # Signature
    text = "— G. G."
    bbox = draw.textbbox((0, 0), text, font=signature_font)
    text_width = bbox[2] - bbox[0]
    draw.text((center_x - text_width // 2, current_y), text, fill=dark_brown, font=signature_font)
    current_y += 80
    
    # Decorative line
    line_width = 200
    draw.line([(center_x - line_width//2, current_y), (center_x + line_width//2, current_y)], 
              fill=gold, width=2)
    draw.ellipse([(center_x - 5, current_y - 5), (center_x + 5, current_y + 5)], fill=gold)
    current_y += 40
    
    # Venue details
    venue_lines = [
        ("Bembridge House", script_font),
        ("", None),
        ("953 Park Circle", small_font),
        ("Long Beach, California", small_font),
        ("", None),
        ("5 o'clock in the evening", body_font),
        ("Early 20th century attire welcomed.", small_font),
        ("Refreshments will be served.", small_font),
    ]
    
    for text, font in venue_lines:
        if text == "":
            current_y += 15
            continue
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        x = center_x - text_width // 2
        draw.text((x, current_y), text, fill=dark_brown, font=font)
        current_y += 36
    
    # Save as PDF
    page_img.save(output_file)
    
    print(f"✅ Invitation PDF created!")
    print(f"📄 Filename: {output_file}")
    print(f"{'='*60}\n")
    
    return True

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate invitation PDF")
    parser.add_argument("--output", default="invitation.pdf", help="Output filename")
    args = parser.parse_args()
    
    success = create_invitation_pdf(args.output)
    exit(0 if success else 1)

if __name__ == "__main__":
    main()


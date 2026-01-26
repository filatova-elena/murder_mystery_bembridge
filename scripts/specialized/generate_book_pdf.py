#!/usr/bin/env python3
"""
Generate a complete, beautifully formatted 1920s-style book PDF of the murder mystery.
"""

import json
import os
from pathlib import Path
from datetime import datetime
import re

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
    from reportlab.lib.colors import HexColor
    from reportlab.pdfgen import canvas
    from reportlab.lib import colors
except ImportError:
    print("Error: Required packages not installed.")
    print("Run: pip install reportlab")
    exit(1)

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, 'data', 'book')
OUTPUT_DIR = os.path.join(PROJECT_DIR, 'to_print')

os.makedirs(OUTPUT_DIR, exist_ok=True)

# All chapters in order - titles derived from JSON filenames
CHAPTERS = [
    ('00_prologue.json', 'Prologue'),
    ('01_cordelia_lover.json', 'Cordelia\'s Lover'),
    ('02_the_alchemist.json', 'The Alchemist'),
    ('03_doctors_orders.json', 'Doctor\'s Orders'),
    ('04_cordelia_concern.json', 'Cordelia\'s Concern'),
    ('05_mortician_discretion.json', 'Mortician\'s Discretion'),
    ('06_investigation_begins.json', 'Investigation Begins'),
    ('07_thomas_whitmore.json', 'Thomas Whitmore'),
    ('08_elixir_eternal_love.json', 'Elixir of Eternal Love'),
    ('09_dressmaker_devotion.json', 'Dressmaker\'s Devotion'),
    ('10_bakers_inheritance.json', 'Baker\'s Inheritance'),
    ('11_cordelias_last_words.json', 'Cordelia\'s Last Words'),
    ('12_romano_treasure.json', 'Romano Treasure'),
    ('13_secrets_unravelled.json', 'Secrets Unravelled'),
    ('14_silent_witness.json', 'Silent Witness'),
]

def extract_images_from_content(content):
    """Extract image references from content.
    Returns list of image data: (src, width, height, alt)"""
    images = []
    img_pattern = r'<img\s+src="([^"]+)"\s+width="(\d+)"\s+height="(\d+)"\s+alt="([^"]*)"'
    matches = re.finditer(img_pattern, content)
    for match in matches:
        src, width, height, alt = match.groups()
        images.append({
            'src': src,
            'width': int(width),
            'height': int(height),
            'alt': alt,
            'pos': match.start()
        })
    return images

def clean_html_tags(text, preserve_structure=False):
    """Remove HTML tags, return clean text with structure preserved."""
    # Replace img tags with a placeholder if preserving structure
    if preserve_structure:
        text = re.sub(r'<img[^>]*>', '[IMAGE]', text)
    else:
        text = re.sub(r'<img[^>]*>', '', text)
    # Remove br tags and replace with newlines
    text = re.sub(r'<br\s*/?>', '\n', text)
    # Remove all formatting tags
    text = re.sub(r'</?i>', '', text)
    text = re.sub(r'</?strong>', '', text)
    text = re.sub(r'</?u>', '', text)
    # Remove other HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    return text.strip()

def extract_italic_regions(content):
    """Extract paragraphs that should be italic based on <i> tags.
    Returns a dict mapping paragraph text to whether it should be italic."""
    # Split by double newline to get paragraphs
    paragraphs = content.split('\n\n')
    
    paragraph_styles = {}
    for para in paragraphs:
        cleaned = para.strip()
        if cleaned:
            # Check if this paragraph is marked with <i> or <strong><i>
            has_italic = '<i>' in para or '<strong><i>' in para
            # Remove the tags but preserve image structure
            clean_para = clean_html_tags(para, preserve_structure=True)
            if clean_para:
                paragraph_styles[clean_para] = has_italic
    
    return paragraph_styles

def format_entry(entry):
    """Format a single entry for the PDF."""
    date = entry.get('date', '')
    location = entry.get('location', '')
    title = entry.get('title', '')
    content = entry.get('content', '')
    
    # Check if this entire entry IS a diary/notebook entry (by location)
    diary_locations = [
        "Diary", "diary", "Notebook", "notebook", "Notes", "notes",
        "'s Diary", "'s Notebook", "'s Notes"
    ]
    is_diary_entry = any(diary_term in location for diary_term in diary_locations)
    
    # Clean HTML from content but preserve image placeholders
    clean_content = clean_html_tags(content, preserve_structure=True)
    
    # Format the header
    parts = []
    if date:
        parts.append(date)
    if location:
        parts.append(location)
    
    header = ' • '.join(parts)
    
    return header, title, clean_content, is_diary_entry

def generate_book_pdf():
    """Generate a complete, book-style PDF."""
    
    # Create PDF with book-like margins
    pdf_path = os.path.join(OUTPUT_DIR, 'Murder_Mystery_Book.pdf')
    
    # Book-like page setup with larger margins
    left_margin = 1.0 * inch
    right_margin = 1.0 * inch
    top_margin = 0.75 * inch
    bottom_margin = 0.75 * inch
    
    page_width = letter[0]
    page_height = letter[1]
    
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=left_margin,
        rightMargin=right_margin,
        topMargin=top_margin,
        bottomMargin=bottom_margin
    )
    
    story = []
    
    # Define styles for a beautiful 1920s-themed book
    styles = getSampleStyleSheet()
    
    # 1920s color palette
    dark_brown = HexColor('#3d2817')
    gold = HexColor('#d4af37')
    cream = HexColor('#f5f1e8')
    rust = HexColor('#8b6f47')
    
    # Title page style - elegant serif
    title_style = ParagraphStyle(
        'BookTitle',
        parent=styles['Heading1'],
        fontSize=48,
        textColor=gold,
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Times-Bold',
        leading=56,
        letterSpacing=2
    )
    
    # Decorative ornament style
    ornament_style = ParagraphStyle(
        'Ornament',
        parent=styles['Normal'],
        fontSize=24,
        textColor=gold,
        spaceAfter=16,
        alignment=TA_CENTER,
        fontName='Times-Roman'
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=18,
        textColor=rust,
        spaceAfter=48,
        alignment=TA_CENTER,
        fontName='Times-Italic',
        leading=24,
        letterSpacing=1
    )
    
    chapter_title_style = ParagraphStyle(
        'ChapterTitle',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=gold,
        spaceAfter=20,
        spaceBefore=10,
        fontName='Times-Bold',
        leading=28,
        letterSpacing=1,
        alignment=TA_CENTER
    )
    
    chapter_num_style = ParagraphStyle(
        'ChapterNum',
        parent=styles['Normal'],
        fontSize=11,
        textColor=rust,
        spaceAfter=4,
        fontName='Times-Italic',
        leading=12,
        alignment=TA_CENTER
    )
    
    entry_header_style = ParagraphStyle(
        'EntryHeader',
        parent=styles['Normal'],
        fontSize=9,
        textColor=rust,
        spaceAfter=6,
        fontName='Times-Italic',
        leading=11,
        textTransform='uppercase'
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=11,
        textColor=dark_brown,
        spaceAfter=12,
        leading=16,
        alignment=TA_JUSTIFY,
        allowOrphans=True,
        allowWidows=True,
        fontName='Times-Roman'
    )
    
    # Italic style for diary entries
    italic_style = ParagraphStyle(
        'Italic',
        parent=styles['Normal'],
        fontSize=11,
        textColor=dark_brown,
        spaceAfter=12,
        leading=16,
        alignment=TA_JUSTIFY,
        allowOrphans=True,
        allowWidows=True,
        fontName='Times-Italic'
    )
    
    # ===== TITLE PAGE =====
    story.append(Spacer(1, 2.5 * inch))
    
    # Decorative top ornament
    story.append(Paragraph("❦ ❦ ❦", ornament_style))
    story.append(Spacer(1, 0.3 * inch))
    
    # Main title
    story.append(Paragraph("The Lost Souls of Kennebec Avenue", title_style))
    
    story.append(Spacer(1, 0.2 * inch))
    
    # Subtitle
    story.append(Paragraph("A Murder Mystery", subtitle_style))
    
    story.append(Spacer(1, 1.2 * inch))
    
    # Tagline
    story.append(Paragraph(
        "A tale of murder, madness, and the ghosts that linger<br/>in the shadows of Long Beach",
        ParagraphStyle(
            'Tagline',
            parent=styles['Normal'],
            fontSize=13,
            textColor=rust,
            alignment=TA_CENTER,
            fontName='Times-Italic',
            leading=18
        )
    ))
    
    story.append(Spacer(1, 1.8 * inch))
    
    # Bottom decorative element
    story.append(Paragraph("❦ ❦ ❦", ornament_style))
    
    story.append(Spacer(1, 0.5 * inch))
    
    # Date at bottom
    story.append(Paragraph(
        f"A Mystery Unveiled<br/>{datetime.now().strftime('%B %Y')}",
        ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=11,
            textColor=gold,
            alignment=TA_CENTER,
            fontName='Times-Italic',
            leading=14
        )
    ))
    
    story.append(PageBreak())
    
    # ===== TABLE OF CONTENTS =====
    story.append(Paragraph("Table of Contents", chapter_title_style))
    story.append(Spacer(1, 0.2 * inch))
    
    for i, (chapter_file, chapter_name) in enumerate(CHAPTERS, 1):
        toc_entry = Paragraph(
            f"{i}. {chapter_name}",
            ParagraphStyle(
                'TOC',
                parent=styles['Normal'],
                fontSize=10,
                textColor=HexColor('#34495e'),
                spaceAfter=6,
                leftIndent=0.2 * inch,
                leading=12
            )
        )
        story.append(toc_entry)
    
    story.append(PageBreak())
    
    # ===== CHAPTERS =====
    for chapter_num, (chapter_file, chapter_name) in enumerate(CHAPTERS, 1):
        chapter_path = os.path.join(DATA_DIR, chapter_file)
        
        if not os.path.exists(chapter_path):
            print(f"⚠️  Warning: {chapter_file} not found, skipping...")
            continue
        
        print(f"📖 Processing Chapter {chapter_num}: {chapter_name}...")
        
        try:
            with open(chapter_path, 'r', encoding='utf-8') as f:
                chapter_data = json.load(f)
        except Exception as e:
            print(f"❌ Error reading {chapter_file}: {e}")
            continue
        
        # Add decorative line before chapter
        story.append(Spacer(1, 0.1 * inch))
        story.append(Paragraph("✦", ornament_style))
        story.append(Spacer(1, 0.1 * inch))
        
        # Add chapter number and title
        story.append(Paragraph(f"CHAPTER {chapter_num}", chapter_num_style))
        story.append(Paragraph(chapter_name, chapter_title_style))
        story.append(Spacer(1, 0.2 * inch))
        
        # Process entries
        entries = chapter_data.get('entries', [])
        for entry_idx, entry in enumerate(entries):
            header, title, content, is_diary_entry = format_entry(entry)
            
            # Add entry header (date/location) - only date and location, no title
            if header:
                story.append(Paragraph(header, entry_header_style))
                story.append(Spacer(1, 0.08 * inch))
            
            # Add content - break into paragraphs and handle italic formatting + images
            if content:
                # First, extract all images from the original content
                images = extract_images_from_content(entry.get('content', ''))
                
                # Process paragraphs
                paragraph_styles = extract_italic_regions(content)
                for para_text, should_be_italic in paragraph_styles.items():
                    # Check if this paragraph contains an image placeholder
                    if '[IMAGE]' in para_text:
                        # Split by image placeholder
                        parts = para_text.split('[IMAGE]')
                        for i, part in enumerate(parts):
                            if part.strip():  # Add text if not empty
                                if is_diary_entry or should_be_italic:
                                    story.append(Paragraph(part, italic_style))
                                else:
                                    story.append(Paragraph(part, body_style))
                            # Add image after the text (but not after the last part)
                            if i < len(parts) - 1 and images:
                                img = images.pop(0)
                                try:
                                    # Resolve relative path to absolute path
                                    img_path = os.path.join(PROJECT_DIR, img['src'].lstrip('../'))
                                    if os.path.exists(img_path):
                                        # Scale image to fit PDF while maintaining aspect ratio (half size)
                                        max_width = 2.0 * inch
                                        max_height = 2.0 * inch
                                        img_obj = Image(img_path, width=min(img['width']/18*inch, max_width), height=min(img['height']/18*inch, max_height))
                                        story.append(img_obj)
                                        story.append(Spacer(1, 0.1 * inch))
                                except Exception as e:
                                    print(f"⚠️ Warning: Could not load image {img['src']}: {e}")
                    else:
                        # No image in this paragraph, add normally
                        if is_diary_entry or should_be_italic:
                            story.append(Paragraph(para_text, italic_style))
                        else:
                            story.append(Paragraph(para_text, body_style))
            
            # Spacing between entries
            if entry_idx < len(entries) - 1:
                story.append(Spacer(1, 0.2 * inch))
        
        # Page break between chapters (except after last)
        if chapter_num < len(CHAPTERS):
            story.append(PageBreak())
    
    # ===== BACK MATTER =====
    story.append(PageBreak())
    story.append(Spacer(1, 2 * inch))
    
    story.append(Paragraph("❦ ❦ ❦", ornament_style))
    story.append(Spacer(1, 0.3 * inch))
    
    story.append(Paragraph(
        "Finis",
        ParagraphStyle(
            'TheEnd',
            parent=styles['Normal'],
            fontSize=28,
            textColor=gold,
            alignment=TA_CENTER,
            fontName='Times-Italic',
            spaceAfter=24,
            letterSpacing=2
        )
    ))
    
    story.append(Spacer(1, 0.5 * inch))
    
    story.append(Paragraph(
        "Some mysteries are solved in an instant.<br/>Others haunt us for a century.",
        ParagraphStyle(
            'Colophon',
            parent=styles['Normal'],
            fontSize=12,
            textColor=rust,
            alignment=TA_CENTER,
            fontName='Times-Italic',
            leading=16
        )
    ))
    
    story.append(Spacer(1, 1 * inch))
    story.append(Paragraph("✦", ornament_style))
    
    # Build PDF
    try:
        doc.build(story)
        file_size = os.path.getsize(pdf_path) / (1024 * 1024)  # Size in MB
        print(f"\n✅ Book PDF created successfully!")
        print(f"   📄 Location: {pdf_path}")
        print(f"   📊 Size: {file_size:.2f} MB")
        print(f"   📖 Chapters: {len(CHAPTERS)}")
        return pdf_path
    except Exception as e:
        print(f"❌ Error creating PDF: {e}")
        return None

if __name__ == "__main__":
    pdf_path = generate_book_pdf()
    if pdf_path:
        print(f"\n🎉 Ready to read! Open: {pdf_path}")


#!/usr/bin/env python3
"""
Generate a PDF from the last 4 chapters with copyable text.
"""

import json
import os
from pathlib import Path
from datetime import datetime
import re

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_LEFT, TA_CENTER
    from reportlab.lib.colors import HexColor
    from html2text import html2text
except ImportError:
    print("Error: Required packages not installed.")
    print("Run: pip install reportlab html2text")
    exit(1)

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, 'data', 'book')
OUTPUT_DIR = os.path.join(PROJECT_DIR, 'to_print')

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Chapters in reading order
CHAPTERS = [
    ('chapter_investigation_begins.json', 'Investigation Begins'),
    ('chapter_thomas_whitmore.json', 'Ghost of Thomas'),
    ('chapter_elixir_eternal_love.json', 'Elixir of Eternal Love'),
    ('chapter_dressmaker_devotion.json', "Dressmaker's Devotion"),
    ('chapter_cordelia_decline.json', "Cordelia's Decline"),
    ('chapter_romano_treasure.json', 'Search for Romano Treasure'),
    ('chapter_secrets_unravelled.json', 'Secrets Unravelled'),
    ('chapter_bakers_inheritance.json', "Baker's Inheritance"),
]

def strip_html_tags(text):
    """Remove HTML tags but preserve text content."""
    # Remove img tags and their attributes
    text = re.sub(r'<img[^>]*>', '', text)
    # Remove other HTML tags but keep content
    text = re.sub(r'<[^>]+>', '', text)
    return text.strip()

def format_entry(entry):
    """Format a single entry for the PDF."""
    date = entry.get('date', '')
    location = entry.get('location', '')
    title = entry.get('title', '')
    content = entry.get('content', '')
    
    # Clean HTML from content
    clean_content = strip_html_tags(content)
    
    # Format the entry
    header = f"{date} - {location}"
    if title:
        header += f" - {title}"
    
    return header, clean_content

def generate_pdf():
    """Generate PDF from the last 4 chapters."""
    
    # Create PDF
    pdf_path = os.path.join(OUTPUT_DIR, 'last_4_chapters.pdf')
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    story = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=HexColor('#1a1a1a'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    chapter_style = ParagraphStyle(
        'ChapterTitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=HexColor('#333333'),
        spaceAfter=10,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    entry_header_style = ParagraphStyle(
        'EntryHeader',
        parent=styles['Normal'],
        fontSize=11,
        textColor=HexColor('#555555'),
        spaceAfter=6,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=10,
        textColor=HexColor('#1a1a1a'),
        spaceAfter=10,
        leading=14,
        alignment=TA_LEFT
    )
    
    # Add title
    story.append(Paragraph("Murder Mystery: Last 4 Chapters", title_style))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Process each chapter
    for chapter_file, chapter_name in CHAPTERS:
        chapter_path = os.path.join(DATA_DIR, chapter_file)
        
        if not os.path.exists(chapter_path):
            print(f"Warning: {chapter_file} not found")
            continue
        
        print(f"Processing {chapter_name}...")
        
        with open(chapter_path, 'r') as f:
            chapter_data = json.load(f)
        
        # Add chapter title
        story.append(Paragraph(chapter_name, chapter_style))
        story.append(Spacer(1, 0.15*inch))
        
        # Process entries
        for entry in chapter_data.get('entries', []):
            header, content = format_entry(entry)
            
            # Add entry header
            story.append(Paragraph(header, entry_header_style))
            
            # Add content
            # Break into paragraphs
            paragraphs = content.split('\n\n')
            for para_text in paragraphs:
                if para_text.strip():
                    story.append(Paragraph(para_text.strip(), body_style))
            
            story.append(Spacer(1, 0.1*inch))
        
        # Page break between chapters (except after last)
        if chapter_file != CHAPTERS[-1][0]:
            story.append(PageBreak())
    
    # Build PDF
    try:
        doc.build(story)
        print(f"✅ PDF created: {pdf_path}")
        return pdf_path
    except Exception as e:
        print(f"❌ Error creating PDF: {e}")
        return None

if __name__ == "__main__":
    generate_pdf()


# Card PDF Generator - Quick Reference

## Usage
```bash
python card_pdf_generator.py --config config.json --output cards.pdf
```

## Config File Format
JSON file with card layout and data settings:
- `card_size`: Card dimensions in inches
- `page_size`: Page dimensions in inches  
- `data_source`: JSON file with card data
- `title`: Card title (e.g., "FACT", "RUMOR")
- `image_path_template`: Optional image path template
- `qr_path_template`: Optional QR code path template

## Examples
- Fact cards: 2.5" × 3.5" cards from `data/rumors.json`
- Character cards: 3" × 4" cards with photos and QR codes
- Rumor cards: Cards with AI-generated images

## Output
PDF file with cards arranged in grid layout, ready for printing.

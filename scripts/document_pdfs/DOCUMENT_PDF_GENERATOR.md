# Document PDF Generator - Quick Reference

## Usage
```bash
python document_pdf_generator.py --config config.json --output documents.pdf
```

## Config File Format
JSON with layout settings:
- `layout`: "full", "half", or "grid"
- `items`: List of images with optional QR codes
- `qr_overlay`: Enable QR code overlays
- `page_size`: Page dimensions in inches

## Layouts
- **full**: One image per page
- **half**: Two images per page (stacked)
- **grid**: Multiple images per page (configurable grid)

## Output
PDF file with images arranged per layout, ready for printing.

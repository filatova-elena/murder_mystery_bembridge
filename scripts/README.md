# Image Generation Scripts

This directory contains scripts for generating images using the Google Gemini API.

## Setup

1. **Install dependencies** (one time):
   ```bash
   python3 -m venv ../venv
   source ../venv/bin/activate
   pip install google-generativeai pillow
   ```

2. **Set your Gemini API key**:
   ```bash
   export GEMINI_API_KEY='your-api-key-here'
   ```

   You can get an API key from: https://aistudio.google.com/apikey

## Scripts

### generate_doctors_office_image.py

Generates a portrait of Dr. Thaddeus Crane in his office for the "A Day Well Spent" entry in the Doctor's Orders chapter.

**Usage**:
```bash
source ../venv/bin/activate
export GEMINI_API_KEY='your-key'
python3 generate_doctors_office_image.py
```

**Output**: Saves image to `assets/doctors_office_portrait.png`

## Notes

- Generated images are saved to the `assets/` directory
- The `venv/` directory is gitignored and not committed
- The `scripts/` directory is gitignored and not committed
- Large generated image files (*.png, *.jpg) are gitignored per project settings
- To add generated images to the book, manually update the JSON chapters with `<img>` tags

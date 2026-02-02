# Eleventy Setup for Murder Mystery

This is an **optional** alternative to the vanilla HTML/JS setup. Eleventy generates static HTML from templates + JSON data.

## Quick Start

```bash
# Install dependencies
npm install

# Start dev server with hot reload
npm run dev

# Build for production
npm run build
```

The site will be available at `http://localhost:8080`

## How It Works

### Folder Structure

```
murder_mystery/
├── src/                          # Source files (Eleventy input)
│   ├── _data/                    # Global data loaders
│   │   ├── characters.js         # Loads all data/character/*.json
│   │   ├── skills.js             # Loads data/skills.json
│   │   └── bookChapters.js       # Loads all data/book/*.json
│   │
│   ├── _includes/                # Reusable templates
│   │   └── layouts/
│   │       ├── base.njk          # Base HTML shell
│   │       └── character.njk     # Character page template
│   │
│   ├── character/
│   │   ├── characters.njk        # Character index page
│   │   └── character-pages.njk   # Generates ALL character pages via pagination
│   │
│   └── index.njk                 # Homepage
│
├── data/                         # Your existing JSON data (unchanged!)
│   ├── character/
│   │   ├── doctor.json
│   │   └── ...
│   ├── book/
│   │   └── ...
│   └── skills.json
│
├── assets/                       # Static assets (passed through unchanged)
│
├── _site/                        # Generated output (gitignored)
│
├── eleventy.config.js            # Eleventy configuration
└── package.json                  # npm scripts
```

### The Magic: Pagination

The file `src/character/character-pages.njk` is a **single file** that generates **all** character pages:

```yaml
---
pagination:
  data: characters
  size: 1
---
```

When Eleventy runs, it:
1. Loads `characters.js` which reads all JSON files from `data/character/`
2. For each character, generates a page using the `character.njk` layout
3. Outputs `/character/doctor.html`, `/character/baker.html`, etc.

**Add a new character?** Just add a JSON file to `data/character/` and rebuild. No new HTML file needed.

## Templates (Nunjucks)

Eleventy uses [Nunjucks](https://mozilla.github.io/nunjucks/) for templating. Quick syntax:

```njk
{# This is a comment #}

{{ variable }}                    {# Output a variable #}

{% if condition %}                {# Conditionals #}
  ...
{% endif %}

{% for item in array %}           {# Loops #}
  {{ item }}
{% endfor %}

{% set foo = "bar" %}             {# Set a variable #}

{{ text | truncate(80) }}         {# Filters #}
```

## Comparison: Before vs After

### Before (Vanilla JS)

Each character needs:
- `character/doctor.html` (159 lines)
- `character/baker.html` (159 lines)
- `character/psychic.html` (159 lines)
- ... (21 nearly identical files)

Total: ~3,339 lines of duplicated HTML/JS

### After (Eleventy)

- `src/_includes/layouts/character.njk` (86 lines) - ONE template
- `src/character/character-pages.njk` (20 lines) - generates all pages

Total: ~106 lines

**Result: 97% reduction in template code**

## When to Use What

| Scenario | Use |
|----------|-----|
| Quick content edits | Edit JSON directly, rebuild |
| New character | Add JSON file, rebuild |
| Template changes | Edit `.njk` file, auto-reloads |
| Interactive features | Keep existing `assets/script.js` |
| Book chapters (client-side nav) | Could migrate or keep vanilla JS |

## Migration Path

You don't have to migrate everything at once:

1. **Phase 1**: Character pages (done in this setup)
2. **Phase 2**: Book chapters (can use same pagination pattern)
3. **Phase 3**: Clue pages
4. **Optional**: Keep some pages as vanilla HTML if they need heavy JS

The original `character/*.html` files still work - Eleventy only processes the `src/` folder.

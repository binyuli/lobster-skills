---
name: unsplash
description: Search and download high-quality free images from Unsplash. Use when the user asks for stock photos, background images, blog images, wallpaper, or any high-quality images. Supports searching by keyword, orientation filtering (landscape/portrait/squarish), random photos, and direct download. NO API key required.
---

# Unsplash Image Search

Get millions of high-resolution, royalty-free images from Unsplash — no API key required.

## Quick Start

```bash
# Search for images
unsplash_search.py search "lobster" --count 5

# Search with orientation
unsplash_search.py search "mountain" --orientation landscape

# Get a random photo
unsplash_search.py random --query nature

# Download an image
unsplash_search.py download "https://source.unsplash.com/..." --output photo.jpg
```

## Commands

### Search

Generate image URLs matching a query:

```bash
unsplash_search.py search <query> [options]

Options:
  --count, -c N       Number of URLs (default: 10)
  --orientation, -o   landscape, portrait, squarish
  --size, -s          thumb, small, regular, full
  --json, -j          Output as JSON
```

### Random

Get a random image URL:

```bash
unsplash_search.py random [options]

Options:
  --query, -q         Topic/keyword
  --orientation, -o   landscape, portrait, squarish
  --size, -s          thumb, small, regular, full
  --json, -j          Output as JSON
```

### Download

Download an image to local file:

```bash
unsplash_search.py download <url> [--output FILE]
```

## Image Sizes

| Size | Dimensions | Use Case |
|------|------------|----------|
| `thumb` | 200x200 | Thumbnails |
| `small` | 400x300 | Previews |
| `regular` | 1080x720 | Web display (default) |
| `full` | 1920x1080 | HD backgrounds |

## Example Workflows

### Find a blog background

```bash
# Generate landscape background URLs
unsplash_search.py search "dark abstract" --orientation landscape --size full --count 5

# Pick one and download
unsplash_search.py download "https://source.unsplash.com/1920x1080/dark,abstract?sig=xxx" --output blog-bg.jpg
```

### Random wallpaper

```bash
# Get a random nature wallpaper
unsplash_search.py random --query "nature landscape" --size full

# Download it
unsplash_search.py download "<url>" --output wallpaper.jpg
```

### JSON output for automation

```bash
unsplash_search.py search "coffee" --json > images.json
```

## Usage Notes

- URLs are generated using Unsplash Source API (no auth needed)
- Each URL with a different `sig` parameter returns a different image
- Images are royalty-free for commercial and personal use
- Attribution appreciated but not required

## Attribution (Optional)

If you want to credit Unsplash:

> Photo from [Unsplash](https://unsplash.com)

#!/usr/bin/env python3
"""
Unsplash Image Search - Get high-quality free images from Unsplash.
Uses the public Unsplash Source API (no API key required).

Usage:
    unsplash_search.py search <query> [--count N] [--orientation ORIENTATION]
    unsplash_search.py random [--query TOPIC] [--orientation ORIENTATION]
    unsplash_search.py download <url> [--output FILE]

Examples:
    unsplash_search.py search "lobster" --count 5
    unsplash_search.py random --query nature --orientation landscape
    unsplash_search.py download "https://source.unsplash.com/..." --output photo.jpg
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.parse
import random
import string


def generate_urls(query, count=10, orientation=None, size="1080x720"):
    """
    Generate Unsplash Source URLs for a search query.
    Each URL will return a different random image matching the criteria.
    """
    urls = []

    # Size mapping
    sizes = {
        "thumb": "200x200",
        "small": "400x300",
        "regular": "1080x720",
        "full": "1920x1080",
    }
    if size in sizes:
        size = sizes[size]

    base_url = "https://source.unsplash.com"

    for i in range(count):
        # Build URL with random sig to get different images
        sig = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        parts = [size]
        if query:
            parts.append(query.replace(" ", ","))
        if orientation:
            parts.append(orientation)

        url = f"{base_url}/{'/'.join(parts)}?sig={sig}"
        urls.append(url)

    return urls


def get_random_url(query=None, orientation=None, size="1080x720"):
    """Get a single random image URL."""
    sig = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    sizes = {
        "thumb": "200x200",
        "small": "400x300",
        "regular": "1080x720",
        "full": "1920x1080",
    }
    if size in sizes:
        size = sizes[size]

    base_url = "https://source.unsplash.com"
    parts = [size]

    if query:
        parts.append(query.replace(" ", ","))
    if orientation:
        parts.append(orientation)

    return f"{base_url}/{'/'.join(parts)}?sig={sig}"


def resolve_url(url):
    """Follow redirects to get the final image URL."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.geturl()
    except Exception as e:
        return url


def download_image(url, output_path=None):
    """Download an image from URL."""
    if not output_path:
        output_path = "unsplash_photo.jpg"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as response:
            with open(output_path, "wb") as f:
                f.write(response.read())
        return output_path
    except Exception as e:
        print(f"Download error: {e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Unsplash Image Search (no API key required)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Search command
    search_parser = subparsers.add_parser("search", help="Search for photos")
    search_parser.add_argument("query", help="Search query (e.g., 'lobster', 'nature landscape')")
    search_parser.add_argument("--count", "-c", type=int, default=10, help="Number of URLs (default: 10)")
    search_parser.add_argument("--orientation", "-o", default=None,
                               choices=["landscape", "portrait", "squarish"],
                               help="Filter by orientation")
    search_parser.add_argument("--size", "-s", default="regular",
                               choices=["thumb", "small", "regular", "full"],
                               help="Image size (default: regular)")
    search_parser.add_argument("--resolve", "-r", action="store_true",
                               help="Resolve URLs to final image URLs (slower)")
    search_parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")

    # Random command
    random_parser = subparsers.add_parser("random", help="Get a random photo URL")
    random_parser.add_argument("--query", "-q", help="Topic/keyword for random photo")
    random_parser.add_argument("--orientation", "-o", default=None,
                               choices=["landscape", "portrait", "squarish"],
                               help="Filter by orientation")
    random_parser.add_argument("--size", "-s", default="regular",
                               choices=["thumb", "small", "regular", "full"],
                               help="Image size (default: regular)")
    random_parser.add_argument("--resolve", "-r", action="store_true",
                               help="Resolve URL to final image URL")
    random_parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")

    # Download command
    download_parser = subparsers.add_parser("download", help="Download an image")
    download_parser.add_argument("url", help="Image URL to download")
    download_parser.add_argument("--output", "-o", default=None, help="Output filename")

    args = parser.parse_args()

    if args.command == "search":
        urls = generate_urls(args.query, args.count, args.orientation, args.size)

        results = []
        for i, url in enumerate(urls, 1):
            final_url = resolve_url(url) if args.resolve else url
            results.append({
                "index": i,
                "source_url": url,
                "url": final_url,
            })

        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print(f"Generated {len(results)} image URLs for '{args.query}':\n")
            for r in results:
                print(f"{r['index']}. {r['url']}")

    elif args.command == "random":
        url = get_random_url(args.query, args.orientation, args.size)
        final_url = resolve_url(url) if args.resolve else url

        result = {
            "source_url": url,
            "url": final_url,
        }

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Random image URL:\n{final_url}")

    elif args.command == "download":
        result = download_image(args.url, args.output)
        if result:
            print(f"Downloaded: {result}")
        else:
            sys.exit(1)


if __name__ == "__main__":
    main()

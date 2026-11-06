#!/usr/bin/env python3
"""Build RexWolf artwork gallery; use --metadata-only to update credits without re-encoding images."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import shutil

try:
    from PIL import Image, ImageOps
except ImportError:
    Image = ImageOps = None

ROOT = Path(__file__).resolve().parent
HTML = ROOT / 'gallery.html'
SOURCE = ROOT / 'gallery-source'
THUMBS = ROOT / 'assets/images/thumbs/gallery'
FULL = ROOT / 'assets/images/full/gallery'
DATA = ROOT / 'gallery-data.js'
INFO = ROOT / 'gallery-info.json'
ARTISTS = ROOT / 'artists.json'
SUPPORTED = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp', '.tif', '.tiff'}


def slugify(value: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', value.lower().strip()).strip('-') or 'image'


def pretty_title(stem: str) -> str:
    stem = re.sub(r'^\d+[. _-]*', '', stem)
    return re.sub(r'\s+', ' ', re.sub(r'[_-]+', ' ', stem)).strip().title() or 'Untitled'


def relative_web(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def save_webp(source: Path, dest: Path, bounds: tuple[int, int], quality: int) -> tuple[int, int]:
    with Image.open(source) as opened:
        im = ImageOps.exif_transpose(opened)
        if getattr(im, 'is_animated', False):
            im.seek(0)
        if im.mode not in ('RGB', 'RGBA'):
            im = im.convert('RGBA' if 'transparency' in im.info else 'RGB')
        im.thumbnail(bounds, Image.Resampling.LANCZOS)
        dest.parent.mkdir(parents=True, exist_ok=True)
        im.save(dest, 'WEBP', quality=quality, method=4)
        return im.size


def existing_items() -> dict[str, dict]:
    if not DATA.exists():
        return {}
    raw = DATA.read_text('utf-8')
    match = re.search(r'window\.GALLERY_IMAGES\s*=\s*(\[.*\])\s*;', raw, re.S)
    if not match:
        raise SystemExit('Cannot parse gallery-data.js; run a full build instead.')
    return {item['downloadName']: item for item in json.loads(match.group(1))}


def update_cache_version() -> None:
    version = datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')
    html = HTML.read_text('utf-8')
    for filename in ('gallery-data.js', 'gallery.js'):
        html = re.sub(
            rf'(<script src="{re.escape(filename)})(?:\?v=[^\"]*)?(\"></script>)',
            lambda m: f'{m.group(1)}?v={version}{m.group(2)}', html)
    HTML.write_text(html, 'utf-8')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--metadata-only', action='store_true', help='Update artists, URLs, captions and data without processing images')
    args = parser.parse_args()
    if not args.metadata_only and Image is None:
        raise SystemExit('Pillow required for full builds: python3 -m pip install Pillow')
    metadata = json.loads(INFO.read_text('utf-8')) if INFO.exists() else {}
    artists = json.loads(ARTISTS.read_text('utf-8')) if ARTISTS.exists() else {}
    files = sorted((p for p in SOURCE.rglob('*') if p.is_file() and p.suffix.lower() in SUPPORTED),
                   key=lambda p: p.relative_to(SOURCE).as_posix().lower())
    if not files:
        raise SystemExit(f'No source artwork found under {SOURCE}')
    prior = existing_items() if args.metadata_only else {}
    if args.metadata_only:
        missing = [p.name for p in files if p.name not in prior]
        if missing:
            raise SystemExit(f'{len(missing)} source image(s) have no generated entries; use python3 build_gallery.py to process them. Example: {missing[0]}')
    else:
        shutil.rmtree(THUMBS, ignore_errors=True)
        shutil.rmtree(FULL, ignore_errors=True)
        THUMBS.mkdir(parents=True, exist_ok=True)
        FULL.mkdir(parents=True, exist_ok=True)

    used: set[str] = set()
    items: list[dict] = []
    for num, src in enumerate(files, 1):
        rel = src.relative_to(SOURCE)
        details = metadata.get(rel.as_posix(), metadata.get(src.name, {}))
        artist_key = details.get('artist')
        artist = artists.get(artist_key, {}) if artist_key else {}
        if artist_key and not artist:
            raise SystemExit(f'Artist ID {artist_key!r} for {src.name} not found in artists.json')
        caption = details.get('caption', '')
        credit_prefix = details.get('creditPrefix', 'Art by')
        if artist:
            # Keep any additional caption notes only; the artist credit is rendered separately.
            credit_caption = f"{credit_prefix} {artist['name']}."
            if not caption or re.fullmatch(r'(?:Art|Badge|Commissioned) by .+?\.?', caption.strip(), re.I):
                caption = credit_caption
        if args.metadata_only:
            item = dict(prior[src.name])
        else:
            base = slugify(src.stem)
            slug = base
            counter = 2
            while slug in used:
                slug = f'{base}-{counter}'
                counter += 1
            used.add(slug)
            thumb, full = THUMBS / f'{slug}.webp', FULL / f'{slug}.webp'
            save_webp(src, thumb, (640, 640), 82)
            w, h = save_webp(src, full, (2200, 2200), 88)
            item = {'thumb': relative_web(thumb), 'src': relative_web(full),
                    'downloadName': src.name, 'width': w, 'height': h}
        item.update({'title': details.get('title') or pretty_title(src.stem),
                     'caption': caption,
                     'category': details.get('category') or (rel.parent.name if rel.parent != Path('.') else 'Gallery'),
                     'artist': artist.get('name', ''),
                     'artistUrl': artist.get('url', ''),
                     'creditPrefix': credit_prefix if artist else ''})
        items.append(item)
        print(f'[{num}/{len(files)}] {"metadata" if args.metadata_only else "built"} {rel}')
    DATA.write_text('// Generated by build_gallery.py. Do not edit by hand.\n'
                    'window.GALLERY_IMAGES = ' + json.dumps(items, ensure_ascii=False, indent=2) + ';\n', 'utf-8')
    update_cache_version()
    print(f'Gallery updated: {len(items)} images; {"no images reprocessed" if args.metadata_only else "images regenerated"}.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

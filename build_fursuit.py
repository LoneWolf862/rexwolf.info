#!/usr/bin/env python3
"""Build Wolf in the Wild gallery from fursuit-source/ photos."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import argparse
import json
import re

try:
    from PIL import Image, ImageOps, UnidentifiedImageError
except ImportError:
    raise SystemExit('Pillow required: python3 -m pip install Pillow')

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'fursuit-source'
THUMBS = ROOT / 'assets/images/thumbs/fursuit'
FULL = ROOT / 'assets/images/full/fursuit'
DOWNLOADS = ROOT / 'assets/images/downloads/fursuit'
DATA = ROOT / 'fursuit-data.js'
HTML = ROOT / 'fursuit.html'
INFO = ROOT / 'fursuit-info.json'
CACHE = ROOT / 'fursuit-build-cache.json'
SUPPORTED = {'.jpg', '.jpeg', '.png', '.webp', '.tif', '.tiff', '.bmp'}


def slug(value: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', value.lower()).strip('-') or 'photo'


def make_webp(source: Path, destination: Path, bounds: tuple[int, int], quality: int) -> tuple[int, int]:
    # EXIF orientation is applied; metadata (GPS, camera IDs, etc.) is not copied.
    with Image.open(source) as original:
        if getattr(original, 'is_animated', False):
            original.seek(0)
        image = ImageOps.exif_transpose(original)
        image = image.convert('RGB')
        image.thumbnail(bounds, Image.Resampling.LANCZOS)
        destination.parent.mkdir(parents=True, exist_ok=True)
        image.save(destination, 'WEBP', quality=quality, method=6)
        return image.size


def make_download(source: Path, destination: Path) -> None:
    """Keep original pixel dimensions and JPEG/PNG type, but remove EXIF/GPS metadata.

    JPEG must be re-encoded to remove metadata; use high-quality encoding.
    PNG pixels are saved losslessly. Neither result is byte-identical to its source.
    """
    with Image.open(source) as opened:
        image = ImageOps.exif_transpose(opened)
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.suffix.lower() == '.png':
            if image.mode not in ('RGB', 'RGBA', 'L', 'LA', 'P'):
                image = image.convert('RGBA' if 'A' in image.getbands() else 'RGB')
            # Construct a new image so imported PNG text/EXIF/ICC metadata is discarded.
            clean = Image.new(image.mode, image.size)
            clean.paste(image)
            clean.save(destination, 'PNG', optimize=True)
        else:
            if image.mode != 'RGB':
                image = image.convert('RGB')
            image.save(destination, 'JPEG', quality=98, subsampling=0, optimize=True)


def main() -> int:
    parser = argparse.ArgumentParser(description='Incremental fursuit gallery builder')
    parser.add_argument('--force', action='store_true', help='Regenerate every image, even if cached')
    args = parser.parse_args()
    SOURCE.mkdir(exist_ok=True)
    metadata = json.loads(INFO.read_text('utf-8')) if INFO.exists() else {}
    files = sorted((p for p in SOURCE.rglob('*') if p.is_file() and p.suffix.lower() in SUPPORTED),
                   key=lambda p: p.relative_to(SOURCE).as_posix().casefold())
    if not files:
        print('No photos found. Add images under fursuit-source/ and run again.')
        return 1

    # Keep source originals on your machine; only sanitized WebP derivatives need deployment.
    THUMBS.mkdir(parents=True, exist_ok=True)
    FULL.mkdir(parents=True, exist_ok=True)
    DOWNLOADS.mkdir(parents=True, exist_ok=True)
    try:
        cache = json.loads(CACHE.read_text('utf-8')) if CACHE.exists() else {}
    except (OSError, ValueError):
        cache = {}
    new_cache = {}
    used = set()
    items = []
    intended = set()
    built = 0
    reused = 0
    for number, source in enumerate(files, 1):
        rel = source.relative_to(SOURCE).as_posix()
        details = metadata.get(rel, metadata.get(source.name, {}))
        name = slug(source.stem)
        candidate = name
        suffix = 2
        while candidate in used:
            candidate = f'{name}-{suffix}'
            suffix += 1
        used.add(candidate)
        thumb = THUMBS / f'{candidate}.webp'
        full = FULL / f'{candidate}.webp'
        # Photos from other image formats are exported as PNG to avoid introducing JPEG loss.
        extension = source.suffix.lower()
        download_ext = extension if extension in ('.jpg', '.jpeg', '.png') else '.png'
        downloadable = DOWNLOADS / f'{candidate}{download_ext}'
        stat = source.stat()
        signature = [stat.st_size, stat.st_mtime_ns]
        outputs = [thumb, full, downloadable]
        prior = cache.get(rel, {})
        cached = (not args.force and all(p.is_file() and p.stat().st_size > 0 for p in outputs)
                  and (prior.get('signature') == signature and prior.get('download') == downloadable.name
                       or not CACHE.exists()))
        # If upgrading from the original builder, existing outputs can be reused
        # immediately. --force always regenerates every image.
        if cached:
            if prior.get('width') and prior.get('height'):
                width, height = prior['width'], prior['height']
            else:
                with Image.open(full) as existing:
                    width, height = existing.size
            reused += 1
        else:
            try:
                make_webp(source, thumb, (420, 560), 79)
                width, height = make_webp(source, full, (2560, 2560), 88)
                make_download(source, downloadable)
            except (UnidentifiedImageError, OSError, ValueError) as exc:
                print(f'Skipping {rel}: {exc}')
                continue
            built += 1
        new_cache[rel] = {'signature': signature, 'download': downloadable.name,
                          'width': width, 'height': height}
        intended.update((thumb, full, downloadable))
        title = details.get('title') or re.sub(r'[-_]+', ' ', source.stem).strip().title()
        items.append({
            'title': title,
            'caption': details.get('caption', ''),
            'thumb': thumb.relative_to(ROOT).as_posix(),
            'src': full.relative_to(ROOT).as_posix(),
            'download': downloadable.relative_to(ROOT).as_posix(),
            'downloadName': candidate + download_ext,
            'width': width, 'height': height,
        })
        print(f'[{number}/{len(files)}] {"cached" if cached else "built "} {rel} → {candidate}.webp')
    for folder in (THUMBS, FULL, DOWNLOADS):
        for old in folder.iterdir():
            if old not in intended:
                old.unlink()
    CACHE.write_text(json.dumps(new_cache, indent=2) + '\n', 'utf-8')
    DATA.write_text('// Generated by build_fursuit.py — do not edit manually.\n'
                    'window.FURSUIT_IMAGES = ' + json.dumps(items, indent=2, ensure_ascii=False) + ';\n', 'utf-8')
    version = datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')
    html = HTML.read_text('utf-8')
    for filename in ('fursuit-data.js', 'fursuit.js'):
        html = re.sub(rf'(<script src="{re.escape(filename)})(?:\?v=[^\"]*)?(\"></script>)',
                      lambda m: f'{m.group(1)}?v={version}{m.group(2)}', html)
    HTML.write_text(html, 'utf-8')
    print(f'Gallery: {len(items)} photos ({built} processed, {reused} reused).')
    print('Publish HTML, CSS, JS, assets/images/*/fursuit/; originals are not needed.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

# Doxed — Wolf in the Wild

The fursuit gallery is part of rexwolf.info and uses the site's existing palette and lightbox components.
Its dense CSS masonry wall preserves each photograph's natural aspect ratio.

## Adding photographs

1. Put new photos in `fursuit-source/` (nested directories are supported).
2. Ensure Pillow is installed (`python3 -m pip install Pillow`, or use your system's Python/Pillow package).
3. Run `python3 build_fursuit.py` from the repository directory.
   - Unchanged photos are reused using `fursuit-build-cache.json`.
   - Use `python3 build_fursuit.py --force` only when a full rebuild is needed.
4. Check `fursuit.html` in a browser. The gallery supports lightbox navigation, keyboard arrows, mobile swipe, and downloads.

Edit `fursuit-info.json` to provide optional titles and captions (keyed by source-relative filename), then rerun the builder.

## What gets published

- **Commit to Git:** `fursuit.html`, `fursuit.css`, `fursuit.js`, `fursuit-data.js`, `fursuit-info.json`, and `build_fursuit.py`.
- **Excluded from Git:** `fursuit-source/`, `fursuit-build-cache.json`, and the generated fursuit image folders under `assets/images/{thumbs,full,downloads}/fursuit/`.
- Generated thumbnails/lightbox photos are WebP. Download copies retain JPEG/PNG formats and original pixel dimensions (with metadata removed; JPEGs are re-encoded).
- The generated photo folders **must remain on the web server**: a fresh Git clone alone does not contain the gallery photographs.

**Privacy:** Do not serve `fursuit-source/` publicly. It may contain original EXIF/GPS metadata. Keep originals outside the web root or block the URL path at Nginx.

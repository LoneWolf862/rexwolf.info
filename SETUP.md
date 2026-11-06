# Doxed — Wolf in the Wild

This add-on was designed against the existing `index.html`, `styles.css`, `gallery.html`, `gallery.js`, `stickers.html`, `stickers.css`, and `build_gallery.py` in `LoneWolf862/rexwolf.info`.

1. Copy files and `assets/` folders in this package into the **root of the existing repository**. Do not replace existing `styles.css` or any gallery files.
2. From the repository root, run `python3 add_nav.py`. It inserts the new card directly **between** Sticker Gallery and Drawing Rex? without affecting the other links.
3. Add photos to `fursuit-source/` (nested folders are supported). Install Pillow: `python3 -m pip install Pillow`, then run `python3 build_fursuit.py`.
4. Preview with `python3 -m http.server 8000`, visit `http://localhost:8000/fursuit.html`.
5. Commit/publish the new gallery page, CSS, JS, data JS, and generated `assets/images/thumbs/fursuit/` and `assets/images/full/fursuit/`. For a large library, avoid committing the raw `fursuit-source` originals: originals are not referenced by the page. Add `fursuit-source/` to `.gitignore` if you don't want to publish the originals.

For optional captions, edit `fursuit-info.json`: e.g. `{ "convention/IMG_0102.jpg": {"title":"Con day one", "caption":"Hanging out with friends"} }`, then rebuild.

**Design:** compact 3:4 portrait-oriented cells with uncropped images (`object-fit: contain`), responsive density, lightweight WebP thumbs, full-screen viewer, keyboard arrows, touch swipe, close/backdrop/Escape, count, download and focus restoration. Original EXIF (including potentially sensitive GPS coordinates) isn't copied into generated images. For very large photo archives, consider pagination or generating batches in a later iteration.

#!/usr/bin/env python3
"""Insert the Wolf in the Wild card before Drawing Rex? in index.html."""
from pathlib import Path

page = Path(__file__).resolve().parent / 'index.html'
if not page.exists():
    raise SystemExit('Run from a copy placed in the rexwolf.info repository root.')
html = page.read_text(encoding='utf-8')
if 'href="fursuit.html"' in html:
    print('Wolf in the Wild navigation card already exists.')
    raise SystemExit(0)
anchor = '      <a class="social-card gallery-link" href="reference.html">'
if html.count(anchor) != 1:
    raise SystemExit('Could not find unique Drawing Rex? link. No changes made.')
new = '''      <a class="social-card gallery-link" href="fursuit.html">
        <span class="icon-box" aria-hidden="true">📸</span>
        <span class="link-copy"><strong>Doxed - Wolf in the Wild</strong><small>Fursuit pictures and IRL wolf sightings</small></span><span class="action">→</span>
      </a>

'''
page.write_text(html.replace(anchor, new + anchor), encoding='utf-8')
print('Navigation card inserted between Sticker Gallery and Drawing Rex?.')

RexWolf creator credits extension — Sticker + Wolf in the Wild

Requires that the previous artist credit update has been installed:
  /var/www/rexwolf.info/artists.json

Transfer artist-links.js and install_creator_credits.py into the website root.
Run on Zeta from that root:
  python3 install_creator_credits.py

This modifies ONLY stickers.html, fursuit.html, and stickers.css.
It does not rebuild galleries or touch any images.
It uses artists.json as the one directory of creator display names and URLs.
The artist link script must remain in the website root and be committed.

Verify https://rexwolf.info/stickers.html and https://rexwolf.info/fursuit.html
then:
  git diff --check
  git diff -- stickers.html fursuit.html stickers.css
  git add artist-links.js stickers.html fursuit.html stickers.css
  git commit -m "Reuse artist directory in sticker and fursuit credits"
  git push origin main

The installer can be deleted after use. Backups are saved in your home directory outside the public website.

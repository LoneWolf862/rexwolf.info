REXWOLF STICKER GALLERY

Copy the contents of this folder into:
/var/www/rexwolf.info/

Then run:
  cd /var/www/rexwolf.info
  python3 build_stickers.py

Open:
  https://rexwolf.info/stickers.html

ADDING STICKERS
1. Put transparent images in /var/www/rexwolf.info/sticker-source/
2. Edit titles/captions in sticker-info.json if desired.
3. Run python3 build_stickers.py

ORDER
Files sort alphabetically. Prefix names with 00., 01., 02., etc. to control order.
The leading number is removed from the displayed title.

HOME PAGE LINK
Add:
  <a href="/stickers.html">Stickers</a>

NOTE
The supplied Apple link is the general App Store page. Replace it in stickers.html
with the direct Wolf Stickers App Store listing when you have that URL.

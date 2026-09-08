REXWOLF STICKER GALLERY

Copy the contents into source folder:
scp -r "C:\Users\Rex\OneDrive\Pictures\0. Fluffy\0. Kaito\stickers\." wolf@10.80.67.215:/var/www/rexwolf.info/sticker-source/

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


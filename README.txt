REXWOLF.INFO STATIC WEBSITE

MAIN FILES
- index.html             NFC/social landing page
- gallery.html           Gallery page and fullscreen viewer
- styles.css             Site styling
- script.js              Discord copy button
- gallery.js             Gallery viewer behavior
- gallery-data.js        Auto-generated gallery list; do not edit manually
- gallery-source/        Put original gallery images here
- gallery-info.json      Optional custom titles and captions
- update-gallery.bat     Double-click this after adding images
- build_gallery.py       Script used by update-gallery.bat

HOW TO ADD GALLERY IMAGES
1. Copy new JPG, PNG, WEBP, GIF, BMP, or TIFF files into gallery-source.
   You may also create subfolders to organize your originals.
2. Double-click update-gallery.bat.
3. Wait until it says "Gallery updated."
4. Open gallery.html to check the results.
5. Upload the entire updated website folder to your server.

The builder automatically:
- Finds every supported image in gallery-source and its subfolders.
- Corrects phone-camera rotation.
- Creates lightweight WebP thumbnails.
- Creates optimized full-size WebP images.
- Rebuilds gallery-data.js.
- Removes generated files for images that you deleted from gallery-source.

CUSTOM TITLES AND CAPTIONS
Open gallery-info.json in a text editor. Each image can have a custom title and caption:

"My Picture.png": {
  "title": "My Picture",
  "caption": "A short description."
}

The filename must exactly match the file in gallery-source. Files without an entry are automatically titled from their filename.

FIRST-TIME REQUIREMENT
The update script needs Python 3 and Pillow. If Pillow is missing, open Command Prompt in this folder and run:

py -m pip install Pillow

DEPLOYMENT
Upload the contents of this folder to /var/www/rexwolf.info or deploy it through Cloudflare Pages. Keep gallery-source and the builder scripts in your local copy; they do not affect the public website, though uploading them is harmless.

Before programming the NFC tag, test https://rexwolf.info on multiple phones. Write the full HTTPS URL as a URL/URI NFC record.

Git:
cd /var/www/rexwolf.info
git status
git add .
git commit -m "Describe the update"
git push

permission commands:
find /var/www/rexwolf.info -type d -exec chmod 755 {} \;
find /var/www/rexwolf.info -type f -exec chmod 644 {} \;
chmod 775 /var/www


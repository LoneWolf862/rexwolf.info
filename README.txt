REXWOLF.INFO STATIC WEBSITE

Files:
- index.html        Main NFC/social landing page
- gallery.html      Image gallery with fullscreen viewer
- styles.css        All visual styling
- script.js         Discord copy button
- gallery.js        Gallery/lightbox controls
- assets/images/    Optimized WebP artwork

DEPLOY TO CLOUDFLARE PAGES (direct upload):
1. Sign in to Cloudflare.
2. Go to Workers & Pages > Create > Pages > Upload assets.
3. Upload this folder (or the included rexwolf-site.zip).
4. After deployment, open Custom domains and add rexwolf.info.
5. Cloudflare will configure HTTPS and the DNS records.

EDITING LINKS:
Open index.html in a text editor and replace the href URL and visible username in the matching social-card.

ADDING GALLERY IMAGES:
1. Add a thumbnail under assets/images/thumbs and a full image under assets/images/full.
2. Copy a gallery-card block in gallery.html.
3. Add the matching object to the images array in gallery.js.

Before programming the NFC tag, test https://rexwolf.info on multiple phones. Program the tag as a URL record using the full HTTPS address.

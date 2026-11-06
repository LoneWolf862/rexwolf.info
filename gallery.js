const images = Array.isArray(window.GALLERY_IMAGES) ? window.GALLERY_IMAGES : [];
let current = 0;
let touchStart = 0;
let previousFocus = null;

const grid = document.querySelector('.gallery-grid');
const empty = document.querySelector('.gallery-empty');
const box = document.querySelector('.lightbox');
const image = document.querySelector('#lightbox-image');
const title = document.querySelector('#lightbox-title');
const caption = document.querySelector('#lightbox-caption');
const counter = document.querySelector('#lightbox-counter');
const download = document.querySelector('#download-link');
const closeButton = document.querySelector('.close-btn');

function creditText(item) {
  return `${item.creditPrefix || 'Art by'} ${item.artist}`;
}

function createCredit(item, className) {
  const label = document.createElement('span');
  label.className = className;
  if (!item.artist) {
    label.textContent = item.caption || item.category || 'RexWolf gallery';
    return label;
  }
  label.append(document.createTextNode(`${item.creditPrefix || 'Art by'} `));
  if (item.artistUrl) {
    const link = document.createElement('a');
    link.className = 'artist-link';
    link.href = item.artistUrl;
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    link.textContent = item.artist;
    link.setAttribute('aria-label', `Visit ${item.artist}'s website (opens in new tab)`);
    label.append(link);
  } else {
    label.append(document.createTextNode(item.artist));
  }
  label.append(document.createTextNode('.'));
  return label;
}

function createCards() {
  if (!images.length) {
    empty.hidden = false;
    return;
  }
  const fragment = document.createDocumentFragment();
  images.forEach((item, index) => {
    // Link and image button are siblings, avoiding invalid nested interactive elements.
    const card = document.createElement('div');
    card.className = 'gallery-card';
    const button = document.createElement('button');
    button.className = 'gallery-card-open';
    button.type = 'button';
    button.setAttribute('aria-label', `View ${item.title || `artwork ${index + 1}`}`);
    const img = document.createElement('img');
    img.src = item.thumb;
    img.alt = item.title || 'Artwork';
    img.loading = 'lazy';
    img.decoding = 'async';
    const strong = document.createElement('strong');
    strong.textContent = item.title || 'Untitled';
    button.append(img, strong);
    button.addEventListener('click', () => openAt(index));
    card.append(button, createCredit(item, 'gallery-card-credit'));
    fragment.append(card);
  });
  grid.append(fragment);
}

function render() {
  const item = images[current];
  if (!item) return;
  image.src = item.src;
  image.alt = item.title;
  title.textContent = item.title;
  caption.replaceChildren();
  if (item.artist) {
    const credit = createCredit(item, 'gallery-viewer-credit');
    caption.append(credit);
    // Preserve custom notes where the caption isn't simply the credit line.
    const normalizedCaption = (item.caption || '').trim().replace(/\.$/, '');
    const normalizedCredit = creditText(item).replace(/\.$/, '');
    if (normalizedCaption && normalizedCaption !== normalizedCredit) {
      caption.append(document.createTextNode(` • ${item.caption}`));
    }
  } else if (item.caption) {
    caption.append(document.createTextNode(item.caption));
  }
  if (item.width && item.height) {
    caption.append(document.createTextNode(`${caption.textContent ? ' • ' : ''}${item.width} × ${item.height}`));
  }
  counter.textContent = `${current + 1} / ${images.length}`;
  download.href = item.src;
  download.download = item.downloadName || item.src.split('/').pop();
}

function openAt(index) {
  previousFocus = document.activeElement;
  current = index;
  render();
  box.classList.add('open');
  box.setAttribute('aria-hidden', 'false');
  document.body.style.overflow = 'hidden';
  closeButton.focus();
}

function close() {
  box.classList.remove('open');
  box.setAttribute('aria-hidden', 'true');
  document.body.style.overflow = '';
  if (previousFocus && previousFocus.isConnected) previousFocus.focus();
}

function move(direction) {
  if (!images.length) return;
  current = (current + direction + images.length) % images.length;
  render();
}

createCards();
closeButton.addEventListener('click', close);
document.querySelector('.prev').addEventListener('click', () => move(-1));
document.querySelector('.next').addEventListener('click', () => move(1));
box.addEventListener('click', event => { if (event.target === box) close(); });
document.addEventListener('keydown', event => {
  if (!box.classList.contains('open')) return;
  if (event.key === 'Escape') close();
  if (event.key === 'ArrowLeft') { event.preventDefault(); move(-1); }
  if (event.key === 'ArrowRight') { event.preventDefault(); move(1); }
});
box.addEventListener('touchstart', event => {
  touchStart = event.changedTouches[0].clientX;
}, { passive: true });
box.addEventListener('touchend', event => {
  const delta = event.changedTouches[0].clientX - touchStart;
  if (Math.abs(delta) > 55) move(delta > 0 ? -1 : 1);
}, { passive: true });

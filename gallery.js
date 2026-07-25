const images = Array.isArray(window.GALLERY_IMAGES) ? window.GALLERY_IMAGES : [];
let current = 0;
let touchStart = 0;

const grid = document.querySelector('.gallery-grid');
const empty = document.querySelector('.gallery-empty');
const box = document.querySelector('.lightbox');
const image = document.querySelector('#lightbox-image');
const title = document.querySelector('#lightbox-title');
const caption = document.querySelector('#lightbox-caption');
const counter = document.querySelector('#lightbox-counter');
const download = document.querySelector('#download-link');

function createCards() {
  if (!images.length) {
    empty.hidden = false;
    return;
  }
  const fragment = document.createDocumentFragment();
  images.forEach((item, index) => {
    const button = document.createElement('button');
    button.className = 'gallery-card';
    button.type = 'button';
    button.dataset.index = String(index);

    const img = document.createElement('img');
    img.src = item.thumb;
    img.alt = item.title;
    img.loading = 'lazy';
    img.decoding = 'async';

    const text = document.createElement('span');
    const strong = document.createElement('strong');
    strong.textContent = item.title;
    const small = document.createElement('small');
    small.textContent = item.caption || item.category || 'RexWolf gallery';
    text.append(strong, small);
    button.append(img, text);
    button.addEventListener('click', () => openAt(index));
    fragment.append(button);
  });
  grid.append(fragment);
}

function render() {
  const item = images[current];
  if (!item) return;
  image.src = item.src;
  image.alt = item.title;
  title.textContent = item.title;
  const dimensions = item.width && item.height ? `${item.width} × ${item.height}` : '';
  caption.textContent = [item.caption, dimensions].filter(Boolean).join(' • ');
  counter.textContent = `${current + 1} / ${images.length}`;
  download.href = item.src;
  download.download = item.downloadName || item.src.split('/').pop();
}

function openAt(index) {
  current = index;
  render();
  box.classList.add('open');
  box.setAttribute('aria-hidden', 'false');
  document.body.style.overflow = 'hidden';
  document.querySelector('.close-btn').focus();
}

function close() {
  box.classList.remove('open');
  box.setAttribute('aria-hidden', 'true');
  document.body.style.overflow = '';
}

function move(direction) {
  if (!images.length) return;
  current = (current + direction + images.length) % images.length;
  render();
}

createCards();
document.querySelector('.close-btn').addEventListener('click', close);
document.querySelector('.prev').addEventListener('click', () => move(-1));
document.querySelector('.next').addEventListener('click', () => move(1));
box.addEventListener('click', event => { if (event.target === box) close(); });
document.addEventListener('keydown', event => {
  if (!box.classList.contains('open')) return;
  if (event.key === 'Escape') close();
  if (event.key === 'ArrowLeft') move(-1);
  if (event.key === 'ArrowRight') move(1);
});
box.addEventListener('touchstart', event => {
  touchStart = event.changedTouches[0].clientX;
}, { passive: true });
box.addEventListener('touchend', event => {
  const delta = event.changedTouches[0].clientX - touchStart;
  if (Math.abs(delta) > 55) move(delta > 0 ? -1 : 1);
}, { passive: true });

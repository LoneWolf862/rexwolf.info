(() => {
  const photos = Array.isArray(window.FURSUIT_IMAGES) ? window.FURSUIT_IMAGES : [];
  const grid = document.getElementById('wild-grid');
  const empty = document.getElementById('wild-empty');
  const count = document.getElementById('wild-count');
  const box = document.getElementById('wild-lightbox');
  const viewer = document.getElementById('wild-image');
  const title = document.getElementById('wild-title');
  const caption = document.getElementById('wild-caption');
  const counter = document.getElementById('wild-counter');
  const download = document.getElementById('wild-download');
  const closeButton = box.querySelector('.close-btn');
  let current = 0;
  let previouslyFocused = null;
  let startX = null;
  count.textContent = `${photos.length} photo${photos.length === 1 ? '' : 's'}`;
  empty.hidden = photos.length > 0;

  function render() {
    const item = photos[current];
    if (!item) return;
    viewer.src = item.src;
    viewer.alt = item.title || 'Wolf in the Wild photo';
    title.textContent = item.title || 'Wolf in the Wild';
    caption.textContent = item.caption || '';
    counter.textContent = `${current + 1} / ${photos.length}`;
    download.href = item.download || item.src;
    download.download = item.downloadName || item.src.split('/').pop();
  }
  function open(index) {
    if (!photos.length) return;
    previouslyFocused = document.activeElement;
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
    viewer.removeAttribute('src');
    if (previouslyFocused && previouslyFocused.isConnected) previouslyFocused.focus();
  }
  function move(delta) {
    if (!photos.length) return;
    current = (current + delta + photos.length) % photos.length;
    render();
  }
  const fragment = document.createDocumentFragment();
  photos.forEach((item, index) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'wild-card';
    button.setAttribute('aria-label', `View ${item.title || `photo ${index + 1}`}`);
    const img = document.createElement('img');
    img.src = item.thumb;
    if (item.width && item.height) { img.width = item.width; img.height = item.height; }
    img.alt = item.title || 'Fursuit photo';
    img.loading = index < 9 ? 'eager' : 'lazy';
    img.decoding = 'async';
    const label = document.createElement('span');
    label.textContent = item.title || `Photo ${index + 1}`;
    button.append(img, label);
    button.addEventListener('click', () => open(index));
    fragment.append(button);
  });
  grid.append(fragment);
  closeButton.addEventListener('click', close);
  box.querySelector('.prev').addEventListener('click', () => move(-1));
  box.querySelector('.next').addEventListener('click', () => move(1));
  box.addEventListener('click', e => { if (e.target === box) close(); });
  document.addEventListener('keydown', e => {
    if (!box.classList.contains('open')) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowLeft') { e.preventDefault(); move(-1); }
    if (e.key === 'ArrowRight') { e.preventDefault(); move(1); }
    if (e.key === 'Tab') {
      const focusables = [download, closeButton, box.querySelector('.prev'), box.querySelector('.next')];
      const position = focusables.indexOf(document.activeElement);
      if (e.shiftKey && position === 0) { e.preventDefault(); focusables.at(-1).focus(); }
      if (!e.shiftKey && position === focusables.length - 1) { e.preventDefault(); focusables[0].focus(); }
    }
  });
  box.addEventListener('touchstart', e => { startX = e.changedTouches[0].clientX; }, { passive: true });
  box.addEventListener('touchend', e => {
    if (startX === null) return;
    const dx = e.changedTouches[0].clientX - startX;
    startX = null;
    if (Math.abs(dx) > 55) move(dx > 0 ? -1 : 1);
  }, { passive: true });
})();

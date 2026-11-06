/* Shared artist credits for static RexWolf pages. artists.json is the single source of URLs/names. */
(() => {
  const credits = document.querySelectorAll('[data-artist]');
  if (!credits.length) return;
  fetch('artists.json', { cache: 'no-cache' })
    .then(response => {
      if (!response.ok) throw new Error(`artists.json: HTTP ${response.status}`);
      return response.json();
    })
    .then(artists => {
      credits.forEach(node => {
        const artist = artists[node.dataset.artist];
        if (!artist) return; // Keep readable fallback if an artist is absent.
        const label = artist.name || node.textContent.trim();
        if (!artist.url || !/^https:\/\//i.test(artist.url)) {
          node.textContent = label;
          return;
        }
        const link = document.createElement('a');
        link.href = artist.url;
        link.target = '_blank';
        link.rel = 'noopener noreferrer';
        link.textContent = label;
        node.replaceWith(link);
      });
    })
    .catch(error => console.warn('Artist credits unavailable; showing plain-text names.', error));
})();

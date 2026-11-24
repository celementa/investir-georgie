{
  // grow bars when their block scrolls into view
  for (const rows of document.querySelectorAll('.rows')) {
    const bars = rows.querySelectorAll('.bar i[data-w]');
    const grow = () => bars.forEach(b => b.style.width = b.dataset.w + '%');
    if ('IntersectionObserver' in window) {
      const io = new IntersectionObserver(e => { if (e.some(x => x.isIntersecting)) { grow(); io.disconnect(); } });
      io.observe(rows);
    } else grow();
  }
  // label stacked table cells on phones
  for (const t of document.querySelectorAll('table.stack')) {
    const h = [...t.rows[0].cells].map(c => c.textContent.trim());
    for (const r of [...t.rows].slice(1)) [...r.cells].forEach((c, i) => c.dataset.l = h[i] || '');
  }
  // draft forms send nothing yet
  for (const f of document.querySelectorAll('form[data-draft]')) {
    f.addEventListener('submit', e => { e.preventDefault(); const ok = f.querySelector('.ok'); if (ok) ok.style.display = 'block'; });
  }
}

// Footer year
document.querySelectorAll('[data-year]').forEach(el => { el.textContent = new Date().getFullYear(); });

// Mobile menu
const nav = document.querySelector('.nav');
const menuBtn = document.querySelector('.menu-btn');
if (nav && menuBtn) {
  const setOpen = open => {
    nav.classList.toggle('open', open);
    menuBtn.setAttribute('aria-expanded', String(open));
  };
  menuBtn.addEventListener('click', () => setOpen(!nav.classList.contains('open')));
  nav.querySelectorAll('.nav-links a').forEach(a => a.addEventListener('click', () => setOpen(false)));
  document.addEventListener('keydown', e => { if (e.key === 'Escape') setOpen(false); });
}

// Highlight the navbar link for the section currently in view
const sectionLinks = [...document.querySelectorAll('.nav-links a[href^="#"]:not(.btn)')];
const sections = sectionLinks.map(a => document.querySelector(a.getAttribute('href'))).filter(Boolean);
if ('IntersectionObserver' in window && sections.length) {
  const visible = new Set();
  const update = () => {
    // the visible section that sits highest on the page wins
    const current = sections.find(s => visible.has(s));
    sectionLinks.forEach(a => a.classList.toggle('active', !!current && a.getAttribute('href') === '#' + current.id));
  };
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => e.isIntersecting ? visible.add(e.target) : visible.delete(e.target));
    update();
  }, { rootMargin: '-45% 0px -50% 0px' });   // a thin band across the middle of the screen
  sections.forEach(s => io.observe(s));
}

document.addEventListener('DOMContentLoaded', function() {
  const toggle = document.getElementById('nav-toggle');
  const overlay = document.getElementById('mobile-menu-overlay');
  const closeBtn = document.getElementById('mobile-menu-close');

  if (!toggle || !overlay || !closeBtn) return;

  function openMenu() {
    overlay.classList.add('is-open');
    toggle.setAttribute('aria-expanded', 'true');
    document.body.classList.add('nav-open');
    document.body.style.overflow = 'hidden';
    setTimeout(() => closeBtn.focus(), 100);
  }

  function closeMenu() {
    overlay.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
    document.body.classList.remove('nav-open');
    document.body.style.overflow = '';
    setTimeout(() => toggle.focus(), 100);
  }

  toggle.addEventListener('click', function(e) {
    e.stopPropagation();
    overlay.classList.contains('is-open') ? closeMenu() : openMenu();
  });

  closeBtn.addEventListener('click', closeMenu);

  overlay.addEventListener('click', function(e) {
    if (e.target === overlay) closeMenu();
  });

  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && overlay.classList.contains('is-open')) {
      closeMenu();
    }
  });

  overlay.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => setTimeout(closeMenu, 150));
  });

  window.addEventListener('resize', function() {
    if (window.innerWidth > 768 && overlay.classList.contains('is-open')) {
      closeMenu();
    }
  });
});
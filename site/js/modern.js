(function () {
  'use strict';
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.site-nav');
  function closeMenu() {
    nav.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
  }
  toggle.addEventListener('click', function () {
    var open = nav.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', String(open));
  });
  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') {
      if (nav.classList.contains('is-open')) { closeMenu(); toggle.focus(); }
      document.querySelectorAll('.nav-drop[open]').forEach(function (item) { item.open = false; });
    }
  });
  document.addEventListener('click', function (event) {
    document.querySelectorAll('.nav-drop[open]').forEach(function (item) {
      if (!item.contains(event.target)) item.open = false;
    });
    if (!nav.contains(event.target) && !toggle.contains(event.target)) closeMenu();
  });
  nav.querySelectorAll('a').forEach(function (link) { link.addEventListener('click', closeMenu); });
}());

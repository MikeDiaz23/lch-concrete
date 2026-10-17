(function () {
  'use strict';
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.site-nav');
  var dropdowns = Array.from(nav.querySelectorAll('.nav-drop'));
  var hoverMenu = window.matchMedia('(min-width: 851px) and (hover: hover) and (pointer: fine)');
  var closeTimers = new WeakMap();
  function closeDropdown(dropdown) {
    window.clearTimeout(closeTimers.get(dropdown));
    dropdown.open = false;
  }
  dropdowns.forEach(function (dropdown) {
    dropdown.addEventListener('pointerenter', function (event) {
      if (!hoverMenu.matches || event.pointerType !== 'mouse') return;
      window.clearTimeout(closeTimers.get(dropdown));
      dropdowns.forEach(function (other) {
        if (other !== dropdown) closeDropdown(other);
      });
      dropdown.open = true;
    });
    dropdown.addEventListener('pointerleave', function (event) {
      if (!hoverMenu.matches || event.pointerType !== 'mouse') return;
      // A small grace period keeps the panel steady while moving into its links.
      closeTimers.set(dropdown, window.setTimeout(function () {
        if (!dropdown.contains(document.activeElement)) closeDropdown(dropdown);
      }, 160));
    });
    dropdown.addEventListener('focusout', function () {
      window.setTimeout(function () {
        if (!dropdown.contains(document.activeElement) && !dropdown.matches(':hover')) closeDropdown(dropdown);
      }, 0);
    });
  });
  hoverMenu.addEventListener('change', function () { dropdowns.forEach(closeDropdown); });
  function closeMenu() {
    nav.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
    dropdowns.forEach(closeDropdown);
  }
  toggle.addEventListener('click', function () {
    var open = nav.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', String(open));
  });
  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') {
      if (nav.classList.contains('is-open')) { closeMenu(); toggle.focus(); }
      dropdowns.forEach(function (item) {
        if (item.open && item.contains(document.activeElement)) item.querySelector('summary').focus();
        closeDropdown(item);
      });
    }
  });
  document.addEventListener('click', function (event) {
    document.querySelectorAll('.nav-drop[open]').forEach(function (item) {
      if (!item.contains(event.target)) closeDropdown(item);
    });
    if (!nav.contains(event.target) && !toggle.contains(event.target)) closeMenu();
  });
  nav.querySelectorAll('a').forEach(function (link) { link.addEventListener('click', closeMenu); });
}());

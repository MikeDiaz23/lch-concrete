/* Restore the saved appearance before styles render, then bind the header switch. */
(function () {
  'use strict';
  var root = document.documentElement;
  var storageKey = 'lch-theme';
  var saved;
  try { saved = window.localStorage.getItem(storageKey); } catch (error) {}
  root.dataset.theme = saved === 'light' ? 'light' : 'dark';

  function updateSwitch() {
    var button = document.querySelector('.theme-toggle');
    if (!button) return;
    var light = root.dataset.theme === 'light';
    button.setAttribute('aria-checked', String(light));
    button.title = light ? 'Switch to dark mode' : 'Switch to light mode';
    button.hidden = false;
  }

  function setTheme(theme) {
    root.dataset.theme = theme === 'light' ? 'light' : 'dark';
    updateSwitch();
    document.dispatchEvent(new CustomEvent('lch:themechange'));
  }

  document.addEventListener('DOMContentLoaded', function () {
    updateSwitch();
    var button = document.querySelector('.theme-toggle');
    if (!button) return;
    button.addEventListener('click', function () {
      setTheme(root.dataset.theme === 'light' ? 'dark' : 'light');
      try { window.localStorage.setItem(storageKey, root.dataset.theme); } catch (error) {}
    });
  });

  window.addEventListener('storage', function (event) {
    if (event.key === storageKey || event.key === null) setTheme(event.newValue);
  });
}());

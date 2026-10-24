/* Draw a tile's construction sketch, then resolve its project photograph. */
(function () {
  'use strict';
  var root = document.documentElement;
  var cards = Array.from(document.querySelectorAll('.studio-hero .orbit-card')).filter(function (card) {
    return card.getClientRects().length > 0;
  });
  var motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  var timer;
  var alreadyFocused = document.activeElement && document.activeElement !== document.body && document.activeElement !== root;
  if (!cards.length || motion.matches || alreadyFocused || !root.classList.contains('tile-intro-pending')) {
    root.classList.remove('tile-intro-pending');
    return;
  }

  var sketches = [
    'M33 8L25 77M66 8L74 77M9 40L91 40',
    'M9 42H91M47 8V42M66 42V77',
    'M25 77L39 8M75 77L61 8M31 48L69 48',
    'M9 30H91M9 56H91M35 8V30M64 30V56M35 56V77'
  ];
  var namespace = 'http://www.w3.org/2000/svg';
  cards.forEach(function (card, index) {
    card.style.setProperty('--tile-delay', index * 110 + 'ms');
    var draft = document.createElement('span');
    draft.className = 'tile-draft';
    draft.setAttribute('aria-hidden', 'true');
    var image = card.querySelector('img');
    // Match the real image bounds so its arrival never changes the framing.
    draft.style.top = image.offsetTop + 'px';
    draft.style.left = image.offsetLeft + 'px';
    draft.style.width = image.offsetWidth + 'px';
    draft.style.height = image.offsetHeight + 'px';
    var svg = document.createElementNS(namespace, 'svg');
    svg.setAttribute('viewBox', '0 0 100 100');
    svg.setAttribute('preserveAspectRatio', 'none');
    svg.setAttribute('focusable', 'false');
    [
      ['tile-draft-guides', 'M5 0V100M95 0V100M0 5H100M0 81H100'],
      ['tile-draft-frame', 'M8 1H92Q99 1 99 8V92Q99 99 92 99H8Q1 99 1 92V8Q1 1 8 1Z'],
      ['tile-draft-joints', sketches[index]],
      ['tile-draft-caption', 'M10 90H44M84 90H91']
    ].forEach(function (part) {
      var path = document.createElementNS(namespace, 'path');
      path.setAttribute('class', part[0]);
      path.setAttribute('d', part[1]);
      path.setAttribute('pathLength', '1');
      svg.appendChild(path);
    });
    draft.appendChild(svg);
    card.appendChild(draft);
  });

  function finish() {
    window.clearTimeout(timer);
    root.classList.remove('tile-intro-pending', 'tile-intro');
    cards.forEach(function (card) {
      card.style.removeProperty('--tile-delay');
      var draft = card.querySelector('.tile-draft');
      if (draft) draft.remove();
    });
    document.removeEventListener('pointerdown', finish, true);
    document.removeEventListener('keydown', finish, true);
    document.removeEventListener('focusin', finish, true);
    motion.removeEventListener('change', finish);
  }

  // Reveal immediately if someone starts interacting; navigation is never delayed.
  document.addEventListener('pointerdown', finish, true);
  document.addEventListener('keydown', finish, true);
  document.addEventListener('focusin', finish, true);
  motion.addEventListener('change', finish);
  // Decode before fading when possible, without holding the page on a slow image.
  var decoded = cards.map(function (card) {
    var image = card.querySelector('img');
    return image.decode ? image.decode().catch(function () {}) : Promise.resolve();
  });
  Promise.race([
    Promise.all(decoded),
    new Promise(function (resolve) { window.setTimeout(resolve, 500); })
  ]).then(function () {
    if (!root.classList.contains('tile-intro-pending')) return;
    root.classList.replace('tile-intro-pending', 'tile-intro');
    timer = window.setTimeout(finish, 2300);
  });
}());

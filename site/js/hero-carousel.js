/* A single project card, with optional automatic rotation and native controls. */
(function () {
  'use strict';
  var carousel = document.querySelector('.hero-project-carousel');
  if (!carousel) return;
  var slides = Array.from(carousel.querySelectorAll('[data-project-slide]'));
  if (slides.length < 2) return;
  var controls = carousel.querySelector('.hero-carousel-controls');
  var counter = carousel.querySelector('.hero-carousel-count');
  var toggle = carousel.querySelector('[data-carousel-toggle]');
  var announcement = carousel.querySelector('.hero-carousel-announcement');
  var motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  var index = 0;
  var timer;
  var paused = motion.matches;
  var hovered = false;
  var focused = carousel.contains(document.activeElement);
  var visible = false;

  function schedule() {
    window.clearTimeout(timer);
    if (paused || hovered || focused || !visible || document.hidden) return;
    timer = window.setTimeout(function () { show(index + 1, false); }, 6000);
  }

  function updateToggle() {
    toggle.textContent = paused ? 'Play' : 'Pause';
    toggle.setAttribute('aria-label', paused ? 'Start automatic project rotation' : 'Pause automatic project rotation');
  }

  function show(next, manual) {
    index = (next + slides.length) % slides.length;
    slides.forEach(function (slide, position) { slide.hidden = position !== index; });
    counter.textContent = String(index + 1).padStart(2, '0') + ' / ' + String(slides.length).padStart(2, '0');
    if (manual) {
      // Manual browsing stays on the chosen project until the visitor selects Play.
      paused = true;
      announcement.textContent = slides[index].getAttribute('aria-label');
      updateToggle();
    }
    schedule();
  }

  controls.hidden = false;
  updateToggle();
  carousel.querySelector('[data-carousel-prev]').addEventListener('click', function () { show(index - 1, true); });
  carousel.querySelector('[data-carousel-next]').addEventListener('click', function () { show(index + 1, true); });
  toggle.addEventListener('click', function () {
    paused = !paused;
    updateToggle();
    schedule();
  });
  carousel.addEventListener('keydown', function (event) {
    if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
    event.preventDefault();
    show(index + (event.key === 'ArrowRight' ? 1 : -1), true);
  });
  carousel.addEventListener('pointerenter', function (event) {
    if (event.pointerType !== 'mouse') return;
    hovered = true;
    schedule();
  });
  carousel.addEventListener('pointerleave', function () { hovered = false; schedule(); });
  carousel.addEventListener('focusin', function () { focused = true; schedule(); });
  carousel.addEventListener('focusout', function () {
    window.setTimeout(function () {
      focused = carousel.contains(document.activeElement);
      schedule();
    }, 0);
  });
  document.addEventListener('visibilitychange', schedule);
  motion.addEventListener('change', function () {
    if (motion.matches) paused = true;
    updateToggle();
    schedule();
  });
  new IntersectionObserver(function (entries) {
    visible = entries[0].isIntersecting && entries[0].intersectionRatio >= .25;
    schedule();
  }, { threshold: [0, .25] }).observe(carousel);
}());

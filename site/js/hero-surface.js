/* A quiet, pointer-responsive concrete surface without grid lines. */
(function () {
  'use strict';
  var hero = document.querySelector('.studio-hero');
  var canvas = hero && hero.querySelector('.hero-surface');
  if (!canvas) return;
  var context = canvas.getContext('2d');
  if (!context) return;
  var motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  var width = 0;
  var height = 0;
  var grains = [];
  var pointer = { x: 0, y: 0, active: false };
  var light = { x: 0, y: 0 };
  var trail = [];
  var frame = 0;
  var previous = 0;
  var visible = true;
  var phase = 0;
  var lightTheme = document.documentElement.dataset.theme === 'light';

  // Retain the concrete plane's depth without drawing its former grid.
  var planeOrigin = { x: .52, y: -.75 };
  var crossSlope = -.095;

  // Seeded texture stays stable when the viewport changes.
  function random(seed) {
    var value = Math.sin(seed * 127.1 + 311.7) * 43758.5453;
    return value - Math.floor(value);
  }

  function resize() {
    var rect = hero.getBoundingClientRect();
    width = rect.width;
    height = rect.height;
    var scale = Math.min(window.devicePixelRatio || 1, 1.5);
    canvas.width = Math.round(width * scale);
    canvas.height = Math.round(height * scale);
    context.setTransform(scale, 0, 0, scale, 0, 0);
    grains = [];
    var count = Math.min(1400, Math.round(width * height / 650));
    for (var i = 0; i < count; i++) {
      grains.push({ x: random(i + 1) * width, y: random(i + 4000) * height,
        size: .35 + random(i + 8000) * 1.1, tone: random(i + 12000) });
    }
    light.x = width * .35;
    light.y = height * .65;
    trail = [];
    draw();
  }

  function draw() {
    if (!width || !height) return;
    context.clearRect(0, 0, width, height);
    var radius = Math.min(width * .4, 250);
    var wash = context.createRadialGradient(light.x, light.y, 0, light.x, light.y, radius);
    var washTone = lightTheme ? '118,91,61' : '195,173,142';
    var washOpacity = lightTheme ? (pointer.active ? .14 : .035) : (pointer.active ? .085 : .035);
    wash.addColorStop(0, 'rgba(' + washTone + ',' + washOpacity + ')');
    wash.addColorStop(1, 'rgba(' + washTone + ',0)');
    context.fillStyle = wash;
    context.fillRect(0, 0, width, height);

    grains.forEach(function (grain) {
      var dx = grain.x - light.x;
      var dy = grain.y - light.y;
      var distance = Math.hypot(dx, dy);
      var influence = Math.max(0, 1 - distance / radius);
      var displacement = pointer.active && !motion.matches ? influence * influence * 7 : 0;
      var x = grain.x + (distance ? dx / distance * displacement : 0);
      var y = grain.y + (distance ? dy / distance * displacement : 0);
      var depth = lightTheme ? 1 : (grain.y / height - planeOrigin.y -
        crossSlope * (grain.x / width - planeOrigin.x)) / .95;
      var grainWidth = grain.size * depth;
      var grainHeight = grain.size * depth;
      var alpha = .06 + grain.tone * .14 + influence * .26;
      if (!lightTheme) alpha /= Math.max(1, depth);
      context.fillStyle = lightTheme ? 'rgba(105,91,71,' + alpha * .85 + ')' : 'rgba(200,190,172,' + alpha + ')';
      context.beginPath();
      // Small angular flecks evoke the mineral aggregate in concrete.
      context.moveTo(x, y - grainHeight);
      context.lineTo(x + grainWidth, y);
      context.lineTo(x, y + grainHeight * .65);
      context.closePath();
      context.fill();
    });

    // A short, fading sweep recalls the pass of a finishing trowel.
    if (trail.length > 1 && !motion.matches) {
      var first = trail[0];
      var last = trail[trail.length - 1];
      var opacity = Math.max(0, 1 - last.age / 1100) * (lightTheme ? .17 : .1);
      var trailTone = lightTheme ? '110,85,57' : '203,177,142';
      var stroke = context.createLinearGradient(first.x, first.y, last.x, last.y);
      stroke.addColorStop(0, 'rgba(' + trailTone + ',0)');
      stroke.addColorStop(1, 'rgba(' + trailTone + ',' + opacity + ')');
      context.save();
      context.lineCap = 'round';
      context.lineJoin = 'round';
      context.filter = 'blur(4px)';
      context.strokeStyle = stroke;
      context.lineWidth = 24;
      context.beginPath();
      context.moveTo(first.x, first.y);
      for (var i = 1; i < trail.length; i++) {
        context.lineTo(trail[i].x, trail[i].y);
      }
      context.stroke();
      context.restore();
    }
  }

  function tick(now) {
    frame = 0;
    if (motion.matches || !visible || document.hidden) return;
    if (now - previous >= 32) {
      var elapsed = Math.min(now - previous, 64);
      previous = now;
      phase += elapsed * .00018;
      var targetX = pointer.active ? pointer.x : width * (.5 + Math.sin(phase) * .29);
      var targetY = pointer.active ? pointer.y : height * (.5 + Math.cos(phase * .7) * .27);
      light.x += (targetX - light.x) * .09;
      light.y += (targetY - light.y) * .09;
      trail.forEach(function (point) { point.age += elapsed; });
      trail = trail.filter(function (point) { return point.age < 1100; });
      draw();
    }
    frame = window.requestAnimationFrame(tick);
  }

  function start() {
    if (!frame && visible && !document.hidden && !motion.matches) {
      previous = performance.now();
      frame = window.requestAnimationFrame(tick);
    }
  }

  function stop() {
    window.cancelAnimationFrame(frame);
    frame = 0;
  }

  hero.addEventListener('pointermove', function (event) {
    if (motion.matches) return;
    var rect = hero.getBoundingClientRect();
    pointer.x = event.clientX - rect.left;
    pointer.y = event.clientY - rect.top;
    pointer.active = true;
    var last = trail[trail.length - 1];
    if (!last || Math.hypot(pointer.x - last.x, pointer.y - last.y) > 8) {
      trail.push({ x: pointer.x, y: pointer.y, age: 0 });
      if (trail.length > 35) trail.shift();
    }
  }, { passive: true });
  hero.addEventListener('pointerleave', function () { pointer.active = false; });
  hero.addEventListener('pointerup', function (event) {
    if (event.pointerType === 'touch') pointer.active = false;
  }, { passive: true });
  hero.addEventListener('pointercancel', function () { pointer.active = false; });
  document.addEventListener('lch:themechange', function () {
    lightTheme = document.documentElement.dataset.theme === 'light';
    draw();
  });
  document.addEventListener('visibilitychange', function () {
    if (document.hidden) stop(); else start();
  });
  motion.addEventListener('change', function () {
    stop();
    pointer.active = false;
    trail = [];
    draw();
    start();
  });
  var observer = new IntersectionObserver(function (entries) {
    visible = entries[0].isIntersecting;
    if (visible) start(); else stop();
  });
  observer.observe(hero);
  new ResizeObserver(resize).observe(hero);
  resize();
  start();
}());

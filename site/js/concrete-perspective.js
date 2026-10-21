/* Project the static concrete texture onto the same plane as the hero grid. */
(function () {
  'use strict';
  var surface = document.querySelector('.hero-concrete');
  var grid = surface && surface.querySelector('.studio-hero');
  var traces = grid && grid.querySelector('.hero-traces');
  if (!traces) return;
  var paths = Array.from(traces.querySelectorAll('path'));
  var vanishing = paths[0].getPointAtLength(0);
  var crossSeam = paths.find(function (path) {
    return path.getPointAtLength(0).y >= 0;
  });
  if (!crossSeam) return;
  var start = crossSeam.getPointAtLength(0);
  var end = crossSeam.getPointAtLength(crossSeam.getTotalLength());
  var view = traces.viewBox.baseVal;
  var canvas = document.createElement('canvas');
  canvas.className = 'concrete-perspective';
  canvas.setAttribute('aria-hidden', 'true');
  var context = canvas.getContext('2d');
  if (!context) return;
  surface.prepend(canvas);
  var texture = new Image();
  var raster;
  var loading = false;
  var frame = 0;

  function render() {
    frame = 0;
    if (document.documentElement.dataset.theme === 'light') return;
    if (!raster) {
      if (!loading) {
        loading = true;
        texture.onload = function () {
          var buffer = document.createElement('canvas');
          buffer.width = texture.naturalWidth;
          buffer.height = texture.naturalHeight;
          var bufferContext = buffer.getContext('2d');
          if (!bufferContext) return;
          // Cache the material once; projection resamples this bitmap on resize.
          bufferContext.drawImage(texture, 0, 0);
          raster = buffer;
          schedule();
        };
        texture.src = '/images/concrete-photo-v1.jpg';
      }
      return;
    }
    var bounds = surface.getBoundingClientRect();
    var gridBounds = grid.getBoundingClientRect();
    if (!bounds.width || !bounds.height || !gridBounds.height) return;
    var resolution = Math.min(window.devicePixelRatio || 1, 1.5);
    canvas.width = Math.round(bounds.width * resolution);
    canvas.height = Math.round(bounds.height * resolution);
    var vx = gridBounds.left - bounds.left + vanishing.x / view.width * gridBounds.width;
    var vy = gridBounds.top - bounds.top + vanishing.y / view.height * gridBounds.height;
    var slope = (end.y - start.y) / view.height * gridBounds.height /
      ((end.x - start.x) / view.width * gridBounds.width);
    var reference = gridBounds.height * .95;
    var tile = raster.width;
    var step = 1 / resolution;
    var leftOffset = slope * vx;
    var rightOffset = -slope * (bounds.width - vx);
    var firstRow = Math.floor(Math.min(leftOffset, rightOffset));
    var lastRow = Math.ceil(bounds.height + Math.max(leftOffset, rightOffset));

    // Flatten the slanted cross-seams for sampling, then shear them back into place.
    context.setTransform(resolution, slope * resolution, 0, resolution, 0, -slope * vx * resolution);
    function drawRow(sourceY, sourceHeight, y, height, tileWidth) {
      var firstX = vx + Math.floor(-vx / tileWidth) * tileWidth;
      for (var x = firstX; x < bounds.width; x += tileWidth) {
        context.drawImage(raster, 0, sourceY, tile, sourceHeight,
          x, y, tileWidth, height + .15 / resolution);
      }
    }
    for (var y = firstRow; y < lastRow; y += step) {
      var distance = Math.max(1, y - vy);
      var scale = distance / reference;
      // Reciprocal depth compresses both the grain and its spacing in the distance.
      var sourceY = ((-reference * reference / distance) % tile + tile) % tile;
      var sourceHeight = reference * reference * (1 / distance - 1 / (distance + step));
      var tileWidth = tile * scale;
      var available = Math.min(sourceHeight, tile - sourceY);
      var firstHeight = step * available / sourceHeight;
      drawRow(sourceY, available, y, firstHeight, tileWidth);
      if (available < sourceHeight) {
        drawRow(0, sourceHeight - available, y + firstHeight, step - firstHeight, tileWidth);
      }
    }
    surface.classList.add('concrete-perspective-ready');
  }

  function schedule() {
    if (!frame) frame = window.requestAnimationFrame(render);
  }
  var observer = new ResizeObserver(schedule);
  observer.observe(surface);
  observer.observe(grid);
  document.addEventListener('lch:themechange', schedule);
  schedule();
}());

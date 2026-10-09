/* Resizing aids. Picture-size slider sets --img-scale; the pair divider sets --cols. Player code is untouched. */
(function () {
  var MIN = 0.1, MAX = 0.9, ratio = 0.5;
  function px(name) { return parseFloat(getComputedStyle(document.documentElement).getPropertyValue(name)) || 0; }
  function $(id) { return document.getElementById(id); }

  // Picture size (phones): 30 to 100 percent of the normal size
  document.querySelectorAll('.view-bar input[type="range"]').forEach(function (r) {
    r.addEventListener('input', function () {
      document.documentElement.style.setProperty('--img-scale', r.value / 100);
      document.querySelectorAll('.view-bar input[type="range"]').forEach(function (o) { o.value = r.value; });
    });
  });

  // Dividers: pair card (between the two words) and single card (between the two columns)
  function split(screenId, layoutId, label, needsSubgrid, iconsWhenNarrow) {
    var screen = $(screenId), layout = $(layoutId), ratio = 0.5;
    if (!screen || !layout) return;
    var h = document.createElement('div');
    h.className = 'split-handle'; h.setAttribute('role', 'separator'); h.setAttribute('aria-orientation', 'vertical');
    h.setAttribute('aria-label', label); h.tabIndex = 0;
    screen.appendChild(h);
    function place() {
      var s = screen.getBoundingClientRect(), l = layout.getBoundingClientRect();
      var ok = l.width && (needsSubgrid ? CSS.supports('grid-template-rows', 'subgrid') : window.innerWidth >= 768);
      if (!ok) { h.classList.remove('ready'); return; }
      h.style.left = (l.left - s.left + l.width * ratio) + 'px';
      h.style.top = (l.top - s.top) + 'px'; h.style.height = l.height + 'px';
      h.setAttribute('aria-valuenow', Math.round(ratio * 100));
      h.classList.add('ready');
    }
    function limits() {
      var w = layout.getBoundingClientRect().width || 1;
      var m = Math.min(0.5, Math.max(MIN, px(iconsWhenNarrow ? '--col-icon' : '--col-min') / w));
      return [m, 1 - m];
    }
    // Anything that would poke out of its own box? (labels, words, tiles, buttons)
    var BOXES = '.trio-btn, .trio-wrap, .sounds-wrap, .sentence-block, .pair-sentence, .word-hero, .pair-word-row, .rating-btn, .pair-rating-btn, .act-row, .ph-tile, .pair-ph, .section-body, .trio-label';
    function overflows() {
      var els = layout.querySelectorAll(BOXES);
      for (var i = 0; i < els.length; i++) {
        var e = els[i];
        if (e.offsetParent === null) continue;
        if (e.classList.contains('trio-label') && e.clientWidth <= 2) continue;
        if (e.scrollWidth > e.clientWidth + 1) return true;
        var p = e.parentElement;
        if (p && e.classList.contains('trio-label')) { var b = e.closest('.trio-btn'); if (b && e.getBoundingClientRect().right > b.getBoundingClientRect().right + 1) return true; }
      }
      return false;
    }
    // A narrow column keeps its section boxes as icons only; the name stays available to screen readers
    function compact() {
      var sw = px('--col-switch');
      layout.querySelectorAll('.pair-card-half, .card-col').forEach(function (hf) {
        var w = hf.getBoundingClientRect().width; if (!w) return;
        var cs = getComputedStyle(hf), on;
        hf.classList.remove('compact'); hf.classList.remove('tight');
        var inner = hf.getBoundingClientRect().width - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
        on = inner < sw; hf.classList.toggle('compact', on); hf.classList.toggle('tight', !on && inner < px('--col-roomy'));
        if (on) hf.querySelectorAll(':scope > details.section > summary').forEach(function (s) { if (!s.hasAttribute('aria-label')) s.setAttribute('aria-label', s.textContent.trim()); });
      });
    }
    function apply(v) {
      ratio = v;
      layout.style.setProperty('--cols', 'minmax(0,' + ratio + 'fr) minmax(0,' + (1 - ratio) + 'fr)');
      if (iconsWhenNarrow) compact();
    }
    // Move toward the target in small steps and stop where something would first leave its box
    function set(r) {
      var lim = limits();
      r = Math.min(lim[1], Math.max(lim[0], r));
      var dir = r > ratio ? 1 : -1, STEP = 0.01, already = overflows();
      while (Math.abs(r - ratio) > 1e-6) {
        var prev = ratio, next = dir > 0 ? Math.min(r, ratio + STEP) : Math.max(r, ratio - STEP);
        apply(next);
        if (!already && overflows()) {
          // A brief tight spot (one row a little too wide just before a column switches to icons) must not stop the drag:
          // look a few steps ahead and only stop if nothing clears within about a tenth of the width.
          var probe = next, clear = false;
          for (var k = 0; k < 10 && Math.abs(r - probe) > 1e-6; k++) {
            probe = dir > 0 ? Math.min(r, probe + STEP) : Math.max(r, probe - STEP);
            apply(probe);
            if (!overflows()) { clear = true; break; }
          }
          if (!clear) { apply(prev); break; }
        }
      }
      place();
    }
    h.addEventListener('pointerdown', function (e) {
      h.setPointerCapture(e.pointerId); h.classList.add('drag');
      function move(ev) { var l = layout.getBoundingClientRect(); set((ev.clientX - l.left) / l.width); }
      function up() { h.classList.remove('drag'); h.removeEventListener('pointermove', move); h.removeEventListener('pointerup', up); h.removeEventListener('pointercancel', up); }
      h.addEventListener('pointermove', move); h.addEventListener('pointerup', up); h.addEventListener('pointercancel', up);
    });
    h.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') { set(ratio - 0.03); e.preventDefault(); }
      if (e.key === 'ArrowRight') { set(ratio + 0.03); e.preventDefault(); }
    });
    h.addEventListener('dblclick', function () { set(0.5); });
    // Touching a section icon in a narrow column opens up the space first, then opens the section
    if (iconsWhenNarrow) layout.addEventListener('click', function (e) {
      var s = e.target.closest('details.section > summary'); if (!s) return;
      var hf = s.closest('.pair-card-half, .card-col'); if (!hf || !hf.classList.contains('compact')) return;
      e.preventDefault(); e.stopPropagation();
      set(0.5); s.parentNode.open = true;
    }, true);
    new ResizeObserver(function () { var lim = limits(); if (ratio < lim[0] || ratio > lim[1]) set(ratio); else place(); }).observe(layout);
    new MutationObserver(place).observe(screen, { attributes: true, attributeFilter: ['class'] });
    window.addEventListener('resize', place);
  }
  split('screen-pair', 'pair-card-layout', 'Resize the two words', true, true);
  split('screen-single', 'sc-scroll', 'Resize the two columns', false, true);


  // Left column drawer (monitor): the word list slides out of view, it does not reflow
  var app = document.querySelector('.app'), idx = $('screen-index');
  if (app && idx) {
    var rh = document.createElement('div');
    rh.className = 'split-handle rail'; rh.setAttribute('role', 'separator'); rh.setAttribute('aria-orientation', 'vertical');
    rh.setAttribute('aria-label', 'Hide part of the word list'); rh.tabIndex = 0;
    app.appendChild(rh);
    var railW = null;
    function railMax() { return px('--rail'); }
    function railPlace() {
      var a = app.getBoundingClientRect(), i = idx.getBoundingClientRect();
      rh.style.left = (i.right - a.left) + 'px';
    }
    function railSet(w) {
      railW = Math.min(railMax(), Math.max(px('--rail-min'), w));
      app.style.setProperty('--rail-w', railW + 'px');
      railPlace();
    }
    rh.addEventListener('pointerdown', function (e) {
      rh.setPointerCapture(e.pointerId); rh.classList.add('drag');
      function move(ev) { railSet(ev.clientX - app.getBoundingClientRect().left); }
      function up() { rh.classList.remove('drag'); rh.removeEventListener('pointermove', move); rh.removeEventListener('pointerup', up); rh.removeEventListener('pointercancel', up); }
      rh.addEventListener('pointermove', move); rh.addEventListener('pointerup', up); rh.addEventListener('pointercancel', up);
    });
    rh.addEventListener('keydown', function (e) {
      var cur = railW == null ? railMax() : railW;
      if (e.key === 'ArrowLeft') { railSet(cur - 24); e.preventDefault(); }
      if (e.key === 'ArrowRight') { railSet(cur + 24); e.preventDefault(); }
    });
    rh.addEventListener('dblclick', function () { railSet(railMax()); });
    new ResizeObserver(railPlace).observe(app);
    new ResizeObserver(railPlace).observe(idx);
    window.addEventListener('resize', railPlace);
    railPlace();
  }

  // Each word's sections open on their own: the learner chooses what to look at.
})();

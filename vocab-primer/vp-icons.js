/* Swaps emoji glyphs for mask icons by tagging elements with data-ic. Player code is untouched. */
(function () {
  var SEL = '.word-audio,.sentence-audio,.pair-word-audio,.pair-s-audio,.trio-icon,.compare-play,.cat-group-toggle,.tr-globe';
  var MAP = { '\u{1F50A}': 'speaker', '\u25B6': 'play', '\u23F8': 'pause', '\u{1F3A4}': 'mic', '\u23F9': 'stop', '\u{1F310}': 'globe' };
  function nameFor(el, t) {
    t = t.replace(/\uFE0F/g, '').trim();
    if (el.classList.contains('cat-group-toggle')) return t === '\u25BC' ? 'chev-down' : t === '\u25B6' ? 'chev-right' : null;
    return MAP[t] || null;
  }
  function sync() {
    document.querySelectorAll(SEL).forEach(function (el) {
      var n = nameFor(el, el.textContent);
      if (n) { if (el.dataset.ic !== n) el.dataset.ic = n; }
      else if (el.dataset.ic && el.textContent.trim()) delete el.dataset.ic;
    });
  }
  var queued = false;
  function queue() { if (queued) return; queued = true; requestAnimationFrame(function () { queued = false; sync(); }); }
  new MutationObserver(queue).observe(document.documentElement, { subtree: true, childList: true, characterData: true });
  document.addEventListener('DOMContentLoaded', sync);
})();

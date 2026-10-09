/* Guided path: a soft glow on the next step. It only suggests. Nothing locks, nothing counts, and it never nags.
   Next = the first step after the last one the learner touched, so skipping ahead is never "wrong". Player code is untouched. */
(function () {
  var ORDER = ['aud', 'pic', 'ex', 'syl', 'snd', 'say', 'sk', 'rate'];
  var SECTION = { ex: 1, syl: 1, snd: 1, say: 1, sk: 1, rate: 1 };
  var states = new WeakMap();

  // Steps done are kept on this device per word and forgotten after a week, so a word comes back as a fresh review. Nothing leaves the device.
  var STORE = 'sxl.steps', TTL = 7 * 24 * 3600 * 1000;
  function readStore() { try { return JSON.parse(localStorage.getItem(STORE) || '{}'); } catch (e) { return {}; } }
  function wordOf(scope) { var e = scope.id === 'screen-single' ? document.getElementById('sc-word') : scope.querySelector('.pair-word-text'); return e ? e.textContent.trim().toLowerCase() : ''; }
  function persist(scope, s) {
    var w = wordOf(scope); if (!w) return;
    var m = readStore(), now = Date.now(); Object.keys(m).forEach(function (k) { if (now - m[k].t > TTL) delete m[k]; });
    m[w] = { t: now, k: Object.keys(s.done) };
    try { localStorage.setItem(STORE, JSON.stringify(m)); } catch (e) {}
  }
  function state(scope) {
    var s = states.get(scope);
    if (!s) {
      s = { done: {} }; states.set(scope, s); initRated(scope, s);
      var w = wordOf(scope), e = w && readStore()[w];
      if (e && Date.now() - e.t <= TTL) e.k.forEach(function (k) { s.done[k] = true; });
    }
    return s;
  }
  function initRated(scope, s) { s.rated = !!(scope.querySelector('.rating-btn.got-it, .rating-btn.practicing, .pair-rating-btn.got-it, .pair-rating-btn.practicing')); }

  function stepEl(scope, k) {
    if (k === 'aud') return scope.querySelector('.word-audio, .pair-word-audio');
    if (k === 'pic') return scope.querySelector('.flip-slot:not([hidden]) .flip-show');
    var d = scope.querySelector('details.section.' + k);
    if (!d || d.hidden) return null;
    return d;
  }

  var ICON = { ex: 'chat', syl: 'syl', snd: 'wave', say: 'mic', sk: 'pencil', rate: 'smile' };
  function decorate(scope) {
    Object.keys(ICON).forEach(function (k) {
      var s = scope.querySelector('details.section.' + k + ' > summary'); if (!s || s.querySelector('.sec-ic')) return;
      var i = document.createElement('span'); i.className = 'sec-ic'; i.setAttribute('aria-hidden', 'true'); i.style.setProperty('--ic', 'var(--ic-' + ICON[k] + ')');
      s.insertBefore(i, s.firstChild);
    });
  }

  function paint(scope) {
    decorate(scope);
    scope.querySelectorAll('[data-next]').forEach(function (e) { e.removeAttribute('data-next'); });
    var screen = scope.closest('.screen'); if (screen && !screen.classList.contains('active')) return;
    var s = state(scope), last = -1;
    Object.keys(SECTION).forEach(function (k) { var d = scope.querySelector('details.section.' + k); if (d && s.done[k] && !d.classList.contains('done')) d.classList.add('done'); });
    if (s.done.sk) scope.querySelectorAll('.sketch-paper').forEach(function (p) { p.classList.add('done'); });
    ORDER.forEach(function (k, i) { if (s.done[k]) last = i; });
    for (var i = last + 1; i < ORDER.length; i++) {
      var el = stepEl(scope, ORDER[i]);
      if (el) { el.setAttribute('data-next', ''); return; }
    }
  }

  function scopes() {
    var out = [], single = document.getElementById('screen-single');
    if (single) out.push(single);
    document.querySelectorAll('#pair-card-layout .pair-card-half').forEach(function (h) { out.push(h); });
    return out;
  }
  var queued = false;
  function refresh() { if (queued) return; queued = true; requestAnimationFrame(function () { queued = false; scopes().forEach(paint); }); }

  function kindOf(scope, target) {
    if (target.closest('.word-audio, .pair-word-audio')) return 'aud';
    if (target.closest('.flip-show, .flip-face.front')) return 'pic';
    var d = target.closest('details.section');
    if (!d || !scope.contains(d) || target.closest('summary')) return null;
    for (var k in SECTION) if (d.classList.contains(k)) {
      if (k === 'sk') { var p = target.closest('.sketch-paper'); if (!p) return null; p.classList.add('done'); }
      if (k === 'rate' && !target.closest('.rating-btn, .pair-rating-btn')) return null;
      return k;
    }
    return null;
  }
  document.addEventListener('click', function (e) {
    var scope = e.target.closest('.pair-card-half') || e.target.closest('#screen-single'); if (!scope) return;
    var k = kindOf(scope, e.target); if (!k) return;
    var st = state(scope); st.done[k] = true; persist(scope, st); refresh();
  }, true);
  document.addEventListener('toggle', refresh, true);

  // Phones: the learner picks one word of a pair. Until then both show as a picture and a word; touching one opens its card.
  function selectHalf(half) {
    var layout = half.parentNode; if (!layout) return;
    layout.classList.add('picked');
    layout.querySelectorAll('.pair-card-half').forEach(function (h) { h.classList.toggle('sel', h === half); });
    refresh();
  }
  var pairLayout = document.getElementById('pair-card-layout');
  if (pairLayout) {
    pairLayout.addEventListener('click', function (e) {
      var half = e.target.closest('.pair-card-half'); if (!half || e.target.closest('details.section')) return;
      var chosen = half.classList.contains('sel') && pairLayout.classList.contains('picked');
      var phone = window.matchMedia('(max-width: 767px)').matches && document.documentElement.dataset.pair !== 'split';
      if (phone && !pairLayout.classList.contains('picked')) { e.stopPropagation(); e.preventDefault(); selectHalf(half); return; }
      if (phone && !chosen && e.target.closest('.pair-word-row')) { selectHalf(half); return; }
      if (!phone) selectHalf(half);
    }, true);
    new MutationObserver(function () { if (!pairLayout.querySelector('.pair-card-half.sel')) pairLayout.classList.remove('picked'); }).observe(pairLayout, { childList: true });
  }

  // New card: start again. The single card reuses its page, so watch the word; pair halves are rebuilt, so they start fresh themselves.
  var word = document.getElementById('sc-word');
  if (word) new MutationObserver(function () { var sc = document.getElementById('screen-single'); states.delete(sc); document.querySelectorAll('#screen-single .sketch-paper.done, #screen-single details.section.done').forEach(function (p) { p.classList.remove('done'); }); document.querySelectorAll('#screen-single details.section').forEach(function (d) { d.open = false; }); refresh(); }).observe(word, { childList: true, characterData: true, subtree: true });
  new MutationObserver(refresh).observe(document.documentElement, { subtree: true, childList: true, attributes: true, attributeFilter: ['hidden', 'open', 'class'] });
})();

/* "More below": a gold chevron between Prev and Next whenever the card has more to scroll to. Touch it to scroll down. */
(function () {
  [['screen-pair', 'pair-card-layout'], ['screen-single', 'sc-scroll']].forEach(function (p) {
    var screen = document.getElementById(p[0]), sc = document.getElementById(p[1]); if (!screen || !sc) return;
    var bar = screen.querySelector('.card-arrows'); if (!bar) return;
    var b = document.createElement('button'); b.type = 'button'; b.className = 'more-btn'; b.setAttribute('aria-label', 'More below'); b.hidden = true;
    bar.insertBefore(b, bar.lastElementChild);
    function check() { b.hidden = !(sc.scrollHeight - sc.scrollTop - sc.clientHeight > 8); }
    b.addEventListener('click', function () { sc.scrollBy({ top: Math.max(sc.clientHeight * 0.7, 120), behavior: 'smooth' }); });
    sc.addEventListener('scroll', check, { passive: true });
    new ResizeObserver(check).observe(sc);
    new MutationObserver(check).observe(sc, { subtree: true, childList: true, attributes: true, attributeFilter: ['open', 'class', 'hidden'] });
    window.addEventListener('resize', check);
    setInterval(check, 600);
  });
})();

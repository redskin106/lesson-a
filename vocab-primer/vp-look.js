/* Learner colours: a strip of small previews under the word list. Touch one to wear it. Pictures only, kept on this device. */
(function () {
  var KEY = 'sxl.look2', MKEY = 'sxl.mine';
  var SCHEMES = [
    { id: 'auto', label: 'Match my device', theme: null, palette: null, accent: null, hidden: true },
    { id: 'day', label: 'Day', theme: 'light', palette: null, accent: null },
    { id: 'night', label: 'Night', theme: 'dark', palette: null, accent: null },
    { id: 'emberblack', label: 'Ember black', theme: 'dark', palette: 'ember-black', accent: null },
    { id: 'mine', label: 'My own colours', theme: null, palette: null, accent: null }
  ];
  var HUES = [8, 192, 218, 250, 285, 330]; // none near the gold and green that carry meaning
  var TONES = ['light', 'paper', 'mist', 'charcoal', 'dusk', 'black'];
  var TEXTS = ['default', 'cream', 'sky', 'lilac', 'peach', 'rose'], THUE = { cream: [42, 45], sky: [205, 60], lilac: [268, 55], peach: [20, 65], rose: [345, 55] };
  var cur = 'auto', mine = { hue: 218, tone: 'dusk', text: 'default' }, root = document.documentElement;
  try { var s = localStorage.getItem(KEY); if (s && SCHEMES.some(function (x) { return x.id === s; })) cur = s; var m = JSON.parse(localStorage.getItem(MKEY) || 'null'); if (m && HUES.indexOf(m.hue) < 0) m.hue = HUES.reduce(function (a, h) { return Math.abs(h - m.hue) < Math.abs(a - m.hue) ? h : a; }, HUES[0]); if (m && HUES.indexOf(m.hue) >= 0 && TONES.indexOf(m.tone) >= 0) { mine = m; if (TEXTS.indexOf(mine.text) < 0) mine.text = 'default'; } } catch (e) {}

  // colour maths: keep every chosen colour readable
  function hsl(h, s, l) { s /= 100; l /= 100; var a = s * Math.min(l, 1 - l); function f(n) { var k = (n + h / 30) % 12; return l - a * Math.max(-1, Math.min(k - 3, 9 - k, 1)); } return [Math.round(f(0) * 255), Math.round(f(8) * 255), Math.round(f(4) * 255)]; }
  function hex(c) { return '#' + c.map(function (v) { return ('0' + v.toString(16)).slice(-2); }).join(''); }
  function lum(c) { var v = c.map(function (x) { x /= 255; return x <= 0.03928 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4); }); return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]; }
  function ratio(a, b) { var x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); }
  function tones(h) {
    return {
      light: { dark: false, bg: '#FAFAFA', surface: '#FFFFFF', s2: '#F1F3F5', fg: '#1A1A1A', dim: '#5F6368', line: '#E0E0E0' },
      paper: { dark: false, bg: '#F6F0E4', surface: '#FCF9F2', s2: '#EFE7D6', fg: '#241F17', dim: '#6B6355', line: '#E2D9C6' },
      mist: { dark: false, bg: '#E6E8EB', surface: '#F2F3F5', s2: '#DADDE1', fg: '#1F2328', dim: '#4F565E', line: '#CDD1D6' },
      charcoal: { dark: true, bg: '#26282B', surface: '#2F3236', s2: '#393D42', fg: '#F2F2F2', dim: '#B0B5BB', line: '#43474D' },
      dusk: { dark: true, bg: hex(hsl(h, 20, 9)), surface: hex(hsl(h, 18, 13)), s2: hex(hsl(h, 16, 18)), fg: '#F2F2F2', dim: '#A3A8AE', line: hex(hsl(h, 14, 22)) },
      black: { dark: true, bg: '#000000', surface: '#111111', s2: '#1B1B1B', fg: '#F2F2F2', dim: '#A3A8AE', line: '#2A2A2A' }
    };
  }
  function rgb(h) { return [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)]; }
  function mix(a, b, t) { return a.map(function (v, i) { return Math.round(v + (b[i] - v) * t); }); }
  // text colour: a soft tint, pushed lighter (dark pages) or darker (light pages) until it reads clearly
  function textColour(key, T) {
    var bgc = rgb(T.bg), fg = rgb(T.fg), t = THUE[key], c = fg, l, k;
    if (t) { if (T.dark) { for (l = 92; l < 99; l += 1) { c = hsl(t[0], t[1], l); if (ratio(c, bgc) >= 9) break; } } else { for (l = 22; l > 6; l -= 1) { c = hsl(t[0], t[1] * 0.8, l); if (ratio(c, bgc) >= 9) break; } } }
    var dim = c; for (k = 0.45; k >= 0.1; k -= 0.05) { dim = mix(c, bgc, k); if (ratio(dim, bgc) >= 4.8) break; }
    return { fg: hex(c), dim: hex(dim) };
  }
  function build(h, tone, text) {
    var T = tones(h)[tone], bg = T.bg, bgc = [parseInt(bg.slice(1, 3), 16), parseInt(bg.slice(3, 5), 16), parseInt(bg.slice(5, 7), 16)], l, acc, p = {};
    if (!T.dark) { for (l = 46; l > 20; l -= 2) { acc = hsl(h, 70, l); if (ratio(acc, bgc) >= 4.6) break; } p['--sky'] = hex(acc); p['--on-sky'] = '#FFFFFF'; p['--sky-ink'] = hex(hsl(h, 70, l - 6)); p['--sky-tint'] = hex(hsl(h, 70, 94)); p['--sheen'] = 'linear-gradient(135deg,' + hex(hsl(h, 70, l + 10)) + ' 0%,' + hex(acc) + ' 55%,' + hex(hsl(h, 70, l - 6)) + ' 100%)'; }
    else { for (l = 70; l < 92; l += 2) { acc = hsl(h, 85, l); if (ratio(acc, bgc) >= 6) break; } p['--sky'] = hex(acc); p['--on-sky'] = hex(hsl(h, 60, 10)); p['--sky-ink'] = hex(acc); p['--sky-tint'] = 'rgba(' + acc.join(',') + ',0.16)'; p['--sheen'] = 'linear-gradient(135deg,' + hex(hsl(h, 85, Math.min(l + 8, 95))) + ' 0%,' + hex(acc) + ' 55%,' + hex(hsl(h, 80, l - 10)) + ' 100%)'; }
    p['--bg'] = T.bg; p['--surface'] = T.surface; p['--surface-2'] = T.s2; var tc = textColour(text || 'default', T); if (!text || text === 'default') tc = { fg: T.fg, dim: T.dim }; p['--fg'] = tc.fg; p['--fg-dim'] = tc.dim; p['--line'] = T.line; p['--scrim'] = T.dark ? 'rgba(0,0,0,0.7)' : 'rgba(10,10,10,0.55)';
    return { dark: T.dark, vars: p, bg: T.bg, surface: T.surface, accent: hex(acc), fg: tc.fg };
  }
  var PROPS = ['--sky', '--on-sky', '--sky-ink', '--sky-tint', '--sheen', '--bg', '--surface', '--surface-2', '--fg', '--fg-dim', '--line', '--scrim'];
  function preview(tile, b) { tile.style.setProperty('--pv-bg', b.bg); tile.style.setProperty('--pv-surface', b.surface); tile.style.setProperty('--pv-accent', b.accent); tile.style.setProperty('--pv-fg', b.fg); }

  function apply() {
    var x = SCHEMES.filter(function (y) { return y.id === cur; })[0];
    PROPS.forEach(function (n) { root.style.removeProperty(n); });
    var theme = x.theme;
    if (cur === 'mine') { var b = build(mine.hue, mine.tone, mine.text); PROPS.forEach(function (n) { root.style.setProperty(n, b.vars[n]); }); theme = b.dark ? 'dark' : 'light'; }
    [['theme', theme], ['palette', x.palette], ['accent', x.accent]].forEach(function (p) { if (p[1]) root.dataset[p[0]] = p[1]; else root.removeAttribute('data-' + p[0]); });
    try { localStorage.setItem(KEY, cur); localStorage.setItem(MKEY, JSON.stringify(mine)); } catch (e) {}
    document.querySelectorAll('.look-tile').forEach(function (t) { t.setAttribute('aria-pressed', t.dataset.id === cur); });
    paintTray();
  }
  var host = document.getElementById('screen-index'), tray, mineTile;
  function paintTray() {
    if (!tray) return;
    tray.querySelectorAll('.look-hue').forEach(function (b) { b.setAttribute('aria-pressed', +b.dataset.hue === mine.hue); });
    tray.querySelectorAll('.look-tone').forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.tone === mine.tone); preview(b, build(mine.hue, b.dataset.tone, mine.text)); });
    tray.querySelectorAll('.look-text').forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.text === mine.text); preview(b, build(mine.hue, mine.tone, b.dataset.text)); });
    preview(mineTile, build(mine.hue, mine.tone, mine.text));
  }
  if (host) {
    var panel = document.createElement('div'); panel.className = 'look-panel';
    tray = document.createElement('div'); tray.className = 'look-tray'; tray.hidden = true;
    var pv = document.createElement('div'); pv.className = 'look-preview'; pv.setAttribute('aria-hidden', 'true'); pv.innerHTML = '<span class="pv-pill"></span><span class="pv-ring"></span><span class="pv-line a"></span><span class="pv-line f"></span><span class="pv-line s"></span>';
    var r1 = document.createElement('div'); r1.className = 'look-line'; r1.innerHTML = '<span class="look-rowic page"></span>';
    var r3 = document.createElement('div'); r3.className = 'look-line'; r3.innerHTML = '<span class="look-rowic text"></span>';
    var tx = document.createElement('div'); tx.className = 'look-opts';
    TEXTS.forEach(function (t) { var b = document.createElement('button'); b.type = 'button'; b.className = 'look-tile look-text'; b.dataset.text = t; b.setAttribute('aria-label', 'Text ' + t); tx.appendChild(b); });
    r3.appendChild(tx);
    var r2 = document.createElement('div'); r2.className = 'look-line'; r2.innerHTML = '<span class="look-rowic brush"></span>';
    var hr = document.createElement('div'); hr.className = 'look-opts look-hues';
    HUES.forEach(function (h) { var b = document.createElement('button'); b.type = 'button'; b.className = 'look-hue'; b.dataset.hue = h; b.setAttribute('aria-label', 'Colour'); b.style.background = hex(hsl(h, 70, 50)); hr.appendChild(b); });
    var tr = document.createElement('div'); tr.className = 'look-opts look-tones';
    TONES.forEach(function (t) { var b = document.createElement('button'); b.type = 'button'; b.className = 'look-tile look-tone'; b.dataset.tone = t; b.setAttribute('aria-label', 'Page ' + t); tr.appendChild(b); });
    r1.appendChild(tr); r2.appendChild(hr); tray.appendChild(pv); tray.appendChild(r1); tray.appendChild(r2); tray.appendChild(r3);
    var main = document.createElement('div'); main.className = 'look-main';
    var ic = document.createElement('span'); ic.className = 'look-ic'; ic.setAttribute('aria-hidden', 'true');
    var strip = document.createElement('div'); strip.className = 'look-strip'; strip.setAttribute('role', 'group'); strip.setAttribute('aria-label', 'Colours');
    SCHEMES.forEach(function (x) { if (x.hidden) return; var b = document.createElement('button'); b.type = 'button'; b.className = 'look-tile' + (x.id === 'auto' ? ' auto' : '') + (x.id === 'mine' ? ' mine' : ''); b.dataset.id = x.id; b.setAttribute('aria-label', x.label); if (x.id === 'mine') mineTile = b; strip.appendChild(b); });
    strip.addEventListener('click', function (e) {
      var b = e.target.closest('.look-tile'); if (!b) return;
      if (b.dataset.id === 'mine') { if (cur === 'mine') tray.hidden = !tray.hidden; else { cur = 'mine'; tray.hidden = false; apply(); } return; }
      tray.hidden = true; cur = b.dataset.id; apply();
    });
    tray.addEventListener('click', function (e) { var b = e.target.closest('button'); if (!b) return; if (b.dataset.hue) mine.hue = +b.dataset.hue; if (b.dataset.tone) mine.tone = b.dataset.tone; if (b.dataset.text) mine.text = b.dataset.text; cur = 'mine'; apply(); });
    main.appendChild(ic); main.appendChild(strip); panel.appendChild(tray); panel.appendChild(main); host.appendChild(panel);
  }
  apply();
})();

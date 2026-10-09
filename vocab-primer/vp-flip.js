/* Flip card: tap the picture, it turns over to a short animation. No autoplay; the learner starts it.
   FlipCard.attach(frame, clip, group): frame is the square picture box; clip is {sources:[{src,type}], title} or null.
   Cards in one group never play at the same time. Player code only calls attach(). */
(function () {
  var LABEL = { show: 'Show animation', back: 'Back to the picture', play: 'Play', pause: 'Pause', replay: 'Play again', seek: 'Position' };
  var all = [];

  function el(tag, cls, attrs) {
    var e = document.createElement(tag); if (cls) e.className = cls;
    if (attrs) for (var k in attrs) e.setAttribute(k, attrs[k]);
    return e;
  }
  function icon(name) { var i = el('span', 'fc-ic'); i.style.setProperty('--ic', 'var(--ic-' + name + ')'); i.setAttribute('aria-hidden', 'true'); return i; }

  function build(frame) {
    var inner = el('div', 'flip-inner');
    var front = el('div', 'flip-face front');
    while (frame.firstChild) front.appendChild(frame.firstChild);
    var back = el('div', 'flip-face back');
    var video = el('video', 'flip-video', { playsinline: '', preload: 'metadata' });
    var bar = el('div', 'flip-bar');
    var play = el('button', 'flip-btn', { type: 'button' }); play.appendChild(icon('play'));
    var turn = el('button', 'flip-btn plain', { type: 'button', 'aria-label': LABEL.back }); turn.appendChild(icon('flip'));
    bar.appendChild(play); bar.appendChild(turn);
    back.appendChild(video);
    inner.appendChild(front); inner.appendChild(back); frame.appendChild(inner);
    // Under the frame, like the audio and translate buttons under text: the hint on the picture side, the controls once turned
    var show = el('button', 'flip-btn plain flip-show', { type: 'button', 'aria-label': LABEL.show }); show.appendChild(icon('flip'));
    var slot = el('div', 'flip-slot'); slot.appendChild(show); slot.appendChild(bar);
    bar.classList.add('away'); bar.inert = true;
    frame.insertAdjacentElement('afterend', slot);
    return { slot: slot, bar: bar, inner: inner, front: front, back: back, video: video, play: play, turn: turn, show: show };
  }

  function attach(frame, clip, group) {
    var inst = frame._flip;
    if (!inst) {
      inst = frame._flip = { frame: frame, group: group || 'default', parts: build(frame), on: false, flipped: false };
      all.push(inst);
      wire(inst);
    }
    inst.group = group || inst.group;
    setClip(inst, clip);
    return inst;
  }

  function setClip(inst, clip) {
    var p = inst.parts, v = p.video;
    flip(inst, false, true);
    v.pause();
    while (v.firstChild) v.removeChild(v.firstChild);
    inst.on = !!(clip && clip.sources && clip.sources.length);
    inst.frame.classList.toggle('flip', inst.on);
    p.slot.hidden = !inst.on;
    if (clip && clip.title) v.setAttribute('aria-label', clip.title); else v.removeAttribute('aria-label');
    if (!inst.on) { v.removeAttribute('src'); v.load(); return; }
    clip.sources.forEach(function (s) { var so = el('source', null, { src: s.src }); if (s.type) so.type = s.type; v.appendChild(so); });
    v.load();
    syncPlay(inst);
    p.front.setAttribute('role', 'button'); p.front.tabIndex = 0; p.front.setAttribute('aria-label', LABEL.show);
  }

  function syncPlay(inst) {
    var v = inst.parts.video, ended = v.ended, playing = !v.paused && !ended;
    var name = ended ? 'replay' : playing ? 'pause' : 'play';
    inst.parts.play.firstChild.style.setProperty('--ic', 'var(--ic-' + name + ')');
    inst.parts.play.setAttribute('aria-label', LABEL[name]);
    inst.parts.play.classList.toggle('on', playing);
  }

  function flip(inst, to, silent) {
    if (!inst.on && to) return;
    if (inst.flipped === to && !silent) return;
    inst.flipped = to;
    var p = inst.parts;
    inst.frame.classList.toggle('is-flipped', to);
    p.front.inert = to; p.back.inert = !to;
    p.show.classList.toggle('away', to); p.show.inert = to;
    p.bar.classList.toggle('away', !to); p.bar.inert = !to;
    if (!to) { p.video.pause(); try { p.video.currentTime = 0; } catch (e) {} syncPlay(inst); }
    if (to) {
      // Flipping a second card only pauses the first one's video; it stays turned until the student taps it
      pauseOthers(inst);
      p.play.focus({ preventScroll: true });
    }
  }

  function pauseOthers(inst) {
    all.forEach(function (o) { if (o !== inst && o.group === inst.group && !o.parts.video.paused) { o.parts.video.pause(); syncPlay(o); } });
  }

  function toggleVideo(inst) {
    var v = inst.parts.video;
    if (v.ended) { v.currentTime = 0; }
    if (v.paused) { pauseOthers(inst); var pr = v.play(); if (pr && pr.catch) pr.catch(function () {}); } else v.pause();
  }

  function wire(inst) {
    var p = inst.parts;
    p.show.addEventListener('click', function () { flip(inst, true); });
    p.turn.addEventListener('click', function () { flip(inst, false); p.show.focus({ preventScroll: true }); });
    p.front.addEventListener('click', function () { flip(inst, true); });
    p.front.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); flip(inst, true); } });
    p.video.setAttribute('role', 'button'); p.video.tabIndex = 0;
    p.video.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); flip(inst, false); p.front.focus({ preventScroll: true }); } });
    p.play.addEventListener('click', function () { toggleVideo(inst); });
    // Tapping the video turns the card back to the picture, mirroring the tap that turned it over. Playback uses the controls.
    p.video.setAttribute('aria-label', LABEL.back);
    p.video.addEventListener('click', function () { flip(inst, false); p.front.focus({ preventScroll: true }); });
    ['play', 'pause', 'ended', 'loadedmetadata'].forEach(function (n) { p.video.addEventListener(n, function () { syncPlay(inst); }); });
    p.back.inert = true;
  }

  // Stop any clip when its screen is left or the tab is hidden
  function pauseAll() { all.forEach(function (i) { if (i.parts.video && !i.parts.video.paused) { i.parts.video.pause(); syncPlay(i); } }); }
  document.addEventListener('visibilitychange', function () { if (document.hidden) pauseAll(); });
  new MutationObserver(function () {
    all = all.filter(function (i) { return i.frame.isConnected; });
    all.forEach(function (i) { var s = i.frame.closest('.screen'); if (s && !s.classList.contains('active')) { flip(i, false); } });
  }).observe(document.documentElement, { subtree: true, attributes: true, attributeFilter: ['class'] });

  window.FlipCard = { attach: attach, pauseAll: pauseAll };
})();

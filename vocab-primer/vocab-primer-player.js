
/* ═══════════════════════════════════════════════════
   DECK DATA
   Each card:
   {
     type: 'single' | 'pair',
     tier: 'bronze' | 'silver' | 'gold',
     // single:
     word, emoji, image(url), illustration(url opt),
     sentence, sentenceAudio(url), wordAudio(url),
     phonemes: [{symbol, audio}],
     video: {url, title, subtitle} (opt),
     // pair: word1, word2, emoji1, emoji2, image1, image2,
     //   sentence1, sentence2, phonemes1, phonemes2,
     //   wordAudio1, wordAudio2, sentenceAudio1, sentenceAudio2,
     //   video1 (opt), video2 (opt)
   }
═══════════════════════════════════════════════════ */
/* ═══════════════════════════════════════════════════
   RUNTIME DECK LOADING
   Lesson shell sets DECK_URL before this script loads.
═══════════════════════════════════════════════════ */
let DECK = null;

function initPlayer() {
  STORAGE_KEY = 'vp_progress_' + DECK.lessonName.replace(/\s+/g, '_');
  init();
  const ov = document.getElementById('loading-overlay');
  if (ov) { ov.classList.add('hidden'); setTimeout(() => ov.remove(), 500); }
}

async function loadDeck() {
  const overlay = document.getElementById('loading-overlay');
  const label   = document.getElementById('loading-label');
  const bar     = document.getElementById('loading-bar-fill');
  function setLoad(pct, txt) {
    if (bar)   bar.style.width = pct + '%';
    if (label) label.textContent = txt;
  }
  try {
    setLoad(20, 'Fetching deck…');
    const res = await fetch(DECK_URL);
    if (!res.ok) throw new Error('HTTP ' + res.status);
    setLoad(60, 'Parsing…');
    DECK = await res.json();
    setLoad(90, 'Building cards…');
  } catch (e) {
    if (overlay) overlay.innerHTML =
      '<div style="color:#e05c5c;font-family:Inter,sans-serif;padding:32px;text-align:center;line-height:1.8">'
      + '⚠️ Could not load deck.<br><small style="opacity:.55">' + e.message + '</small></div>';
    return;
  }
  initPlayer();
}

/* ═══════════════════════════════════════════════
   STATE
═══════════════════════════════════════════════ */
let STORAGE_KEY;  // assigned in initPlayer() after DECK loads
let progress = {};   // cardKey → 'got-it' | 'practicing'
let currentSingleIdx = 0;  // index into singleCards array
let currentPairIdx   = 0;  // index into pairCards array
let singleCards = [];
let pairCards   = [];
let navOrder    = [];   // all cards in deck order for sequential nav
let currentNavIdx = 0;
let currentVideoData = null;
let activeTranslationLang = null; // null = hidden; 'vi'|'km'|'ur'|'th' = active
let mediaRecorder = null;
let recordedChunks = [];
let recordedBlob   = null;
let recordingActive = false;

function cardKey(card, side) {
  if (card.type === 'single') return 'single_' + card.word;
  return 'pair_' + card.word1 + '_' + (side || 'both');
}

function loadProgress() {
  try { progress = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}'); }
  catch(e) { progress = {}; }
}
function saveProgress() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
}

/* ═══════════════════════════════════════════════
   INIT
═══════════════════════════════════════════════ */
function init() {
  loadProgress();
  document.getElementById('idx-lesson-name').textContent = DECK.lessonName;
  pairCards   = DECK.cards.filter(c => c.type === 'pair');
  singleCards = DECK.cards.filter(c => c.type === 'single');
  navOrder    = DECK.cards.slice(); // deck order — category-grouped
  applyTierColours();
  buildGrid();
  updateProgress();
}

/* Apply tierColours from deck JSON to CSS variables */
function applyTierColours() {
  const tc = DECK.tierColours;
  if (!tc) return;
  const root = document.documentElement;
  if (tc.bronze) root.style.setProperty('--tier-bronze', tc.bronze);
  if (tc.silver) root.style.setProperty('--tier-silver', tc.silver);
  if (tc.gold)   root.style.setProperty('--tier-gold',   tc.gold);
}

/* ═══════════════════════════════════════════════
   GRID BUILD
   Groups ALL cards (pairs + singles) by category,
   in DECK.categories[] order. Backwards compatible
   with old decks (Opposite Pairs / Nouns / Shapes / Colours).
═══════════════════════════════════════════════ */
function buildGrid() {
  const grid = document.getElementById('card-grid');
  grid.innerHTML = '';

  const allCards = DECK.cards;

  // Resolve category — use card.category if set, else legacy fallback
  function resolveCategory(card) {
    if (card.category) return card.category;
    if (card.type === 'pair') return 'Opposite Pairs';
    if (card.isColour) return 'Colours';
    if (['circle','rectangle','triangle','square'].includes(card.word)) return 'Shapes';
    return 'Nouns';
  }

  // Category order — use DECK.categories if present, else legacy auto-detect
  const deckCats = (DECK.categories && DECK.categories.length)
    ? DECK.categories
    : (() => {
        const AUTO = ['Opposite Pairs','Nouns','Shapes','Colours'];
        const seen = new Set(allCards.map(c => resolveCategory(c)));
        return AUTO.filter(g => seen.has(g));
      })();

  const rendered = new Set();

  deckCats.forEach(label => {
    const groupCards = allCards.filter(c => resolveCategory(c) === label);
    if (!groupCards.length) return;

    // Category header — collapsible, starts collapsed
    let collapsed = true;
    const body = [];

    const header = document.createElement('div');
    header.className = 'cat-group-header';
    header.innerHTML = `<span class="cat-group-toggle">▶</span><span class="cat-group-label">${label}</span><span class="cat-group-count">${groupCards.length}</span>`;
    header.onclick = () => {
      collapsed = !collapsed;
      header.querySelector('.cat-group-toggle').textContent = collapsed ? '▶' : '▼';
      body.forEach(el => { el.style.display = collapsed ? 'none' : ''; });
    };
    grid.appendChild(header);

    groupCards.forEach(card => {
      rendered.add(card);
      let el;
      if (card.type === 'pair') {
        el = buildPairGridCard(card, pairCards.indexOf(card));
      } else {
        el = buildSingleGridCard(card, singleCards.indexOf(card));
      }
      el.style.display = 'none'; // start collapsed
      grid.appendChild(el);
      body.push(el);
    });
  });

  // Safety net — uncategorised cards shown in Other
  const uncategorised = allCards.filter(c => !rendered.has(c));
  if (uncategorised.length) {
    let collapsed = false;
    const body = [];
    const header = document.createElement('div');
    header.className = 'cat-group-header';
    header.innerHTML = `<span class="cat-group-toggle">▼</span><span class="cat-group-label">Other</span><span class="cat-group-count">${uncategorised.length}</span>`;
    header.onclick = () => {
      collapsed = !collapsed;
      header.querySelector('.cat-group-toggle').textContent = collapsed ? '▶' : '▼';
      body.forEach(el => { el.style.display = collapsed ? 'none' : ''; });
    };
    grid.appendChild(header);
    uncategorised.forEach(card => {
      let el;
      if (card.type === 'pair') {
        el = buildPairGridCard(card, pairCards.indexOf(card));
      } else {
        el = buildSingleGridCard(card, singleCards.indexOf(card));
      }
      grid.appendChild(el);
      body.push(el);
    });
  }
}

function dotClass(key) {
  const s = progress[key];
  if (s === 'got-it')     return 'gc-dot done';
  if (s === 'practicing') return 'gc-dot practicing';
  if (s === 'seen')       return 'gc-dot seen';
  return 'gc-dot';
}
function pairDotClass(card) {
  const k1 = 'pair_' + card.word1 + '_word1';
  const k2 = 'pair_' + card.word2 + '_word2';
  const s1 = progress[k1], s2 = progress[k2];
  if (s1 === 'got-it' && s2 === 'got-it') return 'gc-dot done';
  if (s1 || s2) {
    if (s1 === 'seen' && (!s2 || s2 === 'seen')) return 'gc-dot seen';
    return 'gc-dot practicing';
  }
  return 'gc-dot';
}

function buildSingleGridCard(card, i) {
  const el = document.createElement('div');
  const rating = progress[cardKey(card)] || '';
  el.dataset.tier = card.tier;
  el.className = 'gc'
    + (rating === 'got-it'     ? ' done-card'     : '')
    + (rating === 'practicing' ? ' practice-card' : '')
    + (rating === 'seen'       ? ' seen-card'      : '');
  el.onclick = () => openSingle(i);
  el.innerHTML = `
    <div class="${dotClass(cardKey(card))}"></div>
    <div class="gc-label">
      <span class="gc-word">${card.word}</span>
      <div style="display:flex;align-items:center;gap:6px;">
        ${card.video ? `<span class="gc-video-pip">🎬</span>` : ''}
      </div>
    </div>`;
  return el;
}

function buildPairGridCard(card, i) {
  const el = document.createElement('div');
  const hasVideo = card.video1 || card.video2;
  const dot = pairDotClass(card);
  el.dataset.tier = card.tier;
  el.className = 'gc pair'
    + (dot.includes('done')       ? ' done-card'     : '')
    + (dot.includes('practicing') ? ' practice-card' : '')
    + (dot.includes('seen')       ? ' seen-card'      : '');
  el.onclick = () => openPair(i);
  el.innerHTML = `
    <div class="${dot}" style="z-index:4"></div>
    <div class="pair-cols">
      <div class="pair-col">
        <div class="pair-col-word">${card.word1}</div>
      </div>
      <div class="pair-col">
        <div class="pair-col-word">${card.word2}</div>
      </div>
    </div>
    <div class="pair-footer">
      <span class="pair-footer-vs">opposite</span>
      ${hasVideo ? `<span class="pair-footer-video">🎬</span>` : ''}
    </div>`;
  return el;
}

/* ═══════════════════════════════════════════════
   PROGRESS
═══════════════════════════════════════════════ */
function updateProgress() {
  const total    = singleCards.length + (pairCards.length * 2);
  const done     = Object.values(progress).filter(v => v === 'got-it').length;
  const seen     = Object.values(progress).filter(v => v === 'seen').length;
  const pct      = total > 0 ? Math.round((done / total) * 100) : 0;
  document.getElementById('prog-fill').style.width = pct + '%';
  const seenNote = seen > 0 ? ` · ${seen} seen` : '';
  document.getElementById('prog-count').textContent = done + ' of ' + total + ' confident' + seenNote;
}

/* ═══════════════════════════════════════════════
   TRANSLATIONS
═══════════════════════════════════════════════ */
const LANG_META = {
  vi: { flag: '🇻🇳', name: 'Vietnamese', dir: 'ltr' },
  km: { flag: '🇰🇭', name: 'Khmer',      dir: 'ltr' },
  ur: { flag: '🇵🇰', name: 'Urdu',       dir: 'rtl' },
  th: { flag: '🇹🇭', name: 'Thai',       dir: 'ltr' },
};

function getAvailableTranslations(card) {
  // Returns array of lang codes that have at least a word translation.
  // Pairs use translationVi1 / translationVi2; singles use translationVi.
  return ['vi','km','ur','th'].filter(lang => {
    const cap = lang.charAt(0).toUpperCase() + lang.slice(1);
    const key = 'translation' + cap;
    return (card[key] && card[key].trim())       // single card
        || (card[key+'1'] && card[key+'1'].trim()) // pair card word1
        || (card[key+'2'] && card[key+'2'].trim()); // pair card word2
  });
}

function buildTranslateDropdown(card, containerEl) {
  const langs = getAvailableTranslations(card);
  if (!langs.length) { containerEl.style.display = 'none'; return; }
  containerEl.style.display = '';

  const active = activeTranslationLang;
  const activeMeta = active ? LANG_META[active] : null;

  // Inline flag picker — always visible when langs exist
  const pills = langs.map(lang => {
    const m = LANG_META[lang];
    const isActive = lang === active;
    return `<button class="tr-flag-pill${isActive ? ' active' : ''}"
      onclick="selectTranslationLang('${lang}',event)"
      title="${m.name}">${m.flag} ${m.name}</button>`;
  }).join('');

  containerEl.innerHTML = `
    <div class="tr-picker-row">
      <span class="tr-picker-label">🌐</span>
      ${pills}
      ${active ? `<button class="tr-flag-pill dismiss" onclick="selectTranslationLang('${active}',event)" title="Hide translation">✕</button>` : ''}
    </div>`;
}

function toggleTranslateMenu(e) {
  // kept for back-compat — no longer used
}

function selectTranslationLang(lang, e) {
  e && e.stopPropagation();
  // Toggle off if already active
  activeTranslationLang = (activeTranslationLang === lang) ? null : lang;
  // Re-render the current card to apply/remove translation
  const screen = document.querySelector('.screen.active');
  if (screen && screen.id === 'screen-single') renderSingle();
  else if (screen && screen.id === 'screen-pair') renderPair();
}

function applyTranslationToSingle(card) {
  const lang = activeTranslationLang;
  const wordEl = document.getElementById('sc-word');
  const sentEl = document.getElementById('sc-sentence');
  if (!wordEl || !sentEl) return;

  // Remove any existing translation nodes
  document.querySelectorAll('.sc-word-translation, .sc-sent-translation, .sc-sent-sep').forEach(el => el.remove());

  if (!lang) return;

  const langCap = lang.charAt(0).toUpperCase() + lang.slice(1);
  const wordTr  = card['translation' + langCap] || '';
  const sentTr  = card['sentence'    + langCap] || card['sentence' + langCap + '1'] || '';
  const meta    = LANG_META[lang];
  const isRTL   = meta.dir === 'rtl';

  if (wordTr) {
    const el = document.createElement('div');
    el.className = 'sc-word-translation';
    el.textContent = wordTr;
    if (isRTL) { el.setAttribute('dir','rtl'); el.style.textAlign = 'right'; }
    wordEl.insertAdjacentElement('afterend', el);
  }
  if (sentTr) {
    const sep = document.createElement('hr');
    sep.className = 'sc-sent-sep';
    const el = document.createElement('div');
    el.className = 'sc-sent-translation';
    el.textContent = sentTr;
    if (isRTL) { el.setAttribute('dir','rtl'); el.style.textAlign = 'right'; }
    sentEl.insertAdjacentElement('afterend', sep);
    sep.insertAdjacentElement('afterend', el);
  }
}

function applyTranslationToPairHalf(card, side, halfEl) {
  const lang = activeTranslationLang;
  // Remove existing translation nodes in this half
  halfEl.querySelectorAll('.pair-word-translation, .pair-sent-translation, .pair-sent-sep').forEach(el => el.remove());
  if (!lang) return;

  const langCap = lang.charAt(0).toUpperCase() + lang.slice(1);
  const sideSuffix = side; // '1' or '2'
  const wordTr  = card['translation' + langCap + sideSuffix] || card['translation' + langCap] || '';
  const sentTr  = card['sentence'    + langCap + sideSuffix] || '';
  const meta    = LANG_META[lang];
  const isRTL   = meta.dir === 'rtl';

  const wordEl = halfEl.querySelector('.pair-word-text');
  const sentEl = halfEl.querySelector('.pair-sentence');

  if (wordTr && wordEl) {
    const el = document.createElement('div');
    el.className = 'pair-word-translation';
    el.textContent = wordTr;
    if (isRTL) { el.setAttribute('dir','rtl'); el.style.textAlign = 'right'; }
    wordEl.insertAdjacentElement('afterend', el);
  }
  if (sentTr && sentEl) {
    const sep = document.createElement('hr');
    sep.className = 'pair-sent-sep';
    const el = document.createElement('div');
    el.className = 'pair-sent-translation';
    el.textContent = sentTr;
    if (isRTL) { el.setAttribute('dir','rtl'); el.style.textAlign = 'right'; }
    sentEl.insertAdjacentElement('afterend', sep);
    sep.insertAdjacentElement('afterend', el);
  }
}

/* ═══════════════════════════════════════════════
   SINGLE CARD
═══════════════════════════════════════════════ */
function openSingle(i) {
  currentSingleIdx = i;
  currentNavIdx = navOrder.indexOf(singleCards[i]);
  activeTranslationLang = null;
  // Mark as seen if not yet rated
  const k = cardKey(singleCards[i]);
  if (!progress[k]) { progress[k] = 'seen'; saveProgress(); }
  renderSingle();
  showScreen('screen-single');
}

function renderSingle() {
  const card = singleCards[currentSingleIdx];
  const i    = currentSingleIdx;
  const tot  = singleCards.length;

  document.getElementById('sc-counter').textContent = `${i+1} of ${tot}`;
  document.getElementById('sc-tier').className = 'nav-tier tier-' + card.tier;
  document.getElementById('sc-tier').textContent = card.tier.charAt(0).toUpperCase() + card.tier.slice(1);

  document.getElementById('sc-word').textContent = card.word;

  // Image — colour cards show CSS swatch
  const imgInner = document.getElementById('sc-img-inner');
  if (card.isColour) {
    imgInner.style.cssText = 'position:absolute;inset:0;border-radius:12px;';
    imgInner.style.background = card.swatch;
    imgInner.innerHTML = '';
  } else {
    imgInner.style.cssText = 'position:absolute;inset:0;display:flex;align-items:center;justify-content:center;';
    imgInner.innerHTML = card.image
      ? `<img src="${card.image}" alt="${card.word}" style="width:100%;height:100%;object-fit:cover;">`
      : `<span style="font-size:90px;">${card.emoji}</span>`;
  }

  // Video btn
  const vBtn = document.getElementById('sc-video-btn');
  if (card.video) {
    vBtn.style.display = '';
    currentVideoData = card.video;
  } else {
    vBtn.style.display = 'none';
    currentVideoData = null;
  }

  // Illustration toggle — tap image or button to flip between photo and illustration
  const ilToggle = document.getElementById('sc-illus-toggle');
  const ilLabel  = document.getElementById('sc-illus-label');
  const imgBlock = document.getElementById('sc-img-block');
  ilToggle.style.display = card.illustration ? '' : 'none';
  let showingIllus = false;

  function renderCardImg(illus) {
    const inner = document.getElementById('sc-img-inner');
    inner.style.cssText = 'position:absolute;inset:0;display:flex;align-items:center;justify-content:center;';
    const src = illus ? card.illustration : card.image;
    if (src) {
      inner.innerHTML = `<img src="${src}" alt="${card.word}" style="width:100%;height:100%;object-fit:${illus ? 'contain' : 'cover'};">`;
    } else {
      inner.innerHTML = `<span style="font-size:90px;">${card.emoji}</span>`;
    }
    ilLabel.textContent = illus ? 'Show photo' : 'Show illustration';
    imgBlock.style.cursor = card.illustration ? 'pointer' : '';
  }

  // Tap image to flip (if illustration exists)
  imgBlock.onclick = card.illustration ? () => {
    showingIllus = !showingIllus;
    renderCardImg(showingIllus);
  } : null;

  ilToggle.onclick = () => {
    showingIllus = !showingIllus;
    renderCardImg(showingIllus);
  };

  // Sentence
  const sentEl = document.getElementById('sc-sentence');
  sentEl.innerHTML = highlightWord(card.sentence, card.word);

  // Phonemes
  const phEl = document.getElementById('sc-phonemes');
  phEl.innerHTML = (card.phonemes || []).map((ph, pi) =>
    `<button class="ph-tile" onclick="this.classList.toggle('tapped');playPhoneme('${ph.s}','${ph.audio||''}')">
      ${ph.s}<div class="ph-sub">tap to hear</div>
    </button>`
  ).join('');

  // Translation dropdown
  const trContainer = document.getElementById('sc-translate-container');
  if (trContainer) buildTranslateDropdown(card, trContainer);
  applyTranslationToSingle(card);

  // Rating
  const key = cardKey(card);
  const rating = progress[key] || '';
  document.getElementById('sc-got-it').className     = 'rating-btn' + (rating === 'got-it' ? ' got-it' : '');
  document.getElementById('sc-practicing').className = 'rating-btn' + (rating === 'practicing' ? ' practicing' : '');

  // Arrows
  document.getElementById('sc-prev').disabled = (i === 0) && pairCards.length === 0;
  document.getElementById('sc-next').disabled = i === tot - 1;
  // Update prev label to hint when crossing to pairs
  const scPrev = document.getElementById('sc-prev');
  scPrev.textContent = (i === 0 && pairCards.length > 0) ? '< Pairs' : '< Prev';

  // Reset trio recorder
  resetSCTrio();
  // Wire buttons after DOM update
  setTimeout(wireSCTrio, 0);
  document.getElementById('sc-scroll').scrollTop = 0;
}

function stepCard(dir) { stepNav(dir); }

function rateCard(rating) {
  const card = singleCards[currentSingleIdx];
  const key  = cardKey(card);
  progress[key] = rating;
  saveProgress();
  document.getElementById('sc-got-it').className     = 'rating-btn' + (rating === 'got-it' ? ' got-it' : '');
  document.getElementById('sc-practicing').className = 'rating-btn' + (rating === 'practicing' ? ' practicing' : '');
  buildGrid();
  updateProgress();
}

/* ═══════════════════════════════════════════════
   PAIR CARD
═══════════════════════════════════════════════ */
function openPair(i) {
  currentPairIdx = i;
  currentNavIdx = navOrder.indexOf(pairCards[i]);
  activeTranslationLang = null;
  // Mark both words as seen if not yet rated
  const card = pairCards[i];
  const k1 = `pair_${card.word1}_word1`, k2 = `pair_${card.word2}_word2`;
  let changed = false;
  if (!progress[k1]) { progress[k1] = 'seen'; changed = true; }
  if (!progress[k2]) { progress[k2] = 'seen'; changed = true; }
  if (changed) saveProgress();
  renderPair();
  showScreen('screen-pair');
}

function renderPair() {
  const card = pairCards[currentPairIdx];
  const i    = currentPairIdx;
  const tot  = pairCards.length;

  document.getElementById('pc-counter').textContent = `Pair ${i+1} of ${tot}`;
  document.getElementById('pc-tier').className = 'nav-tier tier-' + card.tier;
  document.getElementById('pc-tier').textContent = card.tier.charAt(0).toUpperCase() + card.tier.slice(1);
  document.getElementById('pc-prev').disabled = currentNavIdx === 0;
  document.getElementById('pc-next').disabled = currentNavIdx === navOrder.length - 1;
  const pcNext = document.getElementById('pc-next');
  pcNext.textContent = 'Next >';

  const layout = document.getElementById('pair-card-layout');
  layout.innerHTML = buildPairHalfHTML(card, 1) + buildPairHalfHTML(card, 2);
  lazyLoadPairImages(layout, card);

  // Translation dropdown — inject before pair-card-layout (or use a wrapper container)
  const trPairContainer = document.getElementById('pc-translate-container');
  if (trPairContainer) buildTranslateDropdown(card, trPairContainer);
  // Apply translations to both halves
  const halves = layout.querySelectorAll('.pair-card-half');
  if (halves[0]) applyTranslationToPairHalf(card, '1', halves[0]);
  if (halves[1]) applyTranslationToPairHalf(card, '2', halves[1]);

  // Pre-load You buttons from history
  ['1','2'].forEach(side => {
    const word = pairCards[currentPairIdx]['word' + side];
    if (word) initPairYouBtn(word, side);
  });

  // Wire rating buttons
  layout.querySelectorAll('[data-rate]').forEach(btn => {
    btn.addEventListener('click', () => {
      const side   = btn.dataset.side;
      const rating = btn.dataset.rate;
      const key    = `pair_${card['word'+side]}_word${side}`;
      progress[key] = rating;
      saveProgress();
      const half = btn.closest('.pair-card-half');
      half.querySelectorAll('[data-rate]').forEach(b => {
        b.className = 'pair-rating-btn' + (b.dataset.rate === rating ? ' '+rating : '');
      });
      buildGrid();
      updateProgress();
    });
  });

  // Wire phoneme buttons
  layout.querySelectorAll('[data-phoneme]').forEach(btn => {
    btn.addEventListener('click', () => {
      btn.classList.toggle('pair-ph-tapped');
      playPhoneme(btn.dataset.phoneme, btn.dataset.audio || '');
    });
  });
}

function buildPairHalfHTML(card, side) {
  const word      = card['word'     + side];
  const emoji     = card['emoji'    + side];
  const image     = card['image'    + side];
  const sentence  = card['sentence' + side];
  const phonemes  = card['phonemes' + side] || [];
  const video     = card['video'    + side];
  const key       = `pair_${word}_word${side}`;
  const rating    = progress[key] || '';

  const imgId = `pair-img-${side}-${card.word1}`;
  const imgContent = image
    ? `<img id="${imgId}" alt="${word}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity 0.3s;">`
    : `<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:48px;">${emoji}</div>`;

  return `
  <div class="pair-card-half">
    <div class="pair-word-row">
      <div class="pair-word-text">${word}${card['word'+side+'note'] ? `<span style="font-size:9px;color:var(--cream-dim);font-family:'Inter',sans-serif;font-weight:400;margin-left:4px;">*</span>` : ''}</div>
      <button class="pair-word-audio" data-audio="${card['wordAudio'+side]||''}" data-tts="${qa(word)}" onclick="playAudio(this.dataset.audio,this.dataset.tts)">🔊</button>
    </div>
    <div class="pair-card-img-wrap"><div class="pair-card-img">${imgContent}</div></div>
    <div class="pair-sentence">
      <span class="pair-s-audio" data-audio="${card['sentenceAudio'+side]||''}" data-tts="${qa(sentence)}" onclick="playAudio(this.dataset.audio,this.dataset.tts)">🔊</span>
      <span>${highlightWord(sentence, word)}</span>
    </div>
    <div>
      <div class="slabel">Sounds</div>
      <div class="pair-phonemes">
        ${phonemes.map(ph => `<button class="pair-ph" data-phoneme="${ph.s}" data-audio="${ph.audio||''}">${ph.s}</button>`).join('')}
      </div>
    </div>
    <div class="trio-wrap" id="pair-wrap-${side}-${word}" style="padding:10px;margin-top:4px;">
      <div class="trio-row">
        <button class="trio-btn model" style="font-size:11px;"
          data-audio="${card['wordAudio'+side]||''}" data-tts="${qa(word)}"
          onclick="playAudio(this.dataset.audio,this.dataset.tts)">
          <span class="trio-icon">&#128266;</span><span class="trio-label">Model</span>
        </button>
        <button class="trio-btn playback" id="pair-you-${side}-${word}" style="font-size:11px;">
          <span class="trio-icon">&#9654;</span><span class="trio-label">You</span>
        </button>
        <button class="trio-btn record" id="pair-rec-${side}-${word}" style="font-size:11px;"
          onclick="togglePairRec(this,'${qa(word)}','${side}')">
          <span class="trio-icon" id="pair-ri-${side}-${word}">&#127908;</span>
          <span class="trio-label" id="pair-rl-${side}-${word}">Record</span>
        </button>
      </div>
      <p class="trio-hint" id="pair-hint-${side}-${word}" style="font-size:10px;margin-top:6px;">Hear the model, then record.</p>
      <div id="pair-hist-${side}-${word}"></div>
    </div>
    ${video ? `<button style="background:var(--coral-dim);border:1.5px solid var(--coral);border-radius:var(--rpill);padding:6px 12px;color:var(--coral);font-size:11px;font-weight:600;display:flex;align-items:center;gap:4px;" onclick="openVideoData(${JSON.stringify(video).replace(/"/g,'&quot;')})">🎬 ${video.title}</button>` : ''}
    <div class="pair-rating">
      <button class="pair-rating-btn${rating==='got-it'?' got-it':''}" data-rate="got-it" data-side="${side}">Got it</button>
      <button class="pair-rating-btn${rating==='practicing'?' practicing':''}" data-rate="practicing" data-side="${side}">Still practising</button>
    </div>
  </div>`;
}

function stepPair(dir) { stepNav(dir); }

/* ═══════════════════════════════════════════════
   UNIFIED NAVIGATION (deck order, category-aware)
═══════════════════════════════════════════════ */
function stepNav(dir) {
  const next = currentNavIdx + dir;
  if (next < 0 || next >= navOrder.length) return;
  currentNavIdx = next;
  const card = navOrder[currentNavIdx];
  if (card.type === 'pair') {
    currentPairIdx = pairCards.indexOf(card);
    renderPair();
    showScreen('screen-pair');
  } else {
    currentSingleIdx = singleCards.indexOf(card);
    renderSingle();
    showScreen('screen-single');
  }
}

/* ═══════════════════════════════════════════════
   AUDIO
═══════════════════════════════════════════════ */
/* Escape single quotes for safe use inside onclick='...' attributes */
function qa(str) { return str ? String(str).replace(/'/g, '&#39;') : ''; }

function playAudio(url, fallbackTTS) {
  if (url) {
    const a = new Audio(url);
    a.addEventListener('error', () => { if (fallbackTTS) speakTTS(fallbackTTS); });
    a.play().catch(() => {}); // swallow autoplay policy rejection
  } else if (fallbackTTS) {
    speakTTS(fallbackTTS);
  }
}

// Jolly Phonics grapheme → filename (same as shell PHONEME_FILE)
const PHONEME_FILE = {
  'c':'ck','k':'k','ck':'ck','g':'g','j':'j','qu':'qu',
  'x':'x','y':'y','z':'z','ng':'ng','sh':'sh','th':'thh',
  'ch':'ch','ai':'ai','ee':'ee','ie':'ie','oa':'oa',
  'oo':'ooo','or':'or','ur':'er','er':'er','ow':'ou','ou':'ou',
  'oi':'oi','ear':'ar','air':'ar','ar':'ar','ue':'ue','thh':'thh',
  // single letters that map directly
  'a':'a','b':'b','d':'d','e':'e','f':'f','h':'h','i':'i',
  'l':'l','m':'m','n':'n','o':'o','p':'p','r':'r','s':'s',
  't':'t','u':'u','v':'v','w':'w',
};

// IPA symbol → Jolly Phonics grapheme (for primer's IPA-keyed phonemes)
const IPA_TO_JP = {
  // vowels
  'æ':'a',    // CAT  → sound_a.mp3
  'ɑː':'ar',  // CAR  → sound_ar.mp3
  'ɒ':'o',    // LOT  → sound_o.mp3
  'ɔː':'or',  // CORN → sound_or.mp3
  'ə':'er',   // schwa → sound_er.mp3 (unstressed central, closer to 'butter' than 'egg')
  'ɛ':'e',    // BED/PEN/HEAVY → sound_e.mp3
  'əʊ':'oa',  // GOAT → sound_oa.mp3
  'eɪ':'ai',  // FACE → sound_ai.mp3
  'iː':'ee',  // FLEECE → sound_ee.mp3
  'ɪ':'i',    // KIT  → sound_i.mp3
  'i':'i',    // unstressed final (happy) → sound_i.mp3
  'uː':'ooo', // GOOSE (long) → sound_ooo.mp3
  'ʊ':'oo',   // FOOT (short) → sound_oo.mp3  ← was wrongly ooo
  'aɪ':'ie',  // PRICE → sound_ie.mp3
  'aʊ':'ou',  // MOUTH → sound_ou.mp3
  'ɔɪ':'oi',  // CHOICE → sound_oi.mp3
  'ɜː':'er',  // NURSE → sound_er.mp3
  'ʌ':'u',    // STRUT → sound_u.mp3
  'juː':'ue', // CUTE → sound_ue.mp3
  'eə':'ar',  // SQUARE → sound_ar.mp3 (closest)
  'ɪə':'er',  // NEAR → sound_er.mp3 (closer than ar)
  // consonants
  'b':'b','d':'d','f':'f','g':'g','h':'h','j':'j','k':'k',
  'l':'l','m':'m','n':'n','p':'p','r':'r','s':'s','t':'t',
  'v':'v','w':'w','x':'x','y':'y','z':'z',
  'tʃ':'ch','dʒ':'j','ŋ':'ng','ʃ':'sh','θ':'th','ð':'thh',
};

const PHONEME_TTS_FALLBACK = {
  'c':'cat','k':'kit','g':'got','j':'jam','qu':'quick',
  'x':'fox','y':'yes','z':'zip','ng':'ring',
};

// Module-level reference prevents GC killing short audio clips mid-play
// Phoneme queue — play tiles one at a time, queue next if busy
let _phAudio   = null;  // currently playing Audio object
let _phQueue   = [];    // pending {src, symbol, useJP} items
let _phPlaying = false;

function _phNext() {
  if (_phQueue.length === 0) { _phPlaying = false; _phAudio = null; return; }
  _phPlaying = true;
  const { src, symbol, useJP } = _phQueue.shift();
  const a = new Audio();
  _phAudio = a;
  let played = false;

  function doPlay() {
    if (played) return;
    played = true;
    a.play().catch(() => { _phPlaying = false; _phAudio = null; _phNext(); });
  }

  a.addEventListener('canplaythrough', doPlay, { once: true });
  a.addEventListener('ended', () => { _phPlaying = false; _phAudio = null; _phNext(); }, { once: true });
  a.addEventListener('error', () => {
    _phPlaying = false; _phAudio = null;
    if (useJP) {
      const grapheme = IPA_TO_JP[symbol] || symbol;
      speakTTS(PHONEME_TTS_FALLBACK[grapheme] || symbol);
    } else {
      _phNext();
    }
  }, { once: true });

  a.preload = 'auto';
  a.src = src;
  a.load();
  // Fallback: if canplaythrough never fires (cached file), play after 300ms
  setTimeout(() => doPlay(), 300);
}

function playPhoneme(symbol, customUrl) {
  const useJP = !customUrl;
  const src = useJP ? (() => {
    const grapheme = IPA_TO_JP[symbol] || symbol;
    const fileKey  = PHONEME_FILE[grapheme] || grapheme;
    return `https://redskin106.github.io/lesson-a/shell-v2/assets/phonemes/sound_${fileKey}.mp3`;
  })() : customUrl;

  _phQueue.push({ src, symbol, useJP });
  if (!_phPlaying) _phNext();
}

function speakTTS(text) {
  if (!text || !window.speechSynthesis) return;
  const utt = new SpeechSynthesisUtterance(text);
  utt.lang = 'en-GB'; utt.rate = 0.85;
  window.speechSynthesis.cancel();
  window.speechSynthesis.speak(utt);
}

/* ═══════════════════════════════════════════════
   RECORDER — full trio system
   Model / You / Re-record + compare card + history
═══════════════════════════════════════════════ */

// Per-word recording history — stored in localStorage
// key: 'vp_rec_{word}' → array of {ts, dataUrl} (last 3)
const REC_MAX = 3;

function recStorageKey(word) { return 'vp_rec_' + word; }

function loadRecHistory(word) {
  try { return JSON.parse(localStorage.getItem(recStorageKey(word)) || '[]'); }
  catch(e) { return []; }
}

function saveRecToHistory(word, blob) {
  return new Promise(resolve => {
    const reader = new FileReader();
    reader.onload = () => {
      let history = loadRecHistory(word);
      history.push({ ts: Date.now(), dataUrl: reader.result });
      if (history.length > REC_MAX) history = history.slice(-REC_MAX);
      localStorage.setItem(recStorageKey(word), JSON.stringify(history));
      resolve(history);
    };
    reader.readAsDataURL(blob);
  });
}

function timeAgo(ts) {
  const s = Math.floor((Date.now() - ts) / 1000);
  if (s < 60)   return 'just now';
  if (s < 3600) return Math.floor(s/60) + 'm ago';
  if (s < 86400) return Math.floor(s/3600) + 'h ago';
  return Math.floor(s/86400) + 'd ago';
}

// Single card trio state
let scModelAudio   = null;
let scModelPlaying = false;
let scSelfAudio    = null;
let scSelfPlaying  = false;
let scRecording    = false;
let scRecBlob      = null;
let scMediaRec     = null;
const scBlobMap    = {}; // word → latest Blob, survives card navigation

function resetSCTrio() {
  // Stop any active audio/recording
  if (scMediaRec && scRecording) { try { scMediaRec.stop(); } catch(e) {} }
  if (scModelAudio) { scModelAudio.pause(); scModelAudio = null; }
  if (scSelfAudio)  { scSelfAudio.pause();  scSelfAudio = null; }
  scModelPlaying = false; scSelfPlaying = false;
  scRecording = false; scRecBlob = null; scMediaRec = null;

  const modelBtn  = document.getElementById('sc-model-btn');
  const playBtn   = document.getElementById('sc-play-btn');
  const recBtn    = document.getElementById('sc-rec-btn');
  const recIcon   = document.getElementById('sc-rec-icon');
  const recLabel  = document.getElementById('sc-rec-label');
  const hint      = document.getElementById('sc-trio-hint');
  const compareCard = document.getElementById('sc-compare-card');
  const histWrap  = document.getElementById('sc-history-wrap');

  if (modelBtn) modelBtn.classList.remove('playing');
  if (playBtn)  { playBtn.classList.remove('ready','playing'); }
  if (recBtn)   { recBtn.classList.remove('recording'); }
  if (recIcon)  recIcon.textContent = '🎤';
  if (recLabel) recLabel.textContent = 'Record';
  if (hint)     hint.textContent = 'Hear the model, then record yourself.';
  if (compareCard) compareCard.style.display = 'none';

  // Render history + pre-load latest recording into You button
  if (histWrap) {
    const word = singleCards[currentSingleIdx]?.word;
    if (word) {
      renderRecHistory(word, histWrap);
      const hist = loadRecHistory(word);
      // Check in-memory map first (fastest, no conversion needed)
      if (scBlobMap[word]) {
        scRecBlob = scBlobMap[word];
        const pb = document.getElementById('sc-play-btn');
        const rl = document.getElementById('sc-rec-label');
        if (pb) pb.classList.add('ready');
        if (rl) rl.textContent = 'Re-record';
      } else if (hist.length) {
        // Fall back to localStorage — convert dataUrl → Blob
        try {
          const blob = dataUrlToBlob(hist[hist.length-1].dataUrl);
          scRecBlob = blob;
          scBlobMap[word] = blob;
          const pb = document.getElementById('sc-play-btn');
          const rl = document.getElementById('sc-rec-label');
          if (pb) pb.classList.add('ready');
          if (rl) rl.textContent = 'Re-record';
        } catch(e) { console.warn('Could not restore recording:', e); }
      }
    }
  }
}

function renderRecHistory(word, container) {
  const history = loadRecHistory(word);
  if (!history.length) { container.innerHTML = ''; return; }
  const reversed = history.slice().reverse();
  const bodyId = 'rh-body-' + word.replace(/[^a-z0-9]/gi, '_');
  container.innerHTML =
    '<div class="rec-history">' +
    '<button class="rec-history-toggle-btn" onclick="toggleRecHistory(\'' + bodyId + '\', this)">▶ ' + history.length + ' past recording' + (history.length > 1 ? 's' : '') + '</button>' +
    '<div class="rec-history-body" id="' + bodyId + '">' +
    reversed.map((r, i) =>
      '<div class="rec-history-row">' +
      '<span class="rec-history-num">' + (history.length - i) + '</span>' +
      '<span class="rec-history-time">' + timeAgo(r.ts) + '</span>' +
      '<button class="rec-history-play">&#9654;</button>' +
      '</div>'
    ).join('') +
    '</div></div>';
  const btns = container.querySelectorAll('.rec-history-play');
  reversed.forEach((r, i) => {
    if (btns[i]) btns[i].addEventListener('click', () => playDataUrl(r.dataUrl));
  });
}

function toggleRecHistory(bodyId, btn) {
  const body = document.getElementById(bodyId);
  if (!body) return;
  const open = body.classList.toggle('open');
  const count = body.querySelectorAll('.rec-history-row').length;
  btn.textContent = (open ? '▼ ' : '▶ ') + count + ' past recording' + (count > 1 ? 's' : '');
}

function playDataUrl(dataUrl) {
  new Audio(dataUrl).play().catch(() => {});
}

function dataUrlToBlob(dataUrl) {
  const [header, b64] = dataUrl.split(',');
  const mime = header.match(/:(.*?);/)[1];
  const bytes = atob(b64);
  const arr = new Uint8Array(bytes.length);
  for (let i = 0; i < bytes.length; i++) arr[i] = bytes.charCodeAt(i);
  return new Blob([arr], { type: mime });
}

// Wire trio buttons after DOM is ready
function wireSCTrio() {
  const modelBtn    = document.getElementById('sc-model-btn');
  const playBtn     = document.getElementById('sc-play-btn');
  const recBtn      = document.getElementById('sc-rec-btn');
  const playIcon    = document.getElementById('sc-play-icon');
  const recIcon     = document.getElementById('sc-rec-icon');
  const recLabel    = document.getElementById('sc-rec-label');
  const hint        = document.getElementById('sc-trio-hint');
  const compareCard = document.getElementById('sc-compare-card');
  const compareSub  = document.getElementById('sc-compare-sub');
  const comparePlay = document.getElementById('sc-compare-play');
  const wordAudioBtn = document.getElementById('sc-word-audio');
  const sentAudioBtn = document.getElementById('sc-sentence-audio');

  if (!modelBtn) return;
  // Audio buttons use global onclick handlers (playWordAudio, playSentenceAudio, playModelAudio)
  // Only wire the record/playback trio below

  // You / playback button
  function stopSCSelf() {
    if (scSelfAudio) { scSelfAudio.pause(); scSelfAudio = null; }
    scSelfPlaying = false;
    playIcon.textContent = '▶';
    playBtn.classList.remove('playing');
  }

  playBtn.addEventListener('click', () => {
    if (!scRecBlob) return;
    if (scSelfPlaying) { stopSCSelf(); return; }
    scSelfPlaying = true;
    playIcon.textContent = '⏸';
    playBtn.classList.add('playing');
    const url = URL.createObjectURL(scRecBlob);
    scSelfAudio = new Audio(url);
    scSelfAudio.onended = () => { stopSCSelf(); URL.revokeObjectURL(url); };
    scSelfAudio.onerror = () => { stopSCSelf(); URL.revokeObjectURL(url); };
    scSelfAudio.play().catch(stopSCSelf);
  });

  // Record button
  recBtn.addEventListener('click', async () => {
    if (scRecording) {
      scMediaRec?.stop();
      return;
    }
    stopSCSelf();
    window.speechSynthesis?.cancel();
    scModelPlaying = false;
    modelBtn.classList.remove('playing');
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mimeType = ['audio/webm;codecs=opus','audio/webm','audio/mp4','audio/ogg']
        .find(t => { try { return MediaRecorder.isTypeSupported(t); } catch(e) { return false; } }) || '';
      const chunks = [];
      scMediaRec = new MediaRecorder(stream, { mimeType });
      scMediaRec.ondataavailable = e => { if (e.data.size) chunks.push(e.data); };
      scMediaRec.onstop = async () => {
        stream.getTracks().forEach(t => t.stop());
        scRecording = false;
        recIcon.textContent  = '🎤';
        recLabel.textContent = 'Re-record';
        recBtn.classList.remove('recording');
        scRecBlob = new Blob(chunks, { type: mimeType });
        // Also key by word so You button survives navigation
        const _w = singleCards[currentSingleIdx]?.word;
        if (_w) scBlobMap[_w] = scRecBlob;
        playBtn.classList.add('ready');
        hint.textContent = 'Listen to both, then rate yourself.';

        // Save to history
        const card = singleCards[currentSingleIdx];
        const history = await saveRecToHistory(card.word, scRecBlob);

        // Show compare card if prior exists
        if (history.length >= 2) {
          const prev = history[history.length - 2];
          compareSub.textContent = 'Recorded ' + timeAgo(prev.ts);
          compareCard.style.display = 'flex';
          comparePlay.onclick = () => new Audio(prev.dataUrl).play().catch(()=>{});
        }

        // Refresh history list
        renderRecHistory(card.word, document.getElementById('sc-history-wrap'));
      };
      scMediaRec.start();
      scRecording = true;
      recIcon.textContent  = '⏹';
      recLabel.textContent = 'Stop';
      recBtn.classList.add('recording');
      hint.textContent = 'Recording… tap ⏹ to stop.';
    } catch(e) {
      hint.textContent = '⚠️ Microphone access needed.';
    }
  });
}

// Simple global audio handlers — called directly from HTML onclick
function playWordAudio() {
  const card = singleCards[currentSingleIdx];
  if (!card) return;
  playAudio(card.wordAudio, card.word);
}
function playSentenceAudio() {
  const card = singleCards[currentSingleIdx];
  if (!card) return;
  playAudio(card.sentenceAudio, card.sentence);
}
function playModelAudio() {
  const card = singleCards[currentSingleIdx];
  if (!card) return;
  const modelBtn = document.getElementById('sc-model-btn');
  if (modelBtn) modelBtn.classList.add('playing');
  const done = () => { if (modelBtn) modelBtn.classList.remove('playing'); };
  if (card.wordAudio) {
    const a = new Audio(card.wordAudio);
    a.onended = done; a.onerror = () => { speakTTS(card.word); done(); };
    a.play().catch(() => { speakTTS(card.word); done(); });
  } else {
    const utt = new SpeechSynthesisUtterance(card.word);
    utt.lang = 'en-GB'; utt.rate = 0.82;
    utt.onend = done;
    window.speechSynthesis?.cancel();
    window.speechSynthesis?.speak(utt);
  }
}

/* ═══════════════════════════════════════════════
   VIDEO MODAL
═══════════════════════════════════════════════ */
function openVideo() {
  openVideoData(currentVideoData);
}
function openVideoData(data) {
  if (!data) return;
  document.getElementById('modal-title').textContent = data.title || '';
  document.getElementById('modal-sub').textContent   = data.subtitle || '';
  document.getElementById('video-modal').classList.add('open');
}
function closeVideo() {
  document.getElementById('video-modal').classList.remove('open');
}

/* ═══════════════════════════════════════════════
   HELPERS
═══════════════════════════════════════════════ */
function highlightWord(sentence, word) {
  if (!sentence || !word) return sentence || '';
  const re = new RegExp(`\\b(${word})\\b`, 'gi');
  return sentence.replace(re, '<span class="sentence-hl">$1</span>');
}

function showScreen(id) {
  document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
  document.getElementById(id).classList.add('active');
}
function goIndex() {
  showScreen('screen-index');
  buildGrid(); // refresh dots
}

/* ── Pair trio record ── */
function togglePairRec(btn, word, side) {
  const youBtn  = document.getElementById('pair-you-'  + side + '-' + word);
  const recIcon = document.getElementById('pair-ri-'   + side + '-' + word);
  const recLbl  = document.getElementById('pair-rl-'   + side + '-' + word);
  const hint    = document.getElementById('pair-hint-' + side + '-' + word);
  const histEl  = document.getElementById('pair-hist-' + side + '-' + word);
  if (btn.classList.contains('recording')) { btn._mr?.stop(); return; }
  navigator.mediaDevices.getUserMedia({audio:true}).then(stream => {
    // Detect supported MIME — webm fails on iOS Safari
    const mime = ['audio/webm;codecs=opus','audio/webm','audio/mp4','audio/ogg']
      .find(t => { try { return MediaRecorder.isTypeSupported(t); } catch(e) { return false; } })
      || '';
    const chunks=[];
    const mr = new MediaRecorder(stream, mime ? {mimeType:mime} : {});
    btn._mr = mr;
    mr.ondataavailable = e=>{ if(e.data.size) chunks.push(e.data); };
    mr.onstop = async () => {
      stream.getTracks().forEach(t=>t.stop());
      btn.classList.remove('recording');
      if(recIcon) recIcon.textContent='🎤';
      if(recLbl)  recLbl.textContent='Re-record';
      const blob = new Blob(chunks,{type:mime});
      if(youBtn){ youBtn.classList.add('ready'); youBtn.onclick=()=>new Audio(URL.createObjectURL(blob)).play().catch(()=>{}); }
      const hist = await saveRecToHistory(word,blob);
      if(histEl) renderPairHistory(hist,histEl);
      if(hint) hint.textContent='Listen to both, then rate yourself.';
    };
    mr.start();
    btn.classList.add('recording');
    if(recIcon) recIcon.textContent='⏹';
    if(recLbl)  recLbl.textContent='Stop';
    if(hint)    hint.textContent='Recording... tap Stop.';
  }).catch(()=>{ if(recLbl) recLbl.textContent='No mic'; });
}

function renderPairHistory(history, el) {
  if (!history.length) { el.innerHTML = ''; return; }
  const reversed = history.slice().reverse();
  const bodyId = 'rph-body-' + Date.now();
  el.innerHTML =
    '<div class="rec-history">' +
    '<button class="rec-history-toggle-btn" onclick="toggleRecHistory(\'' + bodyId + '\', this)">▶ ' + history.length + ' past recording' + (history.length > 1 ? 's' : '') + '</button>' +
    '<div class="rec-history-body" id="' + bodyId + '">' +
    reversed.map((r, i) =>
      '<div class="rec-history-row">' +
      '<span class="rec-history-num">' + (history.length - i) + '</span>' +
      '<span class="rec-history-time">' + timeAgo(r.ts) + '</span>' +
      '<button class="rec-history-play">&#9654;</button>' +
      '</div>'
    ).join('') + '</div></div>';
  const btns = el.querySelectorAll('.rec-history-play');
  reversed.forEach((r, i) => {
    if (btns[i]) btns[i].addEventListener('click', () => playDataUrl(r.dataUrl));
  });
}

function initPairYouBtn(word, side) {
  const hist = loadRecHistory(word);
  if (!hist.length) return;
  try {
    const blob = dataUrlToBlob(hist[hist.length-1].dataUrl);
    const youBtn=document.getElementById('pair-you-'+side+'-'+word);
    const histEl=document.getElementById('pair-hist-'+side+'-'+word);
    if(youBtn){ youBtn.classList.add('ready'); youBtn.onclick=()=>new Audio(URL.createObjectURL(blob)).play().catch(()=>{}); }
    if(histEl) renderPairHistory(hist,histEl);
  } catch(e) {}
}


;

/* lazy image decode for pair card images */
function lazyLoadImages(root) {
  const imgs = (root || document).querySelectorAll('img[data-src]');
  imgs.forEach(img => {
    const src = img.getAttribute('data-src');
    if (!src) return;
    img.removeAttribute('data-src');
    const tmp = new Image();
    tmp.onload = () => { img.src = tmp.src; img.style.opacity = '1'; };
    tmp.src = src;
  });
}

function lazyLoadPairImages(layout, card) {
  // Set pair images via JS to avoid breaking HTML with raw base64 in attribute strings
  ['1','2'].forEach(side => {
    const img = layout.querySelector(`#pair-img-${side}-${card.word1}`);
    const src = card['image' + side];
    if (!img || !src) return;
    const tmp = new Image();
    tmp.onload = () => { img.src = tmp.src; img.style.opacity = '1'; };
    tmp.src = src;
  });
}

/* ── Boot ── */
loadDeck();

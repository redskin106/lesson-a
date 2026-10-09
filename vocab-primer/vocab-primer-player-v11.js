
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
// Which category groups the learner has opened. Survives grid rebuilds (rating a card rebuilds the grid).
const openCats = {};
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
    let collapsed = !openCats[label];
    const body = [];

    const header = document.createElement('div');
    header.className = 'cat-group-header';
    header.innerHTML = `<span class="cat-group-toggle">${collapsed ? '▶' : '▼'}</span><span class="cat-group-label">${label}</span><span class="cat-group-count">${groupCards.length}</span>`;
    header.onclick = () => {
      collapsed = !collapsed;
      openCats[label] = !collapsed;
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
      el.style.display = collapsed ? 'none' : ''; // keep the learner's open/closed choice
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
   TRANSLATIONS — two independent dropdowns
   One anchored under the word, one under the sentence.
   Each has its own active lang state.
═══════════════════════════════════════════════ */
const LANG_META = {
  vi: { flag: '🇻🇳', name: 'Vietnamese', dir: 'ltr' },
  km: { flag: '🇰🇭', name: 'Khmer',      dir: 'ltr' },
  ur: { flag: '🇵🇰', name: 'Urdu',       dir: 'rtl' },
  th: { flag: '🇹🇭', name: 'Thai',       dir: 'ltr' },
};

function getAvailableTranslations(card) {
  return ['vi','km','ur','th'].filter(lang => {
    const cap = lang.charAt(0).toUpperCase() + lang.slice(1);
    const key = 'translation' + cap;
    return (card[key] && card[key].trim())
        || (card[key+'1'] && card[key+'1'].trim())
        || (card[key+'2'] && card[key+'2'].trim());
  });
}

/* Build a self-contained translation dropdown widget.
   slot:    'word' | 'sentence'
   card:    card object
   side:    '1' | '2' | '' (single cards)
   id:      unique DOM id for this widget instance
*/
function buildTrWidget(slot, card, side, id) {
  const langs = getAvailableTranslations(card);
  if (!langs.length) return '';

  const cap = s => s.charAt(0).toUpperCase() + s.slice(1);
  const opts = langs.map(lang => {
    const m = LANG_META[lang];
    return `<button class="tr-opt" data-lang="${lang}" onclick="trSelect('${id}','${lang}',event)">${m.flag} ${m.name}</button>`;
  }).join('');

  return `<div class="tr-widget" id="${id}" data-slot="${slot}" data-side="${side}">
    <div class="tr-globe-wrap">
      <button class="tr-globe" onclick="trToggleMenu('${id}',event)" title="Translate">🌐</button>
      <div class="tr-menu" style="display:none">${opts}</div>
    </div>
    <div class="tr-text" style="display:none"></div>
  </div>`;
}

function trToggleMenu(id, e) {
  e && e.stopPropagation();
  const widget = document.getElementById(id);
  if (!widget) return;
  const menu   = widget.querySelector('.tr-menu');
  const text   = widget.querySelector('.tr-text');
  const globe  = widget.querySelector('.tr-globe');
  const isOpen = menu.style.display !== 'none';
  if (isOpen) {
    menu.style.display = 'none';
  } else {
    if (widget.dataset.activeLang && text.style.display !== 'none') {
      text.style.display = 'none';
      widget.dataset.activeLang = '';
      globe.classList.remove('active');
      globe.textContent = '🌐';
    } else {
      menu.style.display = '';
    }
  }
}

function trSelect(id, lang, e) {
  e && e.stopPropagation();
  const widget = document.getElementById(id);
  if (!widget) return;
  const menu  = widget.querySelector('.tr-menu');
  const text  = widget.querySelector('.tr-text');
  const globe = widget.querySelector('.tr-globe');
  const slot  = widget.dataset.slot;
  const side  = widget.dataset.side;
  const card  = widget._card;
  if (!card) return;

  const cap   = lang.charAt(0).toUpperCase() + lang.slice(1);
  const meta  = LANG_META[lang];
  const isRTL = meta.dir === 'rtl';
  let content = '';

  if (slot === 'word') {
    content = card['translation' + cap + side] || card['translation' + cap] || '';
  } else {
    content = card['sentence' + cap + side] || card['sentence' + cap] || '';
  }

  menu.style.display = 'none';
  if (!content) return;

  text.textContent = content;
  text.style.display = '';
  text.style.direction = isRTL ? 'rtl' : 'ltr';
  text.style.textAlign = isRTL ? 'right' : 'left';
  widget.dataset.activeLang = lang;
  globe.classList.add('active');
  globe.textContent = meta.flag;
}

/* Attach the card reference to a widget after it's in the DOM */
function bindTrWidget(id, card) {
  const el = document.getElementById(id);
  if (el) el._card = card;
}

/* Reset all translation widgets (call when navigating to new card) */
function resetTranslations() {
  activeTranslationLang = null; // kept for compat
}

/* ═══════════════════════════════════════════════
   SINGLE CARD
═══════════════════════════════════════════════ */
function openSingle(i) {
  currentSingleIdx = i;
  currentNavIdx = navOrder.indexOf(singleCards[i]);
  resetTranslations();
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
  document.getElementById('sc-sketch-word').textContent = card.word;

  // Word translation widget — injected right after word text
  const wordHero = document.getElementById('sc-word').parentElement;
  let wTrEl = document.getElementById('sc-word-tr');
  if (!wTrEl) {
    wTrEl = document.createElement('div');
    wTrEl.id = 'sc-word-tr';
    wordHero.insertAdjacentElement('afterend', wTrEl);
  }
  wTrEl.innerHTML = buildTrWidget('word', card, '', 'tr-sc-word');
  bindTrWidget('tr-sc-word', card);

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
  imgBlock.onclick = (card.illustration && !card.animation) ? () => {
    showingIllus = !showingIllus;
    renderCardImg(showingIllus);
  } : null;

  ilToggle.onclick = () => {
    showingIllus = !showingIllus;
    renderCardImg(showingIllus);
  };

  // Flip card: tap the picture for the animation (if the card has one)
  FlipCard.attach(imgBlock, card.animation, 'single');

  // Sentence
  const sentEl = document.getElementById('sc-sentence');
  sentEl.innerHTML = highlightWord(card.sentence, card.word);

  // Sentence translation widget
  let sTrEl = document.getElementById('sc-sent-tr');
  if (!sTrEl) {
    sTrEl = document.createElement('div');
    sTrEl.id = 'sc-sent-tr';
    sentEl.parentElement.insertAdjacentElement('afterend', sTrEl);
  }
  sTrEl.innerHTML = buildTrWidget('sentence', card, '', 'tr-sc-sent');
  bindTrWidget('tr-sc-sent', card);

  // Syllables (only for words of two or more syllables)
  stopSyllables();
  const syls = card.syllables || [];
  document.getElementById('sc-syl-sec').hidden = syls.length < 2;
  document.getElementById('sc-syllables').innerHTML = syls.length >= 2 ? syllableBoxHTML(syls) : '';

  // Phonemes
  const phEl = document.getElementById('sc-phonemes');
  phEl.innerHTML = (card.phonemes || []).map((ph, pi) =>
    `<button class="ph-tile" onclick="this.classList.toggle('tapped');playPhoneme('${ph.s}','${ph.audio||''}')">
      ${ph.s}
    </button>`
  ).join('');

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
  resetTranslations();
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
  stopSyllables();
  layout.innerHTML = buildPairHalfHTML(card, 1) + buildPairHalfHTML(card, 2);
  lazyLoadPairImages(layout, card);
  layout.querySelectorAll('.pair-card-img').forEach((frame, n) => FlipCard.attach(frame, card['animation' + (n + 1)], 'pair'));

  // Bind card reference to translation widgets (needed for trSelect)
  [`tr-pair-word-1-${card.word1}`, `tr-pair-sent-1-${card.word1}`,
   `tr-pair-word-2-${card.word1}`, `tr-pair-sent-2-${card.word1}`].forEach(id => bindTrWidget(id, card));

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

  const trWordId = `tr-pair-word-${side}-${card.word1}`;
  const trSentId = `tr-pair-sent-${side}-${card.word1}`;

  return `
  <div class="pair-card-half">
    <div class="pair-word-row">
      <div class="pair-word-text">${word}${card['word'+side+'note'] ? `<span style="font-size:9px;color:var(--cream-dim);font-family:'Inter',sans-serif;font-weight:400;margin-left:4px;">*</span>` : ''}</div>
    </div>
    <div class="act-row act-word">
      <button class="pair-word-audio" data-audio="${card['wordAudio'+side]||''}" data-tts="${qa(word)}" onclick="playAudio(this.dataset.audio,this.dataset.tts)">🔊</button>
      ${buildTrWidget('word', card, side, trWordId)}
    </div>
    <div class="pair-card-img-wrap"><div class="pair-card-img">${imgContent}</div></div>
    <details class="section ex">
      <summary class="slabel">Example</summary>
      <div class="section-body">
        <div class="pair-sentence"><span>${highlightWord(sentence, word)}</span></div>
        <div class="act-row act-sent">
          <button class="pair-s-audio" data-audio="${card['sentenceAudio'+side]||''}" data-tts="${qa(sentence)}" onclick="playAudio(this.dataset.audio,this.dataset.tts)">🔊</button>
          ${buildTrWidget('sentence', card, side, trSentId)}
        </div>
      </div>
    </details>
    ${(card['syllables'+side] || []).length >= 2 ? `<details class="section syl">
      <summary class="slabel">Syllables</summary>
      <div class="section-body"><div class="sounds-wrap">${syllableBoxHTML(card['syllables'+side])}</div></div>
    </details>` : ''}
    <details class="section snd">
      <summary class="slabel">Sounds</summary>
      <div class="section-body"><div class="sounds-wrap">
        <div class="pair-phonemes">
          ${phonemes.map(ph => `<button class="pair-ph" data-phoneme="${ph.s}" data-audio="${ph.audio||''}">${ph.s}</button>`).join('')}
        </div>
        <p class="trio-hint">Tap a sound to hear it.</p>
      </div></div>
    </details>
    <details class="section say">
      <summary class="slabel">Say it</summary>
      <div class="section-body"><div class="trio-wrap" id="pair-wrap-${side}-${word}">
        <div class="trio-row">
          <button class="trio-btn model"
            data-audio="${card['wordAudio'+side]||''}" data-tts="${qa(word)}"
            onclick="playAudio(this.dataset.audio,this.dataset.tts)">
            <span class="trio-icon">&#128266;</span><span class="trio-label">Model</span>
          </button>
          <button class="trio-btn playback" id="pair-you-${side}-${word}">
            <span class="trio-icon">&#9654;</span><span class="trio-label">You</span>
          </button>
          <button class="trio-btn record" id="pair-rec-${side}-${word}"
            onclick="togglePairRec(this,'${qa(word)}','${side}')">
            <span class="trio-icon" id="pair-ri-${side}-${word}">&#127908;</span>
            <span class="trio-label" id="pair-rl-${side}-${word}">Record</span>
          </button>
        </div>
        <p class="trio-hint" id="pair-hint-${side}-${word}">Hear the model, then record yourself.</p>
        <div id="pair-hist-${side}-${word}"></div>
      </div></div>
    </details>
    ${video ? `<button class="pair-video-btn" style="background:var(--coral-dim);border:1.5px solid var(--coral);border-radius:var(--rpill);padding:6px 12px;color:var(--coral);font-size:11px;font-weight:600;display:flex;align-items:center;gap:4px;" onclick="openVideoData(${JSON.stringify(video).replace(/"/g,'&quot;')})">🎬 ${video.title}</button>` : ''}
    <details class="section pair-sketch-sec sk">
      <summary class="slabel">Draw</summary>
      <div class="section-body"><div class="sounds-wrap sketch-wrap"><div class="sketch-paper"><span class="sk-emoji" aria-hidden="true">✍️🎨</span></div><div class="sketch-word">${word}</div><p class="trio-hint">Write the word. Draw it.</p></div></div>
    </details>
    <details class="section pair-rating-sec rate">
      <summary class="slabel">How did it go?</summary>
      <div class="section-body"><div class="sounds-wrap"><div class="pair-rating">
        <button class="pair-rating-btn${rating==='got-it'?' got-it':''}" data-rate="got-it" data-side="${side}" aria-label="Got it"><span class="rate-emoji" aria-hidden="true">😊</span></button>
        <button class="pair-rating-btn${rating==='practicing'?' practicing':''}" data-rate="practicing" data-side="${side}" aria-label="Still practising"><span class="rate-emoji" aria-hidden="true">😅</span></button>
      </div></div></div>
    </details>
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


/* ═══════════════════════════════════════════════
   SYLLABLES — split by sound, played one chunk at a time or all in a row
═══════════════════════════════════════════════ */
let _sylToken = 0, _sylAudio = null;
function syllableBoxHTML(syls) {
  const tiles = syls.map((sy, i) =>
    `<button class="syl-tile${sy.stress ? ' stress' : ''}" data-audio="${sy.audio || ''}" data-tts="${qa(sy.s)}" onclick="playSyllable(this)">${sy.s}</button>`).join('');
  return `<div class="syl-tiles">${tiles}</div>
    <div class="syl-controls"><button class="syl-all" data-ic="play" aria-label="Play every syllable in order" onclick="playAllSyllables(this)">&#9654;</button></div>
    <p class="trio-hint">Tap a syllable to hear it.</p>`;
}
function stopSyllables() {
  _sylToken++;
  if (_sylAudio) { try { _sylAudio.pause(); } catch (e) {} _sylAudio = null; }
  if (window.speechSynthesis) speechSynthesis.cancel();
  document.querySelectorAll('.syl-tile.syl-on').forEach(t => t.classList.remove('syl-on'));
  document.querySelectorAll('.syl-all.playing').forEach(b => { b.classList.remove('playing'); b.dataset.ic = 'play'; });
}
function sylClipDone(url, tts) {
  return new Promise(res => {
    let done = false; const fin = () => { if (!done) { done = true; res(); } };
    const speak = () => {
      if (tts && window.speechSynthesis) {
        const u = new SpeechSynthesisUtterance(tts); u.lang = 'en-GB'; u.rate = 0.8;
        u.onend = fin; u.onerror = fin; speechSynthesis.speak(u);
        setTimeout(fin, 1800); // some browsers never fire onend
      } else setTimeout(fin, 700);
    };
    if (url) {
      const a = new Audio(url); _sylAudio = a;
      a.addEventListener('ended', fin);
      a.addEventListener('error', speak);
      a.play().catch(fin);
    } else speak();
  });
}
async function sylClip(tile, token) {
  tile.classList.add('syl-on');
  // Highlight for at least half a second, even when the clip is shorter or the voice fails to start
  await Promise.all([sylClipDone(tile.dataset.audio, tile.dataset.tts), new Promise(r => setTimeout(r, 500))]);
  if (token === _sylToken) tile.classList.remove('syl-on');
}
async function playSyllable(tile) {
  stopSyllables();
  const t = _sylToken;
  await sylClip(tile, t);
}
async function playAllSyllables(btn) {
  if (btn.classList.contains('playing')) { stopSyllables(); return; }
  stopSyllables();
  const t = _sylToken;
  const tiles = [...btn.closest('.sounds-wrap').querySelectorAll('.syl-tile')];
  btn.classList.add('playing'); btn.dataset.ic = 'pause';
  for (const tile of tiles) {
    if (t !== _sylToken) return;
    await sylClip(tile, t);
    await new Promise(r => setTimeout(r, 150));
  }
  if (t === _sylToken) { btn.classList.remove('playing'); btn.dataset.ic = 'play'; }
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

// Per-word recording history. Kept on this device only (IndexedDB, with localStorage as a fallback). Never uploaded.
// Learners keep their own takes so they can hear their progress. The newest REC_MAX are kept, no expiry.
// key: word → array of {ts, dataUrl, b} oldest first. A memory copy keeps the rest of the player synchronous.
const REC_MAX = 3;
const recCache = {};
let recDB = null;

function recStorageKey(word) { return 'vp_rec_' + word; }

function recOpen() {
  return new Promise(res => {
    try {
      const rq = indexedDB.open('sxl-rec', 1);
      rq.onupgradeneeded = () => rq.result.createObjectStore('rec');
      rq.onsuccess = () => res(rq.result);
      rq.onerror = () => res(null);
    } catch (e) { res(null); }
  });
}
function recPut(word, history) {
  if (recDB) { try { recDB.transaction('rec', 'readwrite').objectStore('rec').put(history, word); return; } catch (e) {} }
  try { localStorage.setItem(recStorageKey(word), JSON.stringify(history)); } catch (e) {}
}
async function recInit() {
  recDB = await recOpen();
  if (recDB) {
    await new Promise(res => {
      try {
        const rq = recDB.transaction('rec').objectStore('rec').openCursor();
        rq.onsuccess = () => { const c = rq.result; if (c) { recCache[c.key] = c.value; c.continue(); } else res(); };
        rq.onerror = () => res();
      } catch (e) { res(); }
    });
  }
  // Move anything the older version kept in localStorage
  try {
    Object.keys(localStorage).filter(k => k.startsWith('vp_rec_')).forEach(k => {
      const w = k.slice(7), old = JSON.parse(localStorage.getItem(k) || '[]');
      if (!recCache[w] || !recCache[w].length) recCache[w] = old.slice(-REC_MAX);
      if (recDB) { recPut(w, recCache[w]); localStorage.removeItem(k); }
    });
  } catch (e) {}
  if (typeof refreshRecUI === 'function') refreshRecUI();
}
function loadRecHistory(word) { return recCache[word] || []; }
function deleteRecs(word) {
  delete recCache[word];
  if (recDB) { try { recDB.transaction('rec', 'readwrite').objectStore('rec').delete(word); } catch (e) {} }
  try { localStorage.removeItem(recStorageKey(word)); } catch (e) {}
  delete scBlobMap[word];
}

// Seven small bars from the real audio, so each take shows its own shape
async function recBars(blob) {
  try {
    const AC = window.AudioContext || window.webkitAudioContext;
    const ctx = new AC();
    const buf = await ctx.decodeAudioData(await blob.arrayBuffer());
    const d = buf.getChannelData(0), n = 28, step = Math.floor(d.length / n) || 1, out = [];
    for (let i = 0; i < n; i++) { let sum = 0, c = 0; for (let j = i * step; j < Math.min((i + 1) * step, d.length); j += 8) { sum += d[j] * d[j]; c++; } out.push(Math.sqrt(sum / (c || 1))); }
    const mx = Math.max.apply(null, out) || 1; ctx.close && ctx.close();
    return out.map(v => Math.max(18, Math.round(v / mx * 100)));
  } catch (e) { return null; }
}

function saveRecToHistory(word, blob) {
  return new Promise(resolve => {
    const reader = new FileReader();
    reader.onload = async () => {
      const bars = await recBars(blob);
      let history = loadRecHistory(word).slice();
      history.push({ ts: Date.now(), dataUrl: reader.result, b: bars });
      if (history.length > REC_MAX) history = history.slice(-REC_MAX);
      recCache[word] = history;
      recPut(word, history);
      resolve(history);
    };
    reader.readAsDataURL(blob);
  });
}

recInit();

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

// Simplified waveform: one smooth, mirrored shape drawn from the stored loudness values.
function waveSVG(b) {
  if (!b || b.length < 2) return '';
  const W = 100, H = 40, mid = H / 2, n = b.length;
  const pts = b.map((v, i) => [i * W / (n - 1), Math.max(1.5, v / 100 * mid * 0.95)]);
  const curve = (arr, sgn) => {
    let d = '';
    for (let i = 0; i < arr.length - 1; i++) {
      const p0 = arr[i - 1] || arr[i], p1 = arr[i], p2 = arr[i + 1], p3 = arr[i + 2] || p2;
      const y = q => mid - sgn * q[1];
      const c1 = [p1[0] + (p2[0] - p0[0]) / 6, mid - sgn * (p1[1] + (p2[1] - p0[1]) / 6)];
      const c2 = [p2[0] - (p3[0] - p1[0]) / 6, mid - sgn * (p2[1] - (p3[1] - p1[1]) / 6)];
      d += ' C' + c1[0].toFixed(1) + ',' + c1[1].toFixed(1) + ' ' + c2[0].toFixed(1) + ',' + c2[1].toFixed(1) + ' ' + p2[0].toFixed(1) + ',' + y(p2).toFixed(1);
    }
    return d;
  };
  const top = 'M0,' + (mid - pts[0][1]).toFixed(1) + curve(pts, 1);
  const rev = pts.slice().reverse();
  const bottom = ' L' + W + ',' + (mid + pts[n - 1][1]).toFixed(1) + curve(rev, -1) + ' Z';
  return '<svg viewBox="0 0 ' + W + ' ' + H + '" preserveAspectRatio="none" aria-hidden="true"><path d="' + top + bottom + '"/></svg>';
}
// One history list for single and pair cards: a collapsible row, then numbered takes (1 = newest) with their date and shape.
function dayMonth(ts) {
  const a = new Date(ts), b = new Date();
  const n = Math.round((new Date(b.getFullYear(), b.getMonth(), b.getDate()) - new Date(a.getFullYear(), a.getMonth(), a.getDate())) / 864e5);
  return n <= 0 ? 'Today' : n === 1 ? 'Yesterday' : n + ' days ago';
}
function renderTakes(word, container) {
  const history = loadRecHistory(word);
  if (!container) return;
  const wasOpen = !!(container.querySelector('details.past') || {}).open;
  if (!history.length) { container.innerHTML = ''; return; }
  const rev = history.slice().reverse();
  container.innerHTML =
    '<details class="past"><summary aria-label="Past recordings"><span class="past-ic" aria-hidden="true"></span><span class="past-lbl">Show past recordings</span><span class="past-chev" aria-hidden="true"></span></summary>' +
    '<div class="past-list">' +
    rev.map((r, i) =>
      '<div class="past-row' + (i === 0 ? ' new' : '') + '">' +
      '<span class="past-n">' + (i + 1) + '</span>' +
      '<span class="past-d">' + dayMonth(r.ts) + '</span>' +
      '<span class="past-w">' + waveSVG(r.b) + '</span>' +
      '<button type="button" class="past-p" aria-label="Play take ' + (i + 1) + '"></button>' +
      '</div>').join('') +
    '</div>' +
    '<div class="past-keep"><span class="past-lock" role="img" aria-label="Stays on this device"></span><button type="button" class="past-bin" aria-label="Delete my recordings"></button></div>' +
    '</details>';
  const det = container.querySelector('details.past');
  if (wasOpen) { det.open = true; det.querySelector('.past-lbl').textContent = 'Hide past recordings'; }
  det.addEventListener('toggle', () => { det.querySelector('.past-lbl').textContent = det.open ? 'Hide past recordings' : 'Show past recordings'; });
  container.querySelectorAll('.past-p').forEach((b, i) => b.addEventListener('click', () => playDataUrl(rev[i].dataUrl)));
  container.querySelector('.past-bin').addEventListener('click', () => { deleteRecs(word); container.innerHTML = ''; refreshRecUI(); });
}
function renderRecHistory(word, container) { renderTakes(word, container); }
function toggleRecHistory() {}
function refreshRecUI() {
  try { if (document.getElementById('screen-single').classList.contains('active') && typeof resetSCTrio === 'function') resetSCTrio(); } catch (e) {}
  document.querySelectorAll('[id^="pair-hist-"]').forEach(el => {
    const m = el.id.match(/^pair-hist-[12]-(.+)$/); if (!m) return;
    const hist = loadRecHistory(m[1]); const side = el.id.split('-')[2];
    if (hist.length) renderTakes(m[1], el); else el.innerHTML = '';
    const you = document.getElementById('pair-you-' + side + '-' + m[1]);
    if (you) { if (hist.length) { you.classList.add('ready'); you.onclick = () => playDataUrl(hist[hist.length - 1].dataUrl); } else { you.classList.remove('ready'); you.onclick = null; } }
  });
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
        hint.textContent = 'Listen to both, then test yourself.';

        // Save to history
        const card = singleCards[currentSingleIdx];
        const history = await saveRecToHistory(card.word, scRecBlob);


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
      if(histEl) renderPairHistory(word,histEl);
      if(hint) hint.textContent='Listen to both, then test yourself.';
    };
    mr.start();
    btn.classList.add('recording');
    if(recIcon) recIcon.textContent='⏹';
    if(recLbl)  recLbl.textContent='Stop';
    if(hint)    hint.textContent='Recording... tap Stop.';
  }).catch(()=>{ if(recLbl) recLbl.textContent='No mic'; });
}

function renderPairHistory(word, el) { renderTakes(word, el); }

function initPairYouBtn(word, side) {
  const hist = loadRecHistory(word);
  if (!hist.length) return;
  try {
    const blob = dataUrlToBlob(hist[hist.length-1].dataUrl);
    const youBtn=document.getElementById('pair-you-'+side+'-'+word);
    const histEl=document.getElementById('pair-hist-'+side+'-'+word);
    if(youBtn){ youBtn.classList.add('ready'); youBtn.onclick=()=>new Audio(URL.createObjectURL(blob)).play().catch(()=>{}); }
    if(histEl) renderPairHistory(word,histEl);
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

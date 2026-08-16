# Shell Design Spec & Module Consistency Checklist
**Reference for all module development — every new or edited module must pass this checklist before push.**

---

## 1. Design Tokens

### Colour palette
| Token | Value | Usage |
|---|---|---|
| Background | `#0D0C1D` | Screen background |
| Primary text | `#EEF2F7` | Main readable text |
| Dim text | `rgba(255,255,255,0.4)` | Secondary/hint text |
| Accent | `#4FC3F7` | Context clues, highlights |
| Bronze | `#CD7F32` | Bronze tier |
| Silver | `#A0AEC0` | Silver tier |
| Gold | `#FFD700` | Gold tier |
| Pass (border) | `#8BC34A` | Correct border |
| Pass (text) | `#AED581` | Correct text |
| Fail (border) | `#E91E63` | Wrong border |
| Fail (text) | `#F48FB1` | Wrong text |
| Purple (selected border) | `#7052B4` | Selected state |
| Purple (selected text) | `#C9B8EA` | Selected text |

### Interactive state colours
| State | Border | Background | Text |
|---|---|---|---|
| Default | `rgba(255,255,255,0.08)` | `rgba(255,255,255,0.05)` | `rgba(255,255,255,0.85)` |
| Selected | `#7052B4` | `rgba(112,82,180,0.18)` | `#C9B8EA` |
| Correct | `#8BC34A` | `rgba(139,195,74,0.15)` | `#AED581` |
| Wrong | `#E91E63` | `rgba(233,30,99,0.12)` | `#F48FB1` |
| Used/disabled | — | — | `opacity:0` or `0.25` |

---

## 2. Typography Scale (cqw units)

| Element | Size | Weight | Colour |
|---|---|---|---|
| Module title | `3.9cqw` | `500` | `#fff` |
| Question label | `3cqw` | `400` | `rgba(255,255,255,0.75)` |
| Main question text | `4.4cqw` | `500–600` | `#fff` |
| Option button text | `3.4cqw` | `400` | `rgba(255,255,255,0.85)` |
| Large emoji (stimulus) | `15cqw` | — | — |
| Medium emoji (in tile) | `8–10cqw` | — | — |
| Letter tile text | `5cqw` | `700` | — |
| Feedback text | `3.4cqw` | `400` | `#AED581` or `#F48FB1` |
| Hint/dim text | `3cqw` | `400` | `rgba(255,255,255,0.4)` |
| Section label (UPPERCASE) | `2.8cqw` | `400` | dim + `letter-spacing:.08em` |
| Proceed/Next button | `4.4cqw` | `500` | `#fff` |

---

## 3. Spacing System (% of container width)

| Use | Value |
|---|---|
| Between major blocks | `5%` margin-bottom |
| Option tile grid gap | `4%` |
| Letter tile gap | `2–2.5%` |
| Stacked item gap (seq/sb) | `1.44cqw` |
| Tile internal padding | `4% 3%` |
| Card internal padding | `5% 6%` |
| Feedback min-height | `4cqw` |
| After feedback to button | `2%` |

---

## 4. Border Radius

| Element | Radius |
|---|---|
| Option buttons | `12px` |
| Large word cards | `14px` |
| Letter tiles | `10px` |
| Pill buttons | `999px` |
| Text input | `12px` |
| Context/info banners | `14px` |
| Statement panels | `14px` |

---

## 5. Core CSS Classes (always reuse, never reinvent)

### Option tiles
```
.iv-options-grid     grid wrapper: 2-col, gap:4%
.iv-option-btn       tile: all states built in
.iv-option-btn.emoji-opt   emoji tiles: font-size:8cqw
```

### Letter tiles
```
.ws-slots-v2 / .ws-bank-v2    slot row and pool row
.ws-slot-v2 / .ws-tile-v2     slot and pool tile
Default size: 11cqw × 13cqw, font-size:5cqw, font-weight:700
Phonics override: 16cqw × 16cqw
```

### Sentence/sequencing tiles
```
.seq-slots-v2 / .seq-pool-v2 / .seq-item-v2
.sb-slots-v2  / .sb-bank-v2  / .sb-tile-v2
font-size: 3.4–3.6cqw; border-radius: 12px
```

### Pip rows
```
.mp-pips-row-v2    flex row, gap:1.5%, margin-bottom:3%
.mp-pip-v2         default/current/done
Only show when session.length > 1
```

### Feedback
```
.ws-feedback-v2    min-height:4cqw; text-align:center; font-size:3.4cqw
Correct: #AED581 | Wrong: #F48FB1 | Neutral: rgba(255,255,255,0.4)
```

### Buttons
```
Check/action (purple pill):
  padding:3% 12%; border-radius:999px
  background:rgba(112,82,180,0.16); border:1.5px solid rgba(112,82,180,0.5)
  color:#C9B8EA  →  .gf-check-btn

Next/proceed (gradient pill):
  background:linear-gradient(180deg,#3D30B7 0%,#7052B4 45%,#A45B8B 100%)
  color:#fff  →  .iv-proceed-btn

Hint (teal pill):
  background:rgba(79,195,247,0.1); border:1.5px solid rgba(79,195,247,0.4)
  color:#4FC3F7  →  .precheck-hint-btn

Play (circular, purple):
  border-radius:50%; width:9cqw; height:9cqw
  background:rgba(112,82,180,0.16)  →  .ws-play-btn-v2
```

### Panels
```
Context/info banner:
  background:rgba(0,188,212,0.07); border:1.5px solid rgba(0,188,212,0.18)
  border-radius:14px; padding:4% 5%

Statement/sentence:
  background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.08)
  border-radius:14px; padding:5% 6%
```

---

## 6. Standard Module Structure (top to bottom)

```
1. Pip row (only if >1 question)        .mp-pips-row-v2
2. Visual stimulus                      emoji, image, or audio button
3. Question / prompt text               4.4cqw, #fff
4. Interactive area                     tiles, option grid, etc.
5. Feedback line                        .ws-feedback-v2
6. Next / proceed button                .iv-proceed-btn
```

---

## 7. Module Consistency Checklist

### Layout
- [ ] No px sizing — use cqw or % only
- [ ] No hardcoded hex colours — use token values
- [ ] 5% margin-bottom between major sections
- [ ] Pip row hidden when only 1 question
- [ ] No double progress bar (pips ≠ shell bar)
- [ ] No horizontal overflow

### Tiles & options
- [ ] Option buttons use .iv-option-btn (or module equivalent)
- [ ] Option grid uses .iv-options-grid (2-col) or column flex (Gold)
- [ ] Letter tiles: 11cqw × 13cqw, 5cqw font (phonics: 16cqw)
- [ ] Tiles: border-radius 10–12px (never 999px)
- [ ] All 4 states implemented: default, selected, correct, wrong

### Buttons
- [ ] Check: purple pill
- [ ] Next: gradient pill (.iv-proceed-btn)
- [ ] Hint: teal pill (.precheck-hint-btn)
- [ ] Play: circular 9cqw purple
- [ ] All buttons: font-family:inherit; cursor:pointer

### Feedback
- [ ] Feedback line present, min-height:4cqw
- [ ] Correct: #AED581 | Wrong: #F48FB1 | Hint: rgba(255,255,255,0.4)
- [ ] No answer ever shown — hints narrow the space only

### Audio
- [ ] No auto-play on load
- [ ] Correct: celebrate voice, word spoken once
- [ ] Wrong: no audio or neutral only
- [ ] Phonemes: assets/phonemes/sound_{grapheme}.mp3 + TTS fallback

### UX
- [ ] Active/tap state on all interactive elements
- [ ] Disabled: opacity:0.3 or pointer-events:none
- [ ] Retry possible after wrong
- [ ] font-family:inherit on all buttons

---

## 8. Module Reference Table

| Module | Stimulus | Interaction | Feedback class |
|---|---|---|---|
| Gap-fill | Sentence panel | 4-pill grid | .gf-status |
| True/False | Statement panel | 2 buttons + Check | Grammar overlay |
| Picture & Word | Emoji + word | 4-option grid | .iv-feedback |
| Listen & Choose | Audio play btn | 4-option grid | inline |
| Word Match | — | 2-col word grid | encourage text |
| Sequencing | Prompt text | Slots + pool | .gf-status |
| Memory Pairs | Card grid | Tap to flip | .mp-status-v2 |
| Word Scramble | Emoji + play | Letter slots + bank | .ws-feedback-v2 |
| Spelling | Emoji/audio + play | Letter slots + bank | .sp-feedback-v2 |
| Sentence Building | Prompt | Word slots + bank | .sb-feedback-v2 |
| Question Formation | Situation panel | Word slots + bank | inline |
| Phonics | Emoji + word (Bronze) | Phoneme tiles | .ws-feedback-v2 |
| Listen Closely | Sound banner + play | 2-option cards | .ws-feedback-v2 |
| Description Pyramid | Object image | Tier blocks + tiles | Sentence strip |

---

## 9. Known Drift Issues (audit backlog)

- [ ] Listen Closely — word cards: listen button sits outside card
- [ ] Listen Closely — second progress bar showing
- [ ] Sound It Out — pip row shows even with 1 question (fixed in code, verify live)
- [ ] Description Pyramid — sentence assembly produces broken English
- [ ] Reflection Card — output broken
- [ ] Any module with hardcoded px sizes
- [ ] Any module with inline hex colours not matching token values

## 10. Frame & Mask Notes
- `frame-mask` uses `top: -4px` (not `inset: 0`) to shift mask up slightly and cover scene bleed at bottom edge
- `layer-bg` stays at z-index 0 — raising it breaks all UI content
- `app-frame` has `clip-path: inset(0 0 0 0 round 12.7cqw)` as belt-and-braces corner clipping
- If bleed returns, increase `top` negative value (e.g. `-6px`, `-8px`) — do NOT touch z-index

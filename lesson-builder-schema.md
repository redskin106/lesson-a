# Lesson Builder — Content Schema Reference
_Pulled directly from the live repo's 12 module demos, July 2026. This is the backbone the builder's authoring forms, draft store, and publish step all need to agree on._

---

## Shared structural pattern

**SUPERSEDED as of the shell-v2 merge work — see note below.** This section originally described
two shapes found in the live demo files. That split has since been resolved into one standard,
per Nick's decision: **every module is a per-tier pool**, full stop.

**Current standard**: every tier for every module is `{ pick: number, items: [...] }`.
- `items` is a **separate pool per tier** — content differs per tier (harder as tiers progress),
  never shared/reused across bronze/silver/gold. This applies even to modules that used to share
  one pool across all tiers (Memory Pairs, Picture & Word) — reversed on the reasoning that
  identical exercises across tiers didn't make pedagogical sense once actually built.
- `pick` is the number of items drawn per session — **configurable per lesson/module**, not a
  hardcoded constant. The builder needs a real field for this, not an assumed default (existing
  merged modules default to `pick: 2`–`3` in test data, but that's just a placeholder, not a rule).

Original text below, kept for history — **the Shape A / Shape B split it describes no longer
exists as a distinction the builder needs to handle.** All modules are now the former "Shape B."

~~**A) Fixed 3-question array**~~ (`questions = [...]`) — one hardcoded item per tier, selected via `?tier=` → index (bronze=0, silver=1, gold=2). No pooling, no shuffle.
~~Used by: **Gap-fill, True/False, Listen & Choose, Say It**~~ — **now pool-based like everything else.**

**B) Tiered pools** (`tiers = [{ items: [...] }, ...]`) — each tier is a pool of items; a session draws a random subset via `safeShuffle(...).slice(0, PICK)`. `PICK` is a per-module constant (seen values: 3–4) — **now a configurable `pick` field, not a constant.**
Used by: **all 12 modules**, as of this decision.

**This split matters for the builder**: ~~Shape A modules need exactly 3 items authored (one per tier, no more).~~ Every module now needs a *pool* per tier — teachers should be able to add/remove pool items freely, and the builder should show how many items exist vs. how many `pick` will draw, so a teacher doesn't accidentally leave a pool too thin. This is no longer module-type-dependent; it applies uniformly.

---

## Shared sub-structures (used across many modules)

**`tokens` (grammar-tagged sentence)** — array of `{ text, role }`. `role` is one of `subject | verb | object | place | time | connector | null`. Only the first five have defined colors in `GRAMMAR_COLORS`; `connector` and `null` render as plain white text. **Builder implication**: the token editor needs a role-picker per chunk, defaulting to "no color" — this is effectively a small structured sentence-builder UI in its own right, reusable across every module type that has `tokens`.

**Icon/image field** — currently **emoji characters** (e.g. `'🐕'`), not image file references, in Picture & Word, Word Scramble, and Spelling. This is the main thing to flag for your "replace icons with images" goal: today there's no image asset per vocabulary item at all in most modules — illustration is a single per-lesson scene image (`school_scene.png`), separate from per-item icons. If you want teachers to swap a per-word icon for a custom image, that's a **new field**, not an edit to an existing one — worth deciding whether it stays emoji-first with optional image override, or fully switches to an image reference (which then needs to flow into the "publish pushes assets to every module folder" step we discussed).

---

## Per-module schema

### 1. Gap-fill
```
tier: { pick: number, items: [ { sentence: string (with "___" blank), answer: string, options: string[], tokens: TokenArray } ] }
```
**Now pool-based** (was: exactly 1 fixed item per tier, no pooling). Confirmed working in
`lesson-shell-v2.html` — retry-until-correct scoring per question, averaged across the `pick`
questions drawn for the session. `options.length` still varies 4–6, not fixed.

### 2. True/False
```
tier: { pick: number, items: [ { statement: string, answer: boolean, tokens: TokenArray } ] }
```
**Now pool-based** (was: exactly 1 fixed item per tier, no pooling). Confirmed working in
`lesson-shell-v2.html` — single attempt per question, score averaged across the `pick`
questions drawn for the session.

### 3. Word Match
```
tier: { pick: number, pairs: [ { left: string, right: string } ] }
```
Pool size grows per tier in the sample (3 → 4 → 5 pairs) but nothing enforces that — needs an
explicit `pick` field like every other module now, rather than just drawing the whole pool.

### 4. Memory Pairs
```
tier: { pick: number, flipback: number(ms), items: [ { word: string, emoji: string, image: null, sentence: string, tokens: TokenArray } ] }
```
**Reversed from the original shared-pool design** (was: one `allItems` pool reused across all
tiers, with tiers only changing `pairs`/`flipback` settings). Now a separate pool per tier, same
as every other module — `pick` controls how many pairs are drawn this session, `flipback` is
still a real per-tier timing setting (cards flip back faster at higher tiers). Still the only
module with an explicit (currently unused) `image: null` field already sitting next to `emoji`.

### 5. Listen & Choose
```
tier: { pick: number, items: [ { audio: string (text-to-speak), question: string, options: string[], answer: string } ] }
```
**Not yet merged into `lesson-shell-v2.html`** — still the old fixed-1-item-per-tier shape live
today. Should follow the same pool standard as everything else once its turn comes. `audio` is
the literal text passed to TTS — a natural ElevenLabs hook point (generate once, cache, reuse
instead of live TTS).

### 6. Put in Order
```
tier: { pick: number, items: [ { prompt: string, sequence: string[], correct: string[] } ] }
```
**Resolving a contradiction from the original version of this doc**, which listed this module
under the pooled group at the top but then noted "3 tiers, 1 sequence each (not pooled)" here —
those two statements disagreed. Now explicitly pool-based like every other module: each tier
gets its own set of orderable sequences, `pick` draws how many the session uses. `sequence` is
the shuffled/display order, `correct` is the target order — same strings, different order.

### 7. Say It
```
tier: { pick: number, items: [ { prompt: string, target: string (word or sentence to speak) } ] }
```
**Not yet merged into `lesson-shell-v2.html`** — still the old fixed-1-item-per-tier shape live
today. Should follow the same pool standard once its turn comes. Another direct ElevenLabs hook
(model/reference audio for the target).

### 8. Picture & Word
```
tier: { pick: number, mode: 'word-to-image' | 'image-to-word' | 'cloze-image', items: [ { word: string, emoji: string, sentence: string, cloze: string } ] }
```
**Reversed from the original shared-pool design** (was: one `allItems` pool reused across all
tiers, with tiers only changing `mode`). Now a separate pool per tier, same as every other
module — each tier keeps its own `mode` plus its own `items`, and `pick` (was a hardcoded
`PICK = 3`) draws from that tier's own pool each session.

### 9. Word Scramble
```
tier: { pick: number, items: [ { word: string, emoji: string, sentence?: string, clozeWord?: string, tokens: TokenArray } ] }
```
Separate pool per tier (this was already the pattern here — no reversal needed, unlike Memory Pairs/Picture & Word). Needs an explicit `pick` field added like every other module now. `sentence`/`clozeWord` are inconsistently present — only some items have them.

### 10. Spelling
```
tier: { pick: number, name: string, items: [ { word: string, emoji?: string, tokens: TokenArray|null } ] }
```
Separate pool per tier (already the pattern, needs explicit `pick` added). Note `emoji` and `tokens` are both sometimes omitted/null (gold tier examples have `tokens: null`) — the builder should treat these as optional, not required, fields.

### 11. Listen & Match
```
tier: { pick: number, pairs: [ { left: string, right: string } ] }
```
Same shape as Word Match, needs the same explicit `pick` field added. In every sample pair `left === right` (matching identical spoken/written text, not a translation-style pair). Worth confirming with you whether `left`/`right` are ever meant to differ here, or if it's always an audio-echo match — that affects whether the builder form should have one text field or two.

### 12. Build a Sentence
```
tier: { pick: number, items: [ { tokens: TokenArray } ] }
```
Separate pool per tier (already the pattern, needs explicit `pick` added). This is the only module whose *entire* content is just `tokens` — no separate word/sentence field — so its authoring form is really just the token editor by itself.

---

## Cross-module inconsistencies worth resolving before building the schema formally

1. ~~**Shared pool vs. per-tier pool** isn't consistent — Memory Pairs and Picture & Word share one pool across tiers; Word Scramble, Spelling, and Build a Sentence each give every tier its own separate pool. The builder needs to support both patterns per module type (this is a property of the *module type*, not something a teacher should have to configure per lesson).~~ **Resolved**: every module now uses a separate pool per tier, no exceptions. Memory Pairs and Picture & Word were the two that needed reversing; everything else already matched.
2. **Optional field inconsistency** (Spelling's `tokens: null`, `emoji` missing in silver/gold) suggests these fields were sometimes skipped rather than deliberately omitted. Worth deciding: should the builder *require* tokens/emoji everywhere for consistency, or keep them genuinely optional per module type?
3. **Icon representation** is emoji-only right now — no image field is actually used anywhere yet (Memory Pairs' `image: null` is unused scaffolding). Any "replace icon with custom image" feature is new ground, not a retrofit.

---

## Suggested next step

Turn this into a **formal JSON Schema (or TypeScript types)** per module type — one canonical definition each module's builder form, draft store, and publish step all reference. That would also be the natural place to decide the remaining open questions above (required-vs-optional fields, icon/image field design) — the shared-vs-per-tier pool question is no longer open, it's resolved (see above): every module gets its own per-tier pool with a configurable `pick`.

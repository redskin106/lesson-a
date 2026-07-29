# Shell Merge Specification — module-by-module, fully verified

> **STATUS: COMPLETE.** All 12 modules are merged into `lesson-shell-v2.html`, the Lesson
> Builder's `transformModuleForPublish` and `extractSpeakableForTTS` both output/read the
> correct shapes for every module (verified directly against the real shell code, not assumed),
> and `SHELL_TEMPLATE` inside `lesson-builder.html` has been swapped from the old pre-merge
> shell to the real, current `lesson-shell-v2.html`. This document is kept as a historical
> record of the merge process and the audio-capability findings, which remain accurate. The
> per-module table below reflects the *final*, confirmed-correct shapes — not the original
> pre-merge assumptions.
>
> **Two entries in the original version of this table were wrong and have been corrected below**,
> found during a post-completion audit rather than during the merge itself:
> - **listen-match**: the table used to say the correct fields were `{audio, text}` — that was
>   backwards. The real shell (`audio-match` renderer) destructures `{pick, items}` where each
>   item is `{left, right}`, identical to word-match's engine (it reuses word-match's free-pairing
>   code verbatim). The Lesson Builder's transform was fixed to match.
> - **put-in-order**: the correct shape is `{prompt, sequence, correct}`, not `{prompt, items,
>   correct}` — `sequence` is the display order (which the shell re-shuffles itself at runtime
>   regardless of what's given), `correct` is the target order. The Lesson Builder only needs the
>   teacher-authored correct order; `sequence` gets synthesized as a copy of it at publish time.

Every row below was confirmed by reading the actual file — either `module-demos/` during the
original merge, or `lesson-shell-v2.html` directly during the post-completion audit.

| Module | Real data contract (final, per `lesson-shell-v2.html`) | Audio? | Status |
|---|---|---|---|
| **gap-fill** | `tier: {pick, items:[{sentence, options, answer, tokens}]}` | Yes — `showGrammarReinforce()` speaks the full sentence on every correct answer | Merged, transform correct, audio-capable — done |
| **true-false** | `tier: {pick, items:[{statement, answer, tokens}]}` | Yes — same `showGrammarReinforce()`, fires on both correct and wrong (unlike gap-fill, which only fires on correct) | Merged, transform correct, audio-capable — done |
| **word-match** | `tier: {pick, items:[{left, right}]}` | No — confirmed, no `speak()` anywhere in the renderer | Merged, transform correct, correctly excluded from audio — done |
| **memory-pairs** | `tier: {pick, flipback, items:[{word, emoji, image, sentence, tokens}]}` — separate pool per tier | Yes | Merged, transform correct — done |
| **listen-choose** | `tier: {pick, items:[{audio, question, options, answer}]}` | Yes — core feature | Merged, transform correct — done |
| **put-in-order** | `tier: {pick, items:[{prompt, sequence, correct}]}` | No — confirmed | Merged, transform correct, correctly excluded from audio — done |
| **say-it** | `tier: {pick, items:[{prompt, target, keyWords?}]}` | Yes — core feature | Merged, transform correct — done |
| **picture-word** (`image-vocab`) | `tier: {pick, mode, items:[{word, emoji, sentence, cloze}]}` — separate pool per tier. `cloze` is just the answer word (e.g. "runs"), not a full sentence | Yes | Merged, transform correct — done |
| **word-scramble** | `tier: {pick, items:[{word, emoji, sentence, tokens}]}` | Yes | Merged, transform correct — done |
| **spelling** | `tier: {pick, items:[{word, emoji, sentence, tokens}]}` | Yes | Merged, transform correct — done |
| **listen-match** (`audio-match`) | `tier: {pick, items:[{left, right}]}` — same shape/engine as word-match | Yes — core feature | Merged, transform correct — done |
| **build-sentence** | `tier: {pick, items:[{tokens:[{text, role}]}]}` | Yes | Merged, transform correct — done |

## What's genuinely still open

- **An end-to-end publish test** — the whole chain (author → publish → real standalone file
  opened and played) has never been verified as one continuous flow. Everything above has been
  tested piece by piece. See `PROJECT_STATUS.md` section 0 for the current framing of this.
- **`bronze.png` and `gold.png`** — still worth double-checking these exist in every module's
  `assets/` folder before assuming tier-medal art is fully in place; this was flagged during the
  original merge and the resolution ("Nick will locate it") was noted but not independently
  re-verified since.

## Standing regression coverage

`run_all.js` (in the repo root) plus per-module ad-hoc Playwright tests built during the merge
cover: full multi-question sessions for every pool-based module, the free-pairing engine (Word
Match/Listen & Match), tier completion + star animation, the shared reinforcement overlay, tap
sfx call sites, and the Lesson Builder's pool editors + transform output for all 12 modules.
Re-run before trusting any future change.

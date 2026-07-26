# Lesson Builder — Technical Reference

_Dense, scannable, built to onboard a new conversation or a developer fast. For the narrative
version (why decisions were made, what to do next), see `LESSON_BUILDER_PROJECT_STATE.md`._

---

## Artifact manifest

| File | What it is |
|---|---|
| `authoring-screen-mockup-v2.html` | The interactive prototype. Open it directly in a browser — no server needed. Everything client-side, nothing persists on reload. |
| `lesson-builder-schema.md` | Real production JSON shape per module type, pulled directly from the live `lesson-a` repo's module files (not guessed). |
| `persistence-layer-spec.md` | Full backend design: platform choice, key structure, save behavior, security, rollout steps. Not yet built. |
| `LESSON_BUILDER_PROJECT_STATE.md` | Narrative state-of-project — what's real, what's designed, what's next. |
| `LESSON_BUILDER_REFERENCE.md` | This file. |

## Production repo context (for the *real* `lesson-a` site, separate from the builder)

- Repo: `redskin106/lesson-a` · Live site: `https://redskin106.github.io/lesson-a/`
- Deploy pattern: two-step GitHub API — GET file for current `sha`, then PUT new content with
  that `sha`. Always re-fetch `sha` immediately before writing.
- Legacy Pages builder (not Actions) — occasionally stalls after a rapid commit burst; a trivial
  follow-up push reliably re-triggers it.
- **No shared asset folder** — each of the 12 module folders duplicates its own copy of
  `bg_and_border.png`, `school_scene.png`, `silver.png`, `star.png`, `frame_mask.png`, plus the
  grammar-color JS utilities (`GRAMMAR_COLORS`, `safeShuffle`, `speak()`). Real, unresolved
  maintenance cost — the builder's Assets tab designs around this, doesn't fix it at the source.

## Module type reference (12 total, one structural shape — resolved)

**Previously three shapes (A/B/C, see below), now collapsed into one standard**: every module is
`tier: { pick: number, items: [...] }` — a separate pool per tier, `pick` configurable per
lesson/module. This was a real decision, not a simplification for convenience: identical exercises
repeated across bronze/silver/gold didn't make pedagogical sense once actually built, so the two
modules that used to share one pool across tiers (Memory Pairs, Picture & Word) were reversed to
match everyone else, and the four modules that had no pooling at all (Gap-fill, True/False,
Listen & Choose, Say It) gained it. Gap-fill, True/False, and Picture & Word are confirmed working
this way in `lesson-shell-v2.html`; the other 9 still need the same treatment as their merge comes up.

~~**Shape A — fixed array, index-based** (bronze=0/silver=1/gold=2): Gap-fill, True/False,
Listen & Choose, Say It, Put in Order.~~

~~**Shape B — tiered pools** (each tier has its own item pool): Word Match, Listen & Match,
Word Scramble, Spelling, Build a Sentence.~~

~~**Shape C — shared pool + per-tier config** (one pool used by all 3 tiers, tiers only change
settings): Memory Pairs (pairs count + flip-back speed), Picture & Word (interaction mode).~~

Grammar tokens are `{t: text, r: role}` in production for Gap-fill/True-False (phrase-grouped);
Build-a-Sentence tokens are per-chip, never merged, since each chip is individually draggable
in the live module.

## Architecture summary

- **No new platform or account** — drafts live in the browser, sharing is export/import,
  and publishing runs through a **GitHub Action already living in the repo** — nothing to
  sign up for, nothing new to maintain.
- **Publish is atomic**: blob → tree → commit → single ref-update switch. Nothing goes live
  until that switch succeeds; failure at any earlier point is a full no-op. A failure *after*
  the switch (rare — the Pages build lagging) is a different, milder case: content is live,
  just not yet visibly rebuilt.
- **Audio is two-phase**: free instant browser TTS for drafting, simulated "final" generation
  standing in for real ElevenLabs. Audio state is deliberately **separate from content state**
  — editing a field's text never silently marks its old audio as still valid.
- **Cross-lesson audio reuse** works by matching exact text + voice persona — no explicit
  "links" between fields, just literal string matching, with an explicit per-field override
  for when identical text should sound different (e.g. same word, different lesson energy).
- **Word Bank picks are always independent copies** — never live-linked. Editing a picked
  word in one lesson never touches the bank or any other lesson.
- **Saves are per-field, not per-lesson** — module+tier is the save unit, matching how the
  data's already structured, minimizing real collision risk between two people editing
  different parts of the same lesson simultaneously.

## Working agreements established during this build

- Read/verify real data shapes before building against them — never guess a schema.
- Test every change against a running instance (headless DOM + scripted interaction) before
  presenting it, not just visual/logical inspection.
- Run the full regression suite before calling any change done — this caught real regressions
  multiple times across the build.
- When a design choice is deliberately scoped down (a feature deferred, a corner cut), say so
  explicitly rather than silently shipping a smaller version of what was asked for.
- Prefer a fresh, previously-untested lesson for integration testing — a well-worn test case
  (Colors) accumulates state that can mask bugs a truly fresh path would catch.

## What's real vs. simulated in the mockup — the one list that matters most

| Piece | Status |
|---|---|
| All UI, forms, validation, live preview | Real |
| Grammar tagging, merge/split | Real |
| Draft audio (browser TTS) | Real |
| "Final" audio generation | **Simulated** — no real ElevenLabs call |
| Word Bank logic, cross-lesson reuse matching | Real |
| Schema transformation to production JSON | Real |
| Publish sequencing, atomicity logic, failure handling | Real logic — **simulated network calls** |
| Asset fan-out logic | Real logic — **simulated network calls** |
| Anything persisting after a page reload | **Not real** — no backend exists yet |

## Resuming this project in a new conversation

Paste this file plus `persistence-layer-spec.md` and `lesson-builder-schema.md` in as context.
That's enough to skip re-deriving anything above — the open work is executing the persistence
spec, the production-repo asset refactor, and the Colors content review, all independently
startable from here.

# Lesson Builder — Technical Reference

_Dense, scannable, built to onboard a new conversation or a developer fast. For the narrative
version (why decisions were made, what to do next), see `LESSON_BUILDER_PROJECT_STATE.md`._

---

## Artifact manifest

| File | What it is |
|---|---|
| `lesson-builder.html` | The real tool. Open it directly in a browser. Drafts persist across reloads in the browser; publishing goes through a real GitHub pipeline. Not a mockup — an earlier version of this document described `authoring-screen-mockup-v2.html`, a fully-simulated prototype; that phase is superseded. |
| `lesson-shell-v2.html` | The real production shell every published lesson runs on. All 12 modules, phone-frame chrome, sound effects, star-drop completion animation. `lesson-builder.html`'s live preview (`SHELL_TEMPLATE`) is a direct copy of this file's content. |
| `tts-tool.html` | The companion ElevenLabs-based audio generation tool. |
| `lesson-builder-schema.md` | Real production JSON shape per module type, verified directly against `lesson-shell-v2.html`'s actual `render()` functions — not guessed, and kept current as the shell/builder changed. |
| `SHELL_MERGE_SPEC.md` | Historical record of the shell merge process and the per-module audio-capability findings — now describes a completed process. |
| `persistence-layer-spec.md` | The original backend design doc. Its core call (no new platform — browser drafts + GitHub publish) is exactly what got built; treat this as background on *why*, not a pending task. |
| `LESSON_BUILDER_PROJECT_STATE.md` | Narrative state-of-project — what's real, what's next. |
| `LESSON_BUILDER_REFERENCE.md` | This file. |

## Production repo context (for the *real* `lesson-a` site, separate from the builder)

- Repo: `redskin106/lesson-a` · Live site: `https://redskin106.github.io/lesson-a/`
- Deploy pattern: two-step GitHub API — GET file for current `sha`, then PUT new content with
  that `sha`. Always re-fetch `sha` immediately before writing, every time — a stale `sha` is a
  422 error, not a silent overwrite.
- Legacy Pages builder (not Actions) — occasionally stalls after a rapid commit burst; a trivial
  follow-up push reliably re-triggers it.
- **No shared asset folder** — each of the 12 module folders duplicates its own copy of
  `bg_and_border.png`, `school_scene.png`, tier medal images, `star.png`, `frame_mask.png`, plus
  the grammar-color JS utilities (`GRAMMAR_COLORS`, `safeShuffle`, `speak()`). Real, unresolved
  maintenance cost — the builder's Assets tab designs around this, doesn't fix it at the source.
- PAT token used for the API calls should be revoked and regenerated periodically — a standing
  habit, not a one-time fix, and worth doing after any session with a lot of pushes.

## Module type reference (12 total, one structural shape — resolved)

Every module is `tier: { pick: number, items: [...] }` — a separate pool per tier, `pick`
configurable per lesson/module as a real number field in the authoring UI. This was a real
decision, not a simplification: identical exercises repeated across bronze/silver/gold didn't
make pedagogical sense once actually built, so the two modules that used to share one pool
across tiers (Memory Pairs, Picture & Word) were reversed to match everyone else, and the four
modules that had no pooling at all (Gap-fill, True/False, Listen & Choose, Say It) gained it.
**All 12 modules are confirmed working this way**, in both `lesson-shell-v2.html` and the
Lesson Builder's authoring/publish pipeline — this used to be a per-module rollout in progress;
it's now finished.

Grammar tokens use two different field-naming conventions depending on module — a real trap,
not a stylistic choice: `{t: text, r: role}` for Gap-fill, True/False, Memory Pairs, Picture &
Word, Word Scramble, and Spelling (phrase-grouped, merged chunks); `{text, role}` for Build a
Sentence alone (per-chip, never merged, since each chip is individually draggable in the live
module). See `lesson-builder-schema.md` for the full per-module breakdown.

## Architecture summary

- **No new platform or account** — drafts live in the browser, sharing is export/import, and
  publishing runs through direct GitHub API calls from the tool itself (blob → tree → commit →
  atomic ref-switch) — nothing to sign up for, nothing new to maintain.
- **Publish is atomic**: nothing goes live until the final ref-update switch succeeds; failure
  at any earlier point is a full no-op.
- **Audio has a real generation path**: free instant browser TTS for drafting, and a genuine
  ElevenLabs-backed "final" generation step through the companion `tts-tool.html`. Audio state
  is deliberately separate from content state — editing a field's text never silently marks its
  old audio as still valid; the Lesson Builder's "needs new audio" detection compares live
  content text against what was actually recorded, field by field.
- **Cross-lesson audio reuse** works by matching exact text + voice persona — literal string
  matching, with an explicit per-field override for when identical text should sound different.
- **Word Bank picks are always independent copies** — never live-linked.
- **Saves are per-field, not per-lesson** — module+tier is the save unit.

## Working agreements established during this build

- Read/verify real data shapes before building against them — never guess a schema, and never
  trust an older doc's claim about a shape without re-checking the actual current code.
- Test every change against a running instance (headless DOM + scripted interaction) before
  presenting it, not just visual/logical inspection.
- Run the full regression suite before calling any change done.
- When a design choice is deliberately scoped down, say so explicitly rather than silently
  shipping a smaller version of what was asked for.
- Prefer a fresh, previously-untested lesson for integration testing.
- On anything with a genuine pedagogical judgment call, state the reasoning back and get
  explicit sign-off before writing code — this was learned the hard way earlier in the project
  after a misunderstanding required a rebuild.

## What's real — the list that used to distinguish real from simulated

An earlier version of this document had a table here separating "real" from "simulated" pieces
of a mockup. That distinction no longer applies — there is no simulated layer left. All UI,
forms, validation, live preview, grammar tagging, draft and final audio generation, Word Bank
logic, schema transformation, publish sequencing and atomicity, and asset fan-out logic are real,
tested, and running against the real repo. The one thing genuinely not yet verified is the full
publish chain as one continuous test — see `LESSON_BUILDER_PROJECT_STATE.md`'s headline.

## Resuming this project in a new conversation

Paste this file plus `lesson-builder-schema.md` and `LESSON_BUILDER_PROJECT_STATE.md` in as
context. That's enough to skip re-deriving anything above — the open work is the end-to-end
publish test, a content review pass on Colors, and (per Nick's own stated priority sequence)
the Fading Hint Ladder once that test is done.

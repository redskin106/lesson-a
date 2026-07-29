# Lesson Builder — Project State

_Written to be readable on its own, without needing to re-read the conversation that produced
it. If you're picking this project back up — whether that's you in three months, or a developer
you've brought in — start here._

---

## What this project is

A web tool for authoring EFL lesson content across all 12 module types in the `lesson-a`
production shell (Gap-fill, Spelling, Word Match, Memory Pairs, and so on) — so you and future
TAs can build a lesson like Colors Around Us without hand-writing JSON, with a live preview
that matches exactly what a student will see, and audio/grammar-tagging tools built in.

## The honest headline

**This is a real, working tool now — not a prototype.** An earlier version of this document
described `authoring-screen-mockup-v2.html`, a fully-simulated mockup with no real backend and
no persistence. That phase is over. The current tool is `lesson-builder.html`: drafts persist
in the browser, publishing goes through a real GitHub pipeline (blob → tree → commit → atomic
ref-switch), the live preview genuinely renders the real production shell (not a simplified
stand-in), and all 12 module types have real, tested authoring screens producing data the shell
can actually read.

**What hasn't been verified yet: the full chain, start to finish, in one continuous test.**
Every individual piece has been tested — the pool editors, the publish transform's output shape
for all 12 modules, the shell swap, the TTS audio extraction — but nobody has yet clicked
Publish on a real lesson, taken the output file, opened it standalone, and confirmed a student
could actually play through it correctly. That's the natural next step, not a known gap.

---

## What's actually built and tested

- **Dashboard** — lesson cards with status, audio-issue counts, a New Lesson wizard
  (name → pick modules → reorder them)
- **All 12 module authoring screens**, sharing consistent chrome: tier tabs, a live preview pane
  using the real production shell, side-by-side tier comparison. Every module type is
  **pool-based** — a separate pool of exercises per tier (`{ pick, items: [...] }`), with `pick`
  (how many draw per session) a real, teacher-set number field, not a hardcoded constant. This
  was a significant structural change from an earlier design where several modules (Gap-fill,
  True/False, Listen & Choose, Say It) only supported one fixed exercise per tier, and two others
  (Memory Pairs, Picture & Word) shared one pool across all three tiers instead of each tier
  having its own.
- **Grammar tagging** — click-to-tag color coding with merge/split for multi-word phrases,
  working across every module type that uses it (Gap-fill, True/False, Memory Pairs, Picture &
  Word, Word Scramble, Spelling, Build a Sentence). Two different token field-naming conventions
  exist depending on module (`{t, r}` vs. Build a Sentence's `{text, role}`) — see
  `lesson-builder-schema.md` for exactly which is which.
- **A real audio system**: instant free draft playback via the browser's own voice, a real
  ElevenLabs-backed generation step through the companion TTS tool, and per-field "needs new
  audio" flagging that compares live content against what was actually recorded — genuinely
  re-verified against the real shell's actual `speak()` call sites for every module type (not
  assumed), including catching and fixing cases where the extraction logic had silently broken
  for several modules during the pool-conversion work.
- **A global Word Bank** — retroactively seeded from existing lesson content, picks are
  independent copies, audio reuse across lessons when the exact same text is picked elsewhere,
  with an explicit override path when a lesson deliberately needs different-sounding audio.
- **A genuinely atomic publish pipeline** — blob → tree → commit → one atomic switch, so a
  failure before that switch leaves the live site completely untouched.
- **A schema transformer** (`transformModuleForPublish`) that converts the builder's internal
  data into the exact shape the real shell expects, verified module-by-module directly against
  `lesson-shell-v2.html`'s actual `render()` functions — not guessed, and not just carried
  forward from an earlier design document. Two real bugs were caught this way: Picture & Word's
  `cloze` field was backwards (storing a full sentence instead of just the answer word), and
  Listen & Match's transform was outputting fields (`audio`/`text`) that don't match what the
  real shell reads (`left`/`right`, same engine as Word Match).

## What's designed and mostly real, one piece still open

**The persistence layer** — the design called for no new backend platform: drafts live in the
browser, occasional sharing happens via export/import, publishing runs through GitHub. That's
exactly what's built and working today. The one piece not yet proven is the full round-trip:
author a lesson → publish it → open the real resulting file → confirm it plays correctly for a
student, as one continuous test rather than verified in separate pieces.

## Deliberately deferred, not forgotten

- Live "who's editing this" presence indicators — skipped for simplicity
- Conflict-warning UI on simultaneous edits — accepted last-write-wins at the per-field level,
  since real collisions should be rare with a small team
- Formal per-teacher accounts — a simple name-picker was chosen over real logins
- **The production repo's own duplication problem** — the real `lesson-a` repo still has no
  shared asset folder and duplicates the grammar-color JS across all 12 real module files. The
  builder's Assets tab designs *around* this for now; actually centralizing it in the real repo
  is separate work, not yet started.
- **A content-quality pass on Colors** — Word Scramble's Gold tier currently uses words like
  "turquoise," "maroon," and "lavender," which is genuinely more advanced than fits A0–A1
  spelling practice. Worth reviewing before this lesson is treated as a real template.

---

## Suggested order for what's next

1. **The end-to-end publish test** (see headline above) — the real next step, not a known gap
   waiting on infrastructure.
2. **A short content review pass on Colors**, independent of the above.
3. **The production repo's shared-asset/JS refactor**, once the builder itself is the normal
   workflow for publishing, confirmed via step 1.
4. **The Fading Hint Ladder** (`hint-ladder-demo.html`) — explicitly Nick's own next major
   project after the base shell is solid, which it now is.

---

## A practical note

Every file this project has produced lives in the repo (`redskin106/lesson-a`) or this
conversation's outputs — confirm anything not yet pushed gets pushed before ending a session.

# Lesson Builder Project — Status Document
*Compiled from Claude's memory of past conversations + the full conversation that produced this update. Scope: the Lesson Builder, TTS tool, and lesson shell ecosystem only — AI-literacy classroom tools (Persona Prompt Builder, The Masher) are explicitly out of scope for now, by Nick's call. See the honesty note at the bottom — this is not guaranteed complete.*

---

## 0. Headline: the shell/builder reconciliation is DONE

The previous version of this document's whole section 2 was about "a real architecture split that needs reconciling" — two parallel shell designs, mismatched data contracts, a Lesson Builder that couldn't actually produce data the new shell could read. **That work is now complete, end to end:**

- All 12 modules are merged into one real, unified shell (`lesson-shell-v2.html`) — phone-frame chrome, real sound effects, star-drop completion animation, grammar-color reinforcement, the whole locked visual design from `module-demos/`. Nothing left in the old flat-design shell.
- Every module in both the shell and the Lesson Builder now uses the same standard: a **separate pool per tier**, `{pick, items: [...]}`, with `pick` genuinely teacher-configurable (a real number field in the authoring UI), not a hardcoded constant.
- The Lesson Builder's `transformModuleForPublish` outputs the correct shape for all 12 modules, verified against the real shell renderers directly (not assumed).
- The Lesson Builder's own live-preview template (`SHELL_TEMPLATE`) — previously a stale copy of the *old* pre-merge shell — has been swapped for the real `lesson-shell-v2.html` content. A real bug was found and fixed in the process: the embedded content's own closing `</script>` tag would have truncated the outer script block in any browser; fixed by escaping the slash.
- Tap sound effects, ported from the locked demos, are wired into every module that has them (8 of 12 — Memory Pairs, Picture & Word, Listen & Choose, and Say It deliberately don't, matching the demos).
- The TTS audio-extraction pipeline (`extractSpeakableForTTS`, `findMissingEmojiItems`) has been fully re-verified against the real shell: Gap-fill and True/False were wrongly *excluded* from audio generation (both genuinely speak via the reinforcement panel); Listen & Choose, Say It, Listen & Match, Spelling, Word Scramble, and Build a Sentence had all silently broken (crashing on the pool-shape conversion) and are now fixed. Put in Order and Word Match are confirmed genuinely silent, not just assumed.

**What has NOT been done yet: an actual end-to-end publish test** — click Publish in the Lesson Builder, take the real output file, open it standalone, confirm a real lesson plays correctly start to finish. Everything above has been tested piece-by-piece (transform output shapes, individual module editors and interactions, the shell swap in isolation) but not as one continuous chain. This is the natural next step.

---

## 1. Files to bring into a fresh conversation

**The three active tools:**
- `lesson-builder.html` — the authoring tool. All 12 modules pool-converted, `SHELL_TEMPLATE` is real shell-v2, TTS extraction fixed.
- `tts-tool.html` — the ElevenLabs audio generation tool.
- `run_all.js` — the standing regression test suite (needs Playwright + a local Chrome to run; ask before assuming a fresh sandbox has these). Now lives in the repo (`redskin106/lesson-a/run_all.js`), not just locally.

**The shell:**
- `lesson-shell-v2.html` — the real, complete, unified shell. All 12 modules, phone-frame chrome, sfx, star animation, tier-completion overlay (shown in the same overlay as per-question reinforcement, not a separate screen). This is what `SHELL_TEMPLATE` inside `lesson-builder.html` now contains.
- `module-demos/` (all 12 real module demo files + `test-harness.html`) — still the reference for locked visual/interaction design, useful if anything needs re-checking against the original intent.

**Other planning docs, staleness varies — check each doc's own header for a currency note:**
- `SHELL_MERGE_SPEC.md` — the module-by-module merge tracker; now describes a completed process. See that file's own header for the resolution.
- `lesson-builder-schema.md` — the field-level schema reference. Was already largely accurate for the pool-standardization decision; worth a final pass to confirm nothing drifted during the last conversion round.
- `LESSON_BUILDER_PROJECT_STATE.md` — written when the Lesson Builder was still a non-functional prototype ("nothing is live yet"). **That framing is now wrong** — it's a real, working, tested tool. Needs its own rewrite; not done as part of this pass.
- `persistence-layer-spec.md` — unrelated to today's work, a future spec for student-progress persistence. Still accurate as a forward-looking design doc.
- `hint-ladder-demo.html` — the standalone "v2" concept demo, still parked, not yet connected to anything. Explicitly sequenced as work that comes *after* the base shell is solid — which it now is.

---

## 2. What's actually live and working right now

- **`redskin106/lesson-a`** repo, GitHub Pages hosted. Colors lesson is published: `lessons/colors/index.html` + `lessons/colors/content.json`.
- **The Lesson Builder** — multi-instance module support, a real GitHub publish pipeline (blob→tree→commit→atomic ref-switch), pre-publish content-completeness and audio-completeness checks, missing-emoji detection, autosave/draft persistence, a working bridge to the TTS tool's format, and — as of today — a real, accurate live preview using the actual production shell.
- **The TTS tool** (ElevenLabs-based) — voice library browsing, per-line voice override, credit-usage tracking, draft persistence, merge-aware manifest import, human-readable filenames.
- **The published page's audio** — when a line has real generated audio, publish links it correctly; anything not yet generated falls back to browser speech synthesis invisibly.
- **A standing regression-test suite** (`run_all.js`) — automated load/navigation/wizard/export/persistence checks. Re-run after any future change to any of the files above.

## 3. Smaller known gaps, still open

- **No end-to-end publish test yet** (see section 0) — the natural next step.
- **The Lesson Builder's "Audio Polish" tab is being retired — decided, not yet executed.** Replace with a per-lesson "Check audio status" button reusing the already-working `getFullAudioStatusForLesson()` function; mostly wiring, not new engineering.
- **Shared asset publishing** (updating background/medal/star images across all 12 module folders from inside the Lesson Builder) is still out of scope. The `mockUploadAsset`/`SHARED_ASSETS` code is a simulated placeholder for an unbuilt "switch variants" idea (dark/light mode for lesson visuals) — design-from-scratch later, not a bug to fix.
- **Say It audio recording/storage** — a student's spoken attempt currently lives only in memory during self-assessment, then vanishes. Flagged as important for tracking development over time; wants a deliberate design pass (storage, access, retention).
- **Persistent student progress across devices** — needed for any future replay-grid/mastery features. Real decision point still open: local-only vs. a lightweight real backend (Firebase/Supabase). Leaned toward the real backend given shared classroom devices.

## 4. Real, thought-through ideas — discussed, not yet built

- **The student choice model** (agreed a while back): one input gate (a recognition exercise first), then free choice within Bronze exercises, Silver/Gold unlocked lesson-wide only after all Bronze is done, an end-of-lesson replay grid with star scores per module, a Bronze-only mode for the weakest students. Does **not** match what the shell does today (linear, per-module tier gating) — a real future change, not a bug.
- **The Fading Hint Ladder concept** (`hint-ladder-demo.html`): per-question hint level (0–3) escalating on wrong attempts (glow → category hint → letter hint), stars awarded inversely to hints used, a "reflect" button for metacognition after a hinted success, and a not-yet-built idea of a slower per-student mastery score that quietly raises a student's starting hint level over time (never shown as a visible number). **This is Nick's own next major step**, per his stated priority sequence: lesson shell → v2 hint ladder → basics track → dungeon/Minecraft directions activity → viral video project. The shell is now genuinely solid — this is unblocked.
- **A dedicated phonics exercise module** — letters spoken aloud as each letter-tile is tapped, distinct from Word Scramble (which deliberately only speaks the completed word, not individual letters, since it's a vocabulary exercise, not phonics).
- **Spiral curriculum**, 8 survival units (Identity, Numbers/Money, Food, Transport, Health, Time, Technology, Work), each with Bronze/Silver/Gold passes — Colors and Food Court are early instances, not the full set.
- **Flipped classroom model** — Google Slides as home discovery tool + lesson shell for in-class practice; Greetings is the first Foundations micro-lesson with an alien-character discovery hook.
- **A Chatterbox/Kokoro local audio pipeline** — explored as an ElevenLabs alternative, set aside for local-install friction (Python 3.11, GPU dependency). Sequenced after the ElevenLabs pipeline is fully solid, then added as a second, swappable option.
- **Claude Projects reorganization** — parked, not urgent. If picked back up: curate the knowledge base to only the *latest* version of each file, put standing working agreements in custom instructions.

## 5. Standing working agreements (worth keeping visible)

- Always read real data shapes before building — verify against the actual file, don't assume.
- Always run the full regression suite before treating a change as done.
- Discuss approach before coding on anything structurally significant, especially anything with a pedagogical judgment call in it — state the reasoning back and get sign-off first.
- Use fresh, untested lesson content for integration testing rather than only re-testing the same demo data.
- The Bronze/Silver/Gold framework (Say it / Say more / Say it well) is the pedagogical spine — mirrors the CG "level of detail" analogy Nick thinks in.
- PAT tokens get revoked and regenerated periodically — a habit, not a one-time fix.

---

## Honesty note — please read this part

This document is built from two sources only: Claude's compressed memory of past conversations (which drops detail and can miss things entirely), and the full content of the conversation that produced this update. **Claude has no ability to search or re-read other past conversations directly** — if something important was discussed in a session that isn't reflected here, this document won't know about it. Treat this as a strong, current draft — not a guaranteed-complete record.

# Lesson Builder Project — Status Document
*Compiled from Claude's memory of past conversations + this full conversation. Scope: the Lesson Builder, TTS tool, and lesson shell ecosystem only — AI-literacy classroom tools (Persona Prompt Builder, The Masher) are explicitly out of scope for now, by Nick's call. See the honesty note at the bottom — this is not guaranteed complete.*

---

## 0. Files to bring into the fresh conversation

Everything below is the real, current, verified state — upload all of it to start the new conversation on solid ground rather than re-deriving any of it.

**The three active tools:**
- `lesson-builder.html` — the authoring tool, latest version, all fixes from this session applied.
- `tts-tool.html` — the ElevenLabs audio generation tool, latest version.
- `run_all.js` — the standing regression test suite (needs Playwright + a local Chrome to run; ask before assuming a fresh sandbox has these).

**Shell design reconciliation — the active in-progress work:**
- `SHELL_MERGE_SPEC.md` — **read this one first, before touching any shell code.** Exact confirmed data contract and audio capability for all 12 modules, which 2 need a transform fix (memory-pairs, picture-word), which 2 need adding to the audio-capable set (gap-fill, true-false) and exactly when to do it, and the suggested build order.
- `lesson-shell-current-live.html` — what's actually live today (the app shell: name picker, navigation, tier progression, scoring — reusable as-is; individual module implementations inside it are the *old*, simpler design).
- `published-colors-index-baseline.html` — the real published Colors lesson, for reference/diffing.
- `module-demos/` (all 12 real module demo files + `test-harness.html`) — the *new*, correct, currently-unmerged visual design and data contracts for every module. This is the actual source of truth for what each module should look like and expect data-wise.

**Original planning docs:**
- `LESSON_BUILDER_REFERENCE.md`, `LESSON_BUILDER_PROJECT_STATE.md`, `lesson-builder-schema.md`, `persistence-layer-spec.md` — `lesson-builder-schema.md` has since been corrected to reflect the pool-standardization decision (every module now uses a separate per-tier pool with configurable `pick`); the other three haven't been re-checked against that decision yet.
- `hint-ladder-demo.html` — the standalone "v2" concept demo, parked, not yet connected to anything.

---

## 1. What's actually live and working right now

- **`redskin106/lesson-a`** repo, GitHub Pages hosted. Colors lesson is published: `lessons/colors/index.html` + `lessons/colors/content.json` — confirmed live via direct fetch from the repo, not just assumed.
- **The Lesson Builder** (authoring tool) — multi-instance module support (multiple copies of the same module type in one lesson), a real GitHub publish pipeline (blob→tree→commit→atomic ref-switch), a pre-publish content-completeness check, a pre-publish audio-completeness check that reads the *real* TTS-tool manifest (color-coded: green = real audio linked, orange = still on browser speech), missing-emoji detection, autosave/draft persistence across reloads, and a working bridge to export lesson content directly into the TTS tool's format.
- **The TTS tool** (ElevenLabs-based audio generation) — voice library browsing, per-line voice override for A/B comparing voices, real credit-usage tracking, draft persistence across reloads (with honest downgrade of anything that lost its generated audio on reload), merge-aware manifest import (editing one line doesn't wipe out already-approved audio for every other line), human-readable filenames (first few real words + stable id, not a cryptic dotted path).
- **The published page's audio** — when a line has been generated + pushed via the TTS tool, the publish step now correctly links it into the live page (`audioFile` reference); anything not yet generated falls back to browser speech synthesis invisibly. Verified this specific chain end-to-end with a real, mocked GitHub manifest.
- **A standing regression-test suite** (`run_all.js`, uses a real headless Chrome) — runs load/navigation/wizard/export/persistence checks automatically. Re-run after any future change to any of the three files above.

## 2. Found today: a real architecture split that needs reconciling

This is the big one, worth its own heading rather than burying it in a list.

- There are **two parallel versions of the lesson-playing shell**:
  1. The one actually live right now (`lessons/colors/index.html`) — a single monolithic file, simple visual design, no real images, no sound effects.
  2. A **separately designed, more polished version**, living in `demos/{module}/{module}-demo.html` for each of the 12 modules — real phone-frame layout, real background/scene images, sound effects, star-drop animations, grammar-color-coded reinforcement. This design work is real and locked, but **has never been merged into what actually gets published.**
- **The two versions don't even agree on the data contract** for some modules. Confirmed by reading the real files directly (not assumption):
  - **Memory Pairs & Picture/Word — RESOLVED, and the resolution itself changed since this was first found**: the *new* design (as found in `module-demos/`) wanted a shared `allItems` pool + a `tiers` array holding just `{mode}` (or `{name, pairs, flipback}` for Memory Pairs). Nick's call once this got discussed properly: **reverse that** — every module, these two included, gets a *separate* pool per tier (`tier: {pick, items:[...]}`), not a shared pool. Reasoning: identical exercises repeated across bronze/silver/gold didn't make pedagogical sense once actually built. Confirmed working in `lesson-shell-v2.html` for Picture & Word; Memory Pairs still needs the same treatment when its turn comes.
  - **This turned out to be bigger than just those two modules**: Nick's actual intent is that *every* module gets the ability to add multiple exercises per tier — a real, longstanding plan, not a new scope addition. `lesson-builder-schema.md` already documented most modules (8 of 12) as pool-based from the start; only Gap-fill, True/False, Listen & Choose, and Say It were single-fixed-item. Those four are being converted to the same pool standard too — Gap-fill and True/False already done and confirmed working in `lesson-shell-v2.html`, Listen & Choose and Say It still to come. **`pick` (items drawn per session) is meant to be configurable per lesson/module, not a hardcoded constant** — the Lesson Builder doesn't have a real field for this yet.
  - **Picture & Word's `cloze` field**: new design treats it as just the answer word (e.g. "runs"); assumed elsewhere as a full blanked sentence. Confirmed and fixed in `lesson-shell-v2.html`'s test data.
  - **Audio capability changed**: the new Gap-fill and True/False demos *do* have a reinforcement-panel audio moment on success (confirmed by reading the code) — the old live shell has none. Only **Put in Order** and **Word Match** remain audio-incapable in the new design (down from 4 excluded modules to 2).
- **Missing assets, confirmed by direct check**: `bronze.png` and `gold.png` tier-medal images **don't exist anywhere in the repo** — only `silver.png` does, and every demo file hardcodes it regardless of tier. Real bronze/gold artwork needs to be produced before a full tier-aware merge makes sense.
- **In progress**: merging the new module designs into one real, unified shell — started with Gap-fill, True/False, and Picture & Word as the first batch (chosen deliberately as a mixed difficulty set). Currently in a feedback/fix round with Nick on those three (several real bugs found and fixed: true/false's missing `.selected` CSS state, a qlabel contrast issue, the pool-standardization rework above) before moving to the remaining 9.

## 3. Smaller known gaps, still open

- **The Lesson Builder's "Audio Polish" tab is being retired — decided.** It was a global, cross-lesson backlog view, but every real piece of the actual working pipeline (bridge export, TTS manifest, pre-publish check) is lesson-scoped by nature; a global view duplicated that at a different granularity for a benefit that matters more at 20 lessons than at 2. **Concrete replacement, ready to build cheaply**: expose the existing `getFullAudioStatusForLesson()` function (already built and working for the pre-publish gate) as a standalone "Check audio status" button inside the lesson editor, available any time, not just when clicking Publish. Mostly wiring, not new engineering — remove the fake tab/nav entry and `AUDIO_BACKLOG` array, add the button.
- **Shared asset publishing** (updating background/medal/star images across all 12 module folders from inside the Lesson Builder) is still out of scope. The "switch between variants" idea referenced in the Lesson Builder's UI copy was **just a quick discussion — dark mode / light mode switching for lesson visuals — never actually implemented.** The `mockUploadAsset`/`SHARED_ASSETS` code in the Lesson Builder is a simulated placeholder for this unbuilt idea, not a working mechanism with a bug in it. Treat this as design-from-scratch later, not reverse-engineering.
- Field-level verification against real module code has been done for: Gap-fill, True/False, Listen & Choose, Memory Pairs, Picture & Word, Word Scramble, Spelling, Listen & Match, Sentence Building, Say It. **Put in Order and Word Match** haven't had the same close read yet (lower risk — no audio, simpler contracts — but not zero risk).
- The blank "Tap the correct picture" bug reported once was never reproduced against real code + real data (tried three times, all clean) — most likely a stale cached page from an earlier publish, not a live bug. Not fully closed the loop on this with a confirmed fresh-load retest.

## 4. Real, thought-through ideas — discussed, not yet built

- **The student choice model** (agreed a while back): one input gate (a recognition exercise first), then free choice within Bronze exercises, Silver/Gold unlocked lesson-wide only after all Bronze is done, an end-of-lesson replay grid with star scores per module, a Bronze-only mode for the weakest students. Confirmed this does **not** match what the live shell actually does today (strictly linear, per-module tier gating).
- **Persistent student progress across devices** — needed for the choice model's replay grid to mean anything, and for tracking development over time generally. Real decision point: local-only (simple, but breaks across shared classroom devices) vs. a real lightweight backend (Firebase/Supabase — more setup, but survives device switching). Leaned toward wanting the real backend given the shared-device reality.
- **Say It audio recording/storage** — currently nothing is saved anywhere; a student's spoken attempt lives only in memory during self-assessment, then vanishes. Flagged as an important feature for tracking a student's own development, wants a deliberate design pass (where it's stored, who can access it, retention) rather than a quick patch.
- **The audio rules set for different lessons a while back** — Nick flagged that these may have drifted from what's actually implemented, the same way the shell's visual design did. Not yet re-audited.
- **The Fading Hint Ladder concept** (`hint-ladder-demo.html`, standalone, not connected to any of the 12 real modules): per-question hint level (0–3) escalating on wrong attempts (glow → category hint → letter hint), stars awarded inversely to hints used, a "reflect" button for metacognition after a hinted success, and a not-yet-built idea of a slower per-student mastery score that quietly raises a student's starting hint level over time (never shown as a visible number). Explicitly sequenced as **"v2" work**, meant to come after the base shell — so it being unbuilt is expected, not a miss.
- **Other stated priorities, in Nick's own sequence**: complete lesson shell v1 → v2 hint ladder → basics track → dungeon/Minecraft directions activity → viral video project. Only the first is substantially underway.
- **Spiral curriculum**, 8 survival units (Identity, Numbers/Money, Food, Transport, Health, Time, Technology, Work), each with Bronze/Silver/Gold passes — the Colors and Food Court lessons built so far are early instances of this, not the full set.
- **Flipped classroom model** — Google Slides as home discovery tool + lesson shell for in-class practice; Greetings is the first Foundations micro-lesson with an alien-character discovery hook.
- **A Chatterbox/Kokoro local audio pipeline** was explored as an ElevenLabs alternative, but set aside for now due to local install friction (Python 3.11, GPU dependency) — ElevenLabs is the active path.
- **Claude Projects reorganization** — discussed, parked, not urgent. Recommendation if picked back up: curate the knowledge base to only the *latest* version of each file, put standing working agreements in custom instructions.

## 5. Standing working agreements (from memory, worth keeping visible)

- Always read real data shapes before building — don't assume, verify against the actual file.
- Always run the full regression suite before treating a change as done.
- Discuss approach before coding on anything structurally significant.
- Use fresh, untested lesson content for integration testing rather than only re-testing the same demo data.
- The Bronze/Silver/Gold framework (Say it / Say more / Say it well) is the pedagogical spine — mirrors the CG "level of detail" analogy Nick thinks in.

---

## 6. Resolved this session — a round of open questions, cleared

- **Bronze/gold medal art**: exists somewhere, Nick will locate it — not actually missing from the world, just not yet in the repo.
- **Backend decision (persistence) and Say It recording storage**: confirmed related, to be decided together, not separately.
- **Chatterbox/Kokoro**: not abandoned — sequenced after the ElevenLabs pipeline is fully solid, then added as a second, swappable option in the TTS tool.
- **"Audio rules that went under the radar"**: this concern is already fully addressed by `SHELL_MERGE_SPEC.md` — that document *is* the confirmed, per-module audio-behavior audit Nick was worried had drifted. Nothing further to check here.
- **The shared-asset "switch variants" idea**: just a quick discussion — dark mode / light mode switching for lesson visuals — never actually implemented. The Lesson Builder's `SHARED_ASSETS`/`mockUploadAsset` code is a simulated placeholder for this unbuilt idea, not a broken working mechanism. Future work here is design-from-scratch, not debugging.
- **No hidden lessons**: scope is confirmed as exactly what's been seen — Colors, Food Court, and the individually-designed modules in `demos/`. Nothing else exists.
- **`SESSION.md`**: still unresolved — doesn't exist on `main`, `master`, `dev`, `develop`, or `draft` branches. Nick isn't sure it was ever deleted; best guess is it may be a local-only file that was never pushed to the repo, worth checking Nick's own computer rather than GitHub.
- **Audio Polish tab**: decided to retire it entirely rather than reconnect it to real data. Replace with a simple per-lesson "Check audio status" button in the editor, reusing the already-working `getFullAudioStatusForLesson()` function — see the gap entry above for specifics.


## Honesty note — please read this part

This document is built from two sources only: Claude's compressed memory of past conversations (which drops detail and can miss things entirely), and the full content of this one very long conversation. **Claude has no ability to search or re-read other past conversations directly** — if something important was discussed in a session that isn't reflected here, this document won't know about it. Please treat this as a strong first draft to correct, not a guaranteed-complete record — anything you remember that's missing should get added before this becomes the seed for a fresh conversation.

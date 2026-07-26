# Shell Merge Specification — module-by-module, fully verified

> **Update, post-merge decision**: every module is now standardized to a per-tier pool —
> `tier: { pick: number, items: [...] }`, with `pick` configurable per lesson/module rather than
> a hardcoded constant. This reverses what this doc originally said for **memory-pairs** and
> **picture-word** (shared `allItems` pool across tiers) — those two are now separate-pool-per-tier
> like everything else. It also means **gap-fill** and **true-false** are no longer single-fixed-item
> modules — both are pool-based now too, confirmed working in `lesson-shell-v2.html`. See
> `lesson-builder-schema.md` for the full corrected per-module shapes. The table below is kept for
> the audio-capability findings, which are still accurate, but the "Real data contract" column for
> gap-fill, true-false, memory-pairs, and picture-word is superseded — check the schema doc instead.

Every row below was confirmed by reading the actual file in `module-demos/`, not assumed.
"Transform status" tells you exactly what the Lesson Builder's `transformModuleForPublish`
needs, once this module gets merged into the new shell and that shell replaces the live one.

| Module | Real data contract | Audio? | Transform status |
|---|---|---|---|
| **gap-fill** | `{sentence, options, answer, tokens}` per tier | **NEW** — `showReinforce()` speaks the full sentence on success | Shape already correct. **Add to audio-capable list** (currently excluded — was correct for the old shell, wrong once merged) |
| **true-false** | `{statement, answer, tokens}` per tier | **NEW** — same `showReinforce(correct)` pattern | Shape already correct. **Add to audio-capable list.** Confirm exact trigger (correct only, or also wrong?) when integrating |
| **word-match** | `{pairs:[{left,right}]}` per tier | No — confirmed, no `speak()` anywhere | No change. Stays excluded from audio |
| **memory-pairs** | ~~`{allItems:[...], tiers:[{name,pairs,flipback}]}` — shared pool~~ **SUPERSEDED**: now `tier: {pick, flipback, items:[...]}` — separate pool per tier, see `lesson-builder-schema.md` | Yes | **Needs fixing** — current transform wrongly uses per-tier item lists, but the fix target itself changed: don't revert to the old shared `allItems`/`tiers` shape, build the new per-tier-pool shape instead |
| **listen-choose** | `{tier, audio, question, options, answer}` flat per tier | Yes — core feature | Already correct, no change |
| **put-in-order** | `{prompt, items, correct}` per tier | No — confirmed | No change |
| **say-it** | `{tier, prompt, target}` (+ optional `keyWords`, not exercised in this demo's test data) | Yes — core feature | Already correct, no change |
| **picture-word** | ~~`{allItems:[...], tiers:[{mode}]}`~~ **SUPERSEDED**: now `tier: {pick, mode, items:[...]}` — separate pool per tier, see `lesson-builder-schema.md` | Yes | **Needs fixing** — same per-tier-pool rebuild as memory-pairs, PLUS `cloze` field meaning is currently wrong in the transform (treated as a full sentence, should be just the answer word) — confirmed and already fixed in `lesson-shell-v2.html`'s own test data |
| **word-scramble** | `{items:[{word,emoji,image,sentence}]}` per tier | Yes | Already correct, no change |
| **spelling** | `{items:[{word,emoji,image,sentence}]}` per tier | Yes | Already correct, no change (sentence field made unconditional earlier this session to prevent a crash) |
| **listen-match** | `{pairs:[{audio,text}]}` per tier | Yes — core feature | Already correct, no change (fixed from wrong `left`/`right` fields earlier this session) |
| **build-sentence** | `{items:[{tokens:[{text,role}]}]}` per tier | Yes | Already correct, no change |

## What this means concretely for the merge

**Only 2 of 12 modules need a transform fix**: memory-pairs and picture-word. Everything else in
the Lesson Builder's `transformModuleForPublish` already matches the real, confirmed contract —
don't touch what isn't broken.

**2 of 12 modules need adding to the audio-capable set** once (and only once) the new shell
replaces the old live one: gap-fill and true-false. Do this in the same commit as the shell
swap, not before — the currently-live shell genuinely has no audio for these, so extracting
audio for them today would generate lines that can't play yet.

**2 of 12 modules confirmed to have zero audio capability, in both old and new designs**:
put-in-order and word-match. Never add these to the audio-capable set.

## Known blocker, not yet resolved

`bronze.png` and `gold.png` don't exist anywhere in the repo — confirmed via direct HTTP check
against every module's `assets/` folder. Every demo file hardcodes `silver.png` regardless of
tier (these are fixed single-tier snapshots, not live tier-switchers). Real bronze/gold artwork
needs to exist before a genuinely tier-aware merge is complete — worth surfacing to Nick early
in the new conversation rather than discovering it mid-build.

## Suggested build order for the new conversation

1. Gap-fill, True/False, Picture & Word — the originally agreed first trio (deliberately mixed
   difficulty: simplest, audio-but-simple-shape, hardest-shape).
2. Get Nick's review on those three before continuing.
3. Remaining 9, same process.
4. Only once all 12 are merged and tested: swap the Lesson Builder's `SHELL_TEMPLATE`, fix the
   2 transform cases, add gap-fill/true-false to the audio-capable set — all together, since
   they're only correct as a set once the new shell is what's actually live.
5. Re-run `run_all.js` (the regression suite) after every step, not just at the end.

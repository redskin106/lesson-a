# Lessons 3 and 4 (Saraburi nursing college) - first full build, 15 Nov 2026
Open `lesson3.html` / `lesson4.html` (arrow keys or the on-screen arrows; keys 1/2/3 switch bronze/silver/gold on Study exercises), `board.html?case=3|4` on the teacher screen, `team.html?case=3|4` on each tablet.
Self-contained pages, no network, emoji placeholders for all art, browser text-to-speech for the audio clues.
Source: `src/content.py` (all lesson and clue content), `src/deck.html`, `src/board.html`, `src/team.html`, `python3 src/build.py` regenerates the four pages.
Medical content cross-check: project doc `claude/medical-cross-check-lessons-3-4-nov2026.md`.

## Module review (15 Nov, library rebuild step 1)
`modules.html` = one slide per new module in the Lessons 1-2 look (built by `deck-library/lessons/modules_gallery.py`); `team.html` = restyled tablet page (`deck-library/lessons/team_pages.py`).
New modules live in `deck-library/sxl/modules/clue.py` (vol_ladder, dials3, frames3, timetable, reveal, choice, boss, case_board); medals = any slide with `levels:[bronze,silver,gold]`; hooks in `sxl/core.py` (BUILD_EXT, EXT_JS, EXT_CSS) and `sxl/interactive.py`.
`lesson3.html` / `lesson4.html` are still the first quick draft, to be rebuilt from these modules once reviewed.

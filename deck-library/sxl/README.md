# SkillsXLab lesson-deck library (sxl)
Content is data, layout is a module. A slide = a dict {'m': module, 'phase': 'ENGAGE|STUDY|ACTIVATE', ...data}. A lesson = a list of slides. `sxl.build(spec, outdir, pdf=path)` renders 1920x1080 PNGs (+ light PDF).
Modules live in sxl/modules/, register with @module('name'), and take one dict. Art that is not there yet renders as a labelled placeholder (art()).
Built: sort, chat, contrast, storyboard.
To port from Lesson 1: cover, engage_photo, cast, rule, dial, slot, role_cards, timer, recap, exit, question_drill, today/recap card.
New for Lesson 2: case_cover, evidence_board, sound_sort, timeline_sort, spot_the_fib, info_gap, match_pairs, story_flip.

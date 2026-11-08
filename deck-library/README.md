# SkillsXLab deck library
`sxl/` = modules (content is data, layout is a module); `lessons/` = lesson specs (lesson1.py, lesson2.py), builders for the interactive offline files, printables and run sheets.
Not in the repo: `art/` (Gemini art, kept with the lesson files), fonts and Fluent Emoji PNGs; their paths are set at the top of `sxl/core.py`. Catalog: project doc `claude/module-catalog.md`.
Static: `python3 lessons/lesson1.py` -> PNGs + light PDF. Interactive: `python3 lessons/lesson1_interactive.py`.
